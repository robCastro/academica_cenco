# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseForbidden, HttpResponse, JsonResponse, Http404
from django.shortcuts import render, get_object_or_404

import locale
#locale.setlocale(locale.LC_TIME, 'es_ES')

import datetime

# Create your views here.
from apps_cenco.db_app.models import DetalleEstado, Grupo, Empleado, Alumno, Inscripcion, Asistencia, Estado
from apps_cenco.modulo_asistencia.forms import IntervaloFechaForm


def ver_reporte_estados(request):
    form_fecha = IntervaloFechaForm()
    detalle_semanal = DetalleEstado.objects.raw('select 1 as codigo_detalle_e, count(fecha_detalle_e), fecha_detalle_e '
                                                'from db_app_detalleestado '
                                                'where fecha_detalle_e >= (current_date - 8) '
                                                'and estado_id = 1 and actual_detalle_e = true '
                                                'group by fecha_detalle_e '
                                                'order by fecha_detalle_e;')
    maxim = 0
    for det in detalle_semanal:
        if det.count > maxim:
            maxim = det.count

    context = {'detalle_semanal': detalle_semanal, 'maximo': maxim+1, 'form': form_fecha}

    return render(request, 'modulo_asistencia/director_ver_estados.html', context)


def filtrar_estado_por_periodo(request):
    if request.method == 'POST':
        opt_tipo = request.POST.get('tipo')
        if opt_tipo == 'inscritos':
            tipo = '2'
        elif opt_tipo == 'retirados':
            tipo = '3'
        elif opt_tipo == 'graduados':
            tipo = '4'
        else:
            tipo = '1'

        if request.POST.get('opcion') != 'personalizado':
            if request.POST.get('opcion') == 'mensual':
                seleccion = '30'
            elif request.POST.get('opcion') == 'semestral':
                seleccion = '183'
            elif request.POST.get('opcion') == 'anual':
                seleccion = '365'
            else:
                seleccion = '8'

            datos_por_periodo = DetalleEstado.objects.raw(
                'select 1 as codigo_detalle_e, count(fecha_detalle_e), fecha_detalle_e ' 
                ' from db_app_detalleestado ' 
                ' where fecha_detalle_e >= (current_date - ' + seleccion + ') '
                'and estado_id = ' + tipo +
                'group by fecha_detalle_e '
                'order by fecha_detalle_e;')
            maxim = 0
            raw_data= []
            raw_dates = []
            for det in datos_por_periodo:
                raw_data.append(det.count)
                raw_dates.append(det.fecha_detalle_e.strftime('%d %b'))
                if det.count > maxim:
                    maxim = det.count
            return JsonResponse({'datos_filtro': raw_data, 'fechas_filtro': raw_dates, 'maximo': maxim + 1})

        else:
            form_fecha = IntervaloFechaForm(request.POST)
            if form_fecha.is_valid():
                form = form_fecha.cleaned_data
                fecha1 = form.get('fechaInicial')
                fecha2 = form.get('fechaFinal')
                if fecha1 > fecha2:
                    return HttpResponse('Error: Verifique que las fechas sean correctas', status=500)
            else:
                return HttpResponse('Error: Las fechas no son validas', status=500)

            datos_por_periodo = DetalleEstado.objects.raw(
                'select 1 as codigo_detalle_e, count(fecha_detalle_e), fecha_detalle_e' 
                ' from db_app_detalleestado' 
                ' where fecha_detalle_e >= ' + "'" + str(fecha1) + "'" +
                ' and fecha_detalle_e <= ' + "'" + str(fecha2) + "'" +
                ' and estado_id = ' + tipo +
                ' group by fecha_detalle_e'
                ' order by fecha_detalle_e;')
            maxim = 0
            raw_data= []
            raw_dates = []
            for det in datos_por_periodo:
                raw_data.append(det.count)
                raw_dates.append(det.fecha_detalle_e.strftime('%d %b'))
                if det.count > maxim:
                    maxim = det.count
            return JsonResponse({'datos_filtro': raw_data, 'fechas_filtro': raw_dates, 'maximo': maxim + 1})
    else:
        return HttpResponseForbidden('No tiene acceso a esta url')


@login_required
def prof_detalle_grupo(request, id_grupo):
    try:
        empleado = Empleado.objects.get(username=request.user)
        grupo = Grupo.objects.get(codigo=id_grupo, empleado=empleado)
        alumnos = Alumno.objects.filter(grupo=grupo)
        context = {'grupo': grupo, 'alumnos': alumnos}
        return render(request, 'modulo_asistencia/profesor_detalle_grupo.html', context)
    except ObjectDoesNotExist:
        raise Http404("No se encuentra la ruta especificada o no es el usuario correcto")




