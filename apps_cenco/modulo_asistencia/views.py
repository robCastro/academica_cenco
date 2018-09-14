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
from apps_cenco.db_app.models import DetalleEstado, Grupo, Empleado, Alumno, Inscripcion
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
                'and estado_id = ' + tipo + ' and actual_detalle_e = true '
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
                ' and estado_id = ' + tipo + ' and actual_detalle_e = true'
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




