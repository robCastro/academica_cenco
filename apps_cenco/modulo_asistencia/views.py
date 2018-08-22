# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponseForbidden, HttpResponse, JsonResponse
from django.shortcuts import render
import locale
locale.setlocale(locale.LC_TIME, 'es_ES')

import datetime

# Create your views here.
from apps_cenco.db_app.models import DetalleEstado
from apps_cenco.modulo_asistencia.forms import IntervaloFechaForm


def ver_reporte_estados(request):
    # estudiantes activos (estado_id =1) en la ultima semana
    form_fecha = IntervaloFechaForm()
    detalle_semanal = DetalleEstado.objects.raw('select 1 as codigo_detalle_e, count(fecha_detalle_e), fecha_detalle_e '
                                                'from db_app_detalleestado '
                                                'where fecha_detalle_e >= (current_date - 8) '
                                                'and estado_id = 1 and actual_detale_e = true '
                                                'group by fecha_detalle_e '
                                                'order by fecha_detalle_e;')
    maxim = 0
    for det in detalle_semanal:
        if det.count > maxim:
            maxim = det.count

    context = {'detalle_semanal': detalle_semanal, 'maximo': maxim+1, 'form': form_fecha}

    return render(request, 'modulo_asistencia/director_ver_estados.html', context)


def filtrar_estado_por_periodo(request):
    # estudiantes activos (estado_id =1) en el ultimo mes
    if request.method == 'POST':
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
                'and estado_id = 1 and actual_detale_e = true '
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

            # context = {'detalle_semanal': datos_por_periodo, 'maximo': maxim + 1}
            return JsonResponse({'datos_filtro': raw_data, 'fechas_filtro': raw_dates, 'maximo': maxim + 1})

        else:
            # When the date is in a range
            form_fecha = IntervaloFechaForm(request.POST)
            if form_fecha.is_valid():
                form = form_fecha.cleaned_data
                fecha1 = form.get('fechaInicial')
                fecha2 = form.get('fechaFinal')
            else:
                return HttpResponse('Fechas Ingresadas Incorrectamente', status=500)

            datos_por_periodo = DetalleEstado.objects.raw(
                'select 1 as codigo_detalle_e, count(fecha_detalle_e), fecha_detalle_e' 
                ' from db_app_detalleestado' 
                ' where fecha_detalle_e >= ' + "'" + str(fecha1) + "'" +
                ' and fecha_detalle_e <= ' + "'" + str(fecha2) + "'" +
                ' and estado_id = 1 and actual_detale_e = true'
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

            context = {'detalle_semanal': datos_por_periodo, 'maximo': maxim+1}

            return JsonResponse({'datos_filtro': raw_data, 'fechas_filtro': raw_dates, 'maximo': maxim + 1})

    else:
        return HttpResponseForbidden('No tiene acceso a esta url')