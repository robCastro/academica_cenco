# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden, HttpResponse, JsonResponse, Http404

from apps_cenco.db_app.models import Alumno, Encargado, DetallePago, Colegiatura

from datetime import datetime, timedelta

from math import ceil #Redondea hacia arriba
# Create your views here.

@login_required
def detalle_pago(request, idAlumno):
    try:
        alumno = Alumno.objects.get(pk = idAlumno)
    except Alumno.DoesNotExist:
        raise Http404('Alumno no existe')
    plantillaBase = "plantillas_base/"
    mostrarLinkModPago = False
    mostrarLinkIngresarPago = False
    if request.user.groups.filter(name="Asistente").exists():
        plantillaBase = plantillaBase + "base_asistente.html"
        mostrarLinkIngresarPago = True
    elif request.user.groups.filter(name="Director").exists():
        plantillaBase = plantillaBase + "base_director.html"
        mostrarLinkModPago = True
    elif request.user.groups.filter(name="Encargado").exists():
        if not Alumno.objects.filter(codigo=idAlumno, encargado=Encargado.objects.get(username=request.user)).exists():
            return HttpResponseForbidden("Usted no es encargado del estudiante que está consultando.")
        plantillaBase = plantillaBase + "base_encargado.html"
    elif request.user.groups.filter(name="Alumno").exists():
        if not Alumno.objects.filter(codigo=idAlumno, username=request.user).exists():
            return HttpResponseForbidden("No puede consultar asistencias de otros alumnos.")
        plantillaBase = plantillaBase + "base_alumno.html"
    else:
        return HttpResponseForbidden('No tiene acceso a esta url')
    hoy = datetime.today()
    cantidadSemanas = 0
    monto = 0
    expediente = alumno.expediente_set.get(activo_expediente=True)
    colegiatura = expediente.colegiatura_set.get(actual_colegiatura=True)
    ultimoPago = DetallePago.objects.filter(colegiatura=colegiatura).order_by('fecha_pago').last()
    permitirModPago = False
    if ultimoPago != None:
        permitirModPago = (datetime.date(hoy) - ultimoPago.fecha_pago) < timedelta(days=7) and request.user.groups.filter(name="Director").exists()
    print permitirModPago
    rango = 'mes' #El rango por defecto
    cantidadDias = 30 #Utilizado para rangos de mes, trimestre, semestre, etc.
    if request.method == 'POST':
        rango = request.POST.get('cbxPeriodo')
        if rango == 'mes':
            cantidadDias = 30
        elif rango == 'trim':
            cantidadDias = 90
        elif rango == 'sem':
            cantidadDias = 180
        elif rango == 'anual':
            cantidadDias = 365
        else:
            cantidadDias = -1
    if cantidadDias == -1: #Si se solicitan todos los pagos
        pagos = colegiatura.detallepago_set.order_by('fecha_pago')
    else:
        pagos = colegiatura.detallepago_set.filter(fecha_pago__range=
                                                   (hoy - timedelta(days=cantidadDias), hoy)).order_by('fecha_pago')
    if expediente.fecha_proximo_pago_exp > datetime.date(hoy):
        estado = 'Solvente'
    else:
        estado = 'Insolvente'
        diferencia = datetime.date(hoy) - expediente.fecha_proximo_pago_exp
        cantidadSemanas = ceil(diferencia.days/7.0) #Redondea hacia arriba el resultado
        monto = float(colegiatura.cuota_semanal) * cantidadSemanas #Convertir cuota de decimal a float
    context = {
        'alumno' : alumno,
        'plantillaBase' : plantillaBase,
        'linkIngresarPago' : mostrarLinkIngresarPago,
        'linkModPago' : mostrarLinkModPago,
        'ultimoPago' : ultimoPago,
        'expediente' : expediente,
        'estado' : estado,
        'cantidadSemanas' : cantidadSemanas,
        'monto' : monto,
        'colegiatura' : colegiatura,
        'pagos' : pagos,
        'rango' : rango,
        'permitirModPago' : permitirModPago
    }
    return render(request, 'modulo_pagos/detalle_pagos.html', context)