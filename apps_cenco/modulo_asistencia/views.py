# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
import datetime

# Create your views here.
from apps_cenco.db_app.models import DetalleEstado


def ver_reporte_estados(request):
    # estudiantes activos (estado_id =1) en la ultima semana
    detalle_semanal = DetalleEstado.objects.raw('select 1 as codigo_detalle_e, count(fecha_detalle_e), fecha_detalle_e '
                                                'from db_app_detalleestado '
                                                'where fecha_detalle_e >= (current_date - 8) '
                                                'and estado_id = 1 and actual_detale_e = true '
                                                'group by fecha_detalle_e '
                                                'order by fecha_detalle_e;')

    return render(request, 'modulo_asistencia/director_ver_estados.html', {'detalle_semanal': detalle_semanal})
