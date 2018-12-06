# -*- coding: utf-8 -*-
from __future__ import print_function
from __future__ import unicode_literals

from django.contrib.auth.decorators import login_required
from django.shortcuts import render,redirect
from django.http import Http404, HttpResponseRedirect, HttpResponseForbidden, HttpResponse

from apps_cenco.db_app.models import Alumno,Expediente,DetalleEstado,Horario,Reservacion
from datetime import datetime, timedelta
from django.contrib import messages
from apps_cenco.db_local.models import ConfigCentroComputo

from django import template
register=template.Library()

# Create your views here.
@register.filter(name='split')
def split(value, arg):
    return value.split(arg)

@register.filter(name='diaSemana')
def diaSemana(value):
    if(value=='Lunes'):
        dia=1
    if (value == 'Martes'):
        dia = 2
    if (value == 'Miercoles'):
        dia = 3
    if (value == 'Jueves'):
        dia = 4
    if (value == 'Viernes'):
        dia = 5
    if (value == 'Sabado'):
        dia = 6
    if (value == 'Domingo'):
        dia = 7
    return dia

@register.filter(name='strip')
def strip(value):
    return value.strip()

@register.filter(name='reservaciones')
def reservaciones(dia,idhorario):
    cant_pcs = ConfigCentroComputo.objects.get(codigo=1)
    diaHoy = int(datetime.now().date().strftime("%w"))
    if (diaHoy == 0):
        diaHoy = 7
    fecha = (datetime.now().date() + timedelta(days=dia-diaHoy)).strftime('%Y-%m-%d')
    cant_reservaciones=Reservacion.objects.filter(horario_id=idhorario,fecha_reservacion=fecha).count()
    cupos=cant_pcs.cant_computadoras_disp-cant_reservaciones
    return cupos

@login_required
def reservar_practica(request):
    if request.user.groups.filter(name="Alumno").exists():
        alumno = Alumno.objects.filter(username=request.user).first()
        expediente = Expediente.objects.filter(alumno=alumno, activo_expediente=True).first()
        detalleEstado = DetalleEstado.objects.filter(alumno=alumno, actual_detalle_e=True).first()
        estado = detalleEstado.estado.tipo_estado
        if (expediente.fecha_proximo_pago_exp > datetime.now().date() and estado == 'Activo'):
            solvente = True
        else:
            solvente = False
        dia = int(datetime.now().date().strftime("%w"))
        if (dia == 0):
            dia = 7

        fechaLimite = (datetime.now().date() + timedelta(days=7 - dia)).strftime('%Y-%m-%d')
        hoy = datetime.now().date().strftime('%Y-%m-%d')
        horarios = Horario.objects.raw('select codigo,dias_asignados, hora_inicio,hora_fin from db_app_horario except ' +
                                        'select db_app_horario.codigo,dias_asignados, hora_inicio,hora_fin from db_app_horario inner join db_app_grupo ' +
                                        'on db_app_horario.codigo = db_app_grupo.horario_id and db_app_grupo."fechaInicio"::date <= ' + "'" + fechaLimite + "'" + '::date')

        existeReservacion=Reservacion.objects.raw('select * from db_app_reservacion where alumno_id = '+ str(alumno.codigo) +' and "fecha_reservacion"::date between ' + "'"+ hoy  + "'" + '::date and ' + "'"+ fechaLimite  + "'" + '::date')

        horaActual = datetime.now().time()
        reservacion_actual = None
        for reservacion in existeReservacion:
            if str(reservacion.fecha_reservacion) == str(hoy) == hoy:
                if reservacion.horario.hora_inicio > horaActual:
                    reservacion_actual=reservacion
            else:
                reservacion_actual = reservacion

        context = {"solvente": solvente, "horarios": horarios, "diaActual": dia,"existeReservacion": reservacion_actual,"horaActual":horaActual}

        if 'reservar' in request.POST:
            horario=request.POST.get('codigoHorario')
            diaReserva=request.POST.get('diaSemana')
            actual=datetime.now().date()
            fechaReserva=( actual + timedelta(days=int(diaReserva) - dia)).strftime('%Y-%m-%d')
            reservacion=Reservacion.objects.create(fecha_reservacion=fechaReserva,alumno_id=alumno.codigo,horario_id=horario)
            reservacion.save()
            messages.success(request, 'La reservación se realizo con éxito')
            return redirect('reservarPractica')

        if 'cambiar' in request.POST:
            codReserva=request.POST.get('codResExistente')
            horario=request.POST.get('codigoHorario2')
            diaReserva=request.POST.get('diaSemana2')
            actual=datetime.now().date()
            fechaReserva=( actual + timedelta(days=int(diaReserva) - dia)).strftime('%Y-%m-%d')
            reservacion=Reservacion.objects.filter(codigo_reservacion=codReserva).first()
            reservacion.fecha_reservacion=fechaReserva
            reservacion.horario_id=horario
            reservacion.save()
            messages.success(request, 'La reservación se modifico con éxito')
            return redirect('reservarPractica')

        if 'cancelar' in request.POST:
            codigo=request.POST.get('codResCancelar')
            reservacion=Reservacion.objects.filter(codigo_reservacion=codigo).first()
            reservacion.delete()
            messages.success(request, 'La reservación se cancelo con éxito')
            return redirect('reservarPractica')


        return render(request, 'modulo_practicas/reservar_practica_libre.html',context)
    else:
        raise Http404('Error, no tiene permiso para esta página')