#Encargada de manejar metodo GET, valida si se puede o no ingresar asistencias en este momento
@login_required
def asistencia_a_clases(request, id_grupo):
    try:
        grupo = Grupo.objects.get(codigo = id_grupo)
    except Grupo.DoesNotExist:
        return Http404("Grupo no Existe")
    # validando tomar asistencia solo una vez
    hoy = datetime.datetime.now().date().strftime("%d/%m/%y")
    asistencias = Asistencia.objects.filter(fecha_asistencia=datetime.datetime.now())
    tomarAsistencia = True;
    for asistencia in asistencias:
        if asistencia.inscripcion.grupo == grupo:
            tomarAsistencia = False
            break;
    if tomarAsistencia:
        inscripciones = grupo.inscripcion_set.filter(actual_inscripcion = True)
        codAlumnos = []
        for inscripcion in inscripciones:
            codAlumnos.append(inscripcion.alumno.codigo)
        alumnos = Alumno.objects.filter(pk__in = codAlumnos).order_by('apellido')
        for alumno in alumnos:
            alumno.tel = alumno.telefono_set.first()
        context = {
            'grupo' : grupo,
            'hoy': hoy,
            'alumnos' : alumnos,
            'tomarAsistencia' : tomarAsistencia,
        }
        return render(request, 'modulo_asistencia/profesor_ingresar_asistencia.html', context)
    else:
        context = {
            'tomarAsistencia':tomarAsistencia,
        }
        return render(request, 'modulo_asistencia/profesor_ingresar_asistencia.html', context)

#Encargada de metodo POST, almacena las asistencias y retorna a "asistencia_a_clases" para regenerar la pantalla
@login_required
def guardarAsistencia(request, id_grupo):
    if request.method == "POST":
        print "usando post"
        try:
            grupo = Grupo.objects.get(pk = id_grupo)
        except Grupo.DoesNotExist:
            return Http404('Grupo no existe')
        inscripciones = grupo.inscripcion_set.filter(actual_inscripcion=True)
        for inscripcion in inscripciones:
            if request.POST.get(str(inscripcion.alumno.codigo)):
                asistencia = Asistencia.objects.create(fecha_asistencia=datetime.datetime.now(), asistio=True, inscripcion = inscripcion)
                asistencia.save()
                #detalle_estado = inscripcion.alumno.detalleestado_set.filter(actual_detalle_e=True).first()
                #estado_actual = detalle_estado.estado.tipo_estado
                print "datos para detalle: " + str(inscripcion.alumno.codigo)
                detalle_estado = DetalleEstado.objects.filter(alumno=inscripcion.alumno, actual_detalle_e=True).first()
                print "Detalle de estado es: "
                print detalle_estado
                estado_actual = detalle_estado.estado.tipo_estado
                estado_activo = Estado.objects.filter(tipo_estado='Activo').first()
                if estado_actual == 'Inscrito':
                    nuevo_detalle_estado = DetalleEstado.objects.create(fecha_detalle_e=datetime.datetime.now(), actual_detalle_e=True, estado=estado_activo, alumno=inscripcion.alumno)
                    detalle_estado.actual_detalle_e = False;
                    detalle_estado.save()
                    nuevo_detalle_estado.save()
                elif estado_actual == 'Activo':
                    fecha_detalle = detalle_estado.fecha_detalle_e
                    fecha_hoy = datetime.datetime.now()
                    if fecha_detalle.year < fecha_hoy.year or fecha_detalle.month < fecha_hoy.month:
                        nuevo_detalle_estado = DetalleEstado.objects.create(fecha_detalle_e=datetime.datetime.now(), actual_detalle_e=True, estado=estado_activo, alumno=inscripcion.alumno)
                        detalle_estado.actual_detalle_e = False
                        detalle_estado.save()
                        nuevo_detalle_estado.save()
            else:
                asistencia = Asistencia.objects.create(fecha_asistencia=datetime.datetime.now(), asistio=False, inscripcion=inscripcion)
                asistencia.save()
                detalle_estado = DetalleEstado.objects.filter(alumno=inscripcion.alumno, actual_detalle_e=True).first()
                estado_actual = detalle_estado.estado.tipo_estado
                estado_inactivo = Estado.objects.filter(tipo_estado='Inactivo').first()
                print datetime.datetime.now().date() - inscripcion.fecha_inscripcion
                if estado_actual == 'Inscrito':
                    if datetime.datetime.now().date() - inscripcion.fecha_inscripcion >= datetime.timedelta(days=20):
                        inscripcion.actual_inscripcion = False
                        inscripcion.save()
                        detalle_estado.actual_detalle_e = False
                        detalle_estado.save()
                        nuevo_detalle_estado = DetalleEstado.objects.create(fecha_detalle_e=datetime.datetime.now(), actual_detalle_e=True, estado=estado_inactivo, alumno=inscripcion.alumno)
                        nuevo_detalle_estado.save()
                        inscripcion.grupo.horario.cantidad_alumnos = inscripcion.grupo.horario.cantidad_alumnos - 1
                        inscripcion.grupo.horario.save()
                        inscripcion.grupo.alumnosInscritos = inscripcion.grupo.alumnosInscritos - 1
                        inscripcion.grupo.save()

                elif estado_actual == 'Activo':
                    if datetime.datetime.now().date() - inscripcion.asistencia_set.order_by('fecha_asistencia').last().fecha_asistencia >= datetime.timedelta(days=25):
                        inscripcion.actual_inscripcion = False
                        inscripcion.save()
                        detalle_estado.actual_detalle_e = False
                        detalle_estado.save()
                        nuevo_detalle_estado = DetalleEstado.objects.create(fecha_detalle_e=datetime.datetime.now(),actual_detalle_e=True,estado=estado_inactivo)
                        nuevo_detalle_estado.save()
                        inscripcion.grupo.horario.cantidad_alumnos = inscripcion.grupo.horario.cantidad_alumnos - 1
                        inscripcion.grupo.horario.save()
                        inscripcion.grupo.alumnosInscritos = inscripcion.grupo.alumnosInscritos - 1
                        inscripcion.grupo.save()
    else:
        return Http404('Utilizar solo como POST')
    return asistencia_a_clases(request, id_grupo)