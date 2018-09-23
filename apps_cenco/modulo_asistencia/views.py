# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import calendar

from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseForbidden, HttpResponse, JsonResponse, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Avg, Min, Max
import locale, os
#if os.name != 'nt':
#    locale.setlocale(locale.LC_TIME, 'es_ES')

import datetime

# Create your views here.
from apps_cenco.db_app.models import DetalleEstado, Grupo, Empleado, Alumno, Inscripcion, Asistencia, Estado, MetricaEstado
from apps_cenco.modulo_asistencia.forms import IntervaloFechaForm, FechaAsistenciaForm

@login_required
def ver_reporte_estados(request):
    if request.user.groups.filter(name="Director").exists():
        form_fecha = IntervaloFechaForm()

        detalle_semanal = DetalleEstado.objects.raw(
            "select 1 as codigo_detalle_e, p.fechas::date as fecha_detalle_e, coalesce(s.count, 0) as count "
            "from generate_series((current_date-7)::date, current_date::date, '1 day'::interval) as p(fechas)"
            " left outer join "
            "(select 1 as codigo_detalle_e, count(fecha_detalle_e) as count, fecha_detalle_e "
            "from db_app_detalleestado "
            "where fecha_detalle_e >= (current_date - 7) "
            "and estado_id = 1"
            "group by fecha_detalle_e "
            "order by fecha_detalle_e) s on p.fechas = s.fecha_detalle_e")
        maxim = 0
        for det in detalle_semanal:
            if det.count > maxim:
                maxim = det.count

        context = {'detalle_semanal': detalle_semanal, 'maximo': maxim+1, 'form': form_fecha}

        return render(request, 'modulo_asistencia/director_ver_estados.html', context)
    else:
        return HttpResponseForbidden('No tiene acceso a esta url')

@login_required
def filtrar_estado_por_periodo(request):
    if request.user.groups.filter(name="Director").exists():
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
                    if datetime.datetime.now().month > 6:
                        intervalo_actual = 'extract(month from current_date)::integer-6, ' \
                                           'extract(month from current_date)::integer'
                        intervalo_pasado = '1,0'
                    else:
                        mes_actual = datetime.datetime.now().month
                        mes_anterior = 6 - mes_actual
                        intervalo_actual = '1, '+str(mes_actual)
                        intervalo_pasado = '13-'+str(mes_anterior)+', 12'
                elif request.POST.get('opcion') == 'anual':
                    seleccion = '365'
                    intervalo_actual = '1, extract(month from current_date)::integer'
                    intervalo_pasado = 'extract(month from current_date)::integer, 12'
                else:
                    seleccion = '7'

                opt = request.POST.get('opcion')
                if opt == 'semestral' or opt == 'anual':
                    datos_por_periodo = DetalleEstado.objects.raw(
                        '(select 1 as codigo_detalle_e, (extract(year from current_date) - 1) as anio, coalesce(s.mes, p.correlativo) as mes, '
                        'coalesce(s.cuenta, 0) as contador '
                        'from generate_series('+intervalo_pasado+') as p(correlativo) '
                        'left outer join '
                        '(select  1 as codigo_detalle_e, count(fecha_detalle_e) as cuenta, '
                        'extract(month from fecha_detalle_e) as mes from db_app_detalleestado '
                        'where extract(year from fecha_detalle_e) = extract(year from current_date) - 1 '
                        'and estado_id = 1 group by extract(month from fecha_detalle_e) '
                        'order by extract(month from fecha_detalle_e)) s on p.correlativo = s.mes) '
                        'union '
                        '(select 1 as codigo_detalle_e, (extract(year from current_date)) as codigo, coalesce(s.mes, p.correlativo) as mes, '
                        'coalesce(s.cuenta, 0) as contador '
                        'from generate_series('+intervalo_actual+') as p(correlativo) '
                        'left outer join  '
                        '(select  1 as codigo_detalle_e, count(fecha_detalle_e) as cuenta, '
                        'extract(month from fecha_detalle_e) as mes from db_app_detalleestado '
                        'where extract(year from fecha_detalle_e) = extract(year from current_date) '
                        'and estado_id = '+tipo+' group by extract(month from fecha_detalle_e) '
                        'order by extract(month from fecha_detalle_e)) s on p.correlativo = s.mes) '
                        'order by anio, mes;')
                    maxim = 0
                    raw_data= []
                    raw_dates = []
                    for det in datos_por_periodo:
                        raw_data.append(det.contador)
                        raw_dates.append(calendar.month_name[int(det.mes)]+'/'+str(int(det.anio)))
                        if det.contador > maxim:
                            maxim = det.contador
                else:
                    datos_por_periodo = DetalleEstado.objects.raw(
                        "select 1 as codigo_detalle_e, p.fechas::date as fecha_detalle_e, coalesce(s.count, 0) as count "
                        "from generate_series((current_date-"+seleccion+")::date, current_date::date, '1 day'::interval) as p(fechas)"
                        " left outer join "
                        "(select 1 as codigo_detalle_e, count(fecha_detalle_e) as count, fecha_detalle_e "
                        "from db_app_detalleestado "
                        "where fecha_detalle_e >= (current_date - "+seleccion+") "
                        "and estado_id = "+tipo+
                        "group by fecha_detalle_e "
                        "order by fecha_detalle_e) s on p.fechas = s.fecha_detalle_e")

                    aux = {}
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
                    if (fecha2 - fecha1).days > 40:
                        return HttpResponse('Error: Intervalo demasiado amplio. Si desea ver registros anteriores,'
                                            ' puede filtrar por semestre o reducir el intervalo para una vista detallada.',
                                            status=500)
                else:
                    return HttpResponse('Error: Las fechas no son validas', status=500)

                datos_por_periodo = DetalleEstado.objects.raw(
                    "select 1 as codigo_detalle_e, p.fechas::date as fecha_detalle_e, coalesce(s.count, 0) as count "
                    "from generate_series((" + "'" + str(fecha1) + "'" + ")::date, "
                    "'"+str(fecha2)+"'"+"::date, '1 day'::interval) as p(fechas)"
                    " left outer join "
                    "(select 1 as codigo_detalle_e, count(fecha_detalle_e) as count, fecha_detalle_e "
                    "from db_app_detalleestado "
                    "where estado_id = " + tipo + 
                    "group by fecha_detalle_e "
                    "order by fecha_detalle_e) s on p.fechas = s.fecha_detalle_e")

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

@login_required
def ver_metricas_estado(request):
    if request.user.groups.filter(name="Director").exists():
        insertarFechasMetricasEstado()
        fechaHoy = datetime.datetime.today()
        if request.method == 'GET':         #Para GET siempre será trimestre
            if fechaHoy.month == 1:
                fechaMin = datetime.datetime(fechaHoy.year - 1, 11, 1)
            elif fechaHoy.month == 2:
                fechaMin = datetime.datetime(fechaHoy.year - 1, 12, 1)
            else:
                fechaMin = datetime.datetime(fechaHoy.year, fechaHoy.month - 2, 1)
            fechaMin = datetime.datetime(2018, 1, 1)
            estadoActivo = Estado.objects.filter(tipo_estado="Inscrito").first()
            metricasActivos = MetricaEstado.objects.filter(fecha_metrica__range=(fechaMin, fechaHoy)).filter(
                estado=estadoActivo).order_by('fecha_metrica')
            promedio = metricasActivos.aggregate(Avg('cantidad')).get('cantidad__avg')
            minimo = metricasActivos.aggregate(Min('cantidad')).get('cantidad__min')
            maximo = metricasActivos.aggregate(Max('cantidad')).get('cantidad__max')
            fechas = []
            cantidades = []
            color = '#008000'
            for metricaActivo in metricasActivos:
                fechas.append(metricaActivo.fecha_metrica)
                cantidades.append(metricaActivo.cantidad)
            context = {
                'fechas' : fechas,
                'cantidades' : cantidades,
                'promedio' : promedio,
                'minimo' : minimo,
                'maximo' : maximo,
                'color' : color,
                'etiqueta' : 'Activos',
            }
            return render(request, 'modulo_asistencia/director_ver_metrica_estados.html', context)
    else:
        return HttpResponseForbidden('No tiene acceso a esta url')


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
        insertarFechasMetricasEstado()
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
        try:
            grupo = Grupo.objects.get(pk = id_grupo)
        except Grupo.DoesNotExist:
            return Http404('Grupo no existe')
        inscripciones = grupo.inscripcion_set.filter(actual_inscripcion=True)
        fecha_hoy = datetime.datetime.now()
        fecha_aux = datetime.datetime(fecha_hoy.year, fecha_hoy.month, 1)

        estado_activo = Estado.objects.filter(tipo_estado='Activo').first()
        estado_inactivo = Estado.objects.filter(tipo_estado='Inactivo').first()
        estado_presentados = Estado.objects.filter(tipo_estado='Presentados').first()
        estado_no_presentados = Estado.objects.filter(tipo_estado='No Presentados').first()
        estado_retenidos = Estado.objects.filter(tipo_estado='Retenidos').first()
        estado_retirados = Estado.objects.filter(tipo_estado='Retirados').first()

        metrica_estado_activo = MetricaEstado.objects.filter(fecha_metrica=fecha_aux, estado=estado_activo).first()
        metrica_estado_inactivo = MetricaEstado.objects.filter(fecha_metrica=fecha_aux, estado=estado_inactivo).first()
        metrica_estado_presentados = MetricaEstado.objects.filter(fecha_metrica=fecha_aux, estado=estado_presentados).first()
        metrica_estado_no_presentados = MetricaEstado.objects.filter(fecha_metrica=fecha_aux, estado=estado_no_presentados).first()
        metrica_estado_retenidos = MetricaEstado.objects.filter(fecha_metrica=fecha_aux, estado=estado_retenidos).first()
        metrica_estado_retirados = MetricaEstado.objects.filter(fecha_metrica=fecha_aux, estado=estado_retirados).first()

        for inscripcion in inscripciones:
            if request.POST.get(str(inscripcion.alumno.codigo)):
                asistencia = Asistencia.objects.create(fecha_asistencia=fecha_hoy, asistio=True, inscripcion = inscripcion)
                asistencia.save()
                detalle_estado = DetalleEstado.objects.filter(alumno=inscripcion.alumno, actual_detalle_e=True).first()
                estado_actual = detalle_estado.estado.tipo_estado
                if estado_actual == 'Inscrito':
                    nuevo_detalle_estado = DetalleEstado.objects.create(fecha_detalle_e=fecha_hoy, actual_detalle_e=True, estado=estado_activo, alumno=inscripcion.alumno)
                    detalle_estado.actual_detalle_e = False;
                    detalle_estado.save()
                    nuevo_detalle_estado.save()
                    metrica_estado_presentados.cantidad = metrica_estado_presentados.cantidad + 1
                    metrica_estado_presentados.save()
                    metrica_estado_activo.cantidad = metrica_estado_activo.cantidad + 1
                    metrica_estado_activo.save()
                elif estado_actual == 'Activo':
                    fecha_detalle = detalle_estado.fecha_detalle_e
                    if fecha_detalle.year < fecha_hoy.year or fecha_detalle.month < fecha_hoy.month:
                        nuevo_detalle_estado = DetalleEstado.objects.create(fecha_detalle_e=fecha_hoy, actual_detalle_e=True, estado=estado_activo, alumno=inscripcion.alumno)
                        detalle_estado.actual_detalle_e = False
                        detalle_estado.save()
                        nuevo_detalle_estado.save()
                        metrica_estado_retenidos.cantidad = metrica_estado_retenidos.cantidad + 1
                        metrica_estado_retenidos.save()
                        metrica_estado_activo.cantidad = metrica_estado_activo.cantidad + 1
                        metrica_estado_activo.save()
            else:
                asistencia = Asistencia.objects.create(fecha_asistencia=fecha_hoy, asistio=False, inscripcion=inscripcion)
                asistencia.save()
                detalle_estado = DetalleEstado.objects.filter(alumno=inscripcion.alumno, actual_detalle_e=True).first()
                estado_actual = detalle_estado.estado.tipo_estado
                if estado_actual == 'Inscrito':
                    if fecha_hoy.date() - inscripcion.fecha_inscripcion >= datetime.timedelta(days=20):
                        inscripcion.actual_inscripcion = False
                        inscripcion.save()
                        detalle_estado.actual_detalle_e = False
                        detalle_estado.save()
                        nuevo_detalle_estado = DetalleEstado.objects.create(fecha_detalle_e=fecha_hoy, actual_detalle_e=True, estado=estado_inactivo, alumno=inscripcion.alumno)
                        nuevo_detalle_estado.save()

                        # if fecha_hoy.day >= 21:
                        #     metrica_estado_no_presentados.cantidad = metrica_estado_no_presentados.cantidad + 1
                        #     metrica_estado_no_presentados.save()
                        #     metrica_estado_inactivo.cantidad = metrica_estado_inactivo.cantidad + 1
                        #     metrica_estado_inactivo.save()
                        # else:                       #Caso especial
                        fecha_caso_especial = datetime.datetime(inscripcion.fecha_inscripcion.year, inscripcion.fecha_inscripcion.month, 1)
                        metrica_estado_no_presentados_especial = MetricaEstado.objects.filter(fecha_metrica=fecha_caso_especial, estado=estado_no_presentados).first()
                        metrica_estado_no_presentados_especial.cantidad = metrica_estado_no_presentados_especial.cantidad + 1
                        metrica_estado_no_presentados_especial.save()
                        metrica_estado_inactivo_especial = MetricaEstado.objects.filter(fecha_metrica=fecha_caso_especial, estado=estado_inactivo).first()
                        metrica_estado_inactivo_especial.cantidad = metrica_estado_inactivo_especial.cantidad + 1
                        metrica_estado_inactivo_especial.save()

                        inscripcion.grupo.horario.cantidad_alumnos = inscripcion.grupo.horario.cantidad_alumnos - 1
                        inscripcion.grupo.horario.save()
                        inscripcion.grupo.alumnosInscritos = inscripcion.grupo.alumnosInscritos - 1
                        inscripcion.grupo.save()
                elif estado_actual == 'Activo':
                    if fecha_hoy.date() - inscripcion.asistencia_set.filter(asistio=True).order_by('fecha_asistencia').last().fecha_asistencia >= datetime.timedelta(days=25):
                        inscripcion.actual_inscripcion = False
                        inscripcion.save()
                        detalle_estado.actual_detalle_e = False
                        detalle_estado.save()
                        nuevo_detalle_estado = DetalleEstado.objects.create(fecha_detalle_e=fecha_hoy,actual_detalle_e=True,estado=estado_inactivo, alumno=inscripcion.alumno)
                        nuevo_detalle_estado.save()

                        # if fecha_hoy.day >= 26:
                        #     metrica_estado_retirados.cantidad = metrica_estado_retirados.cantidad + 1
                        #     metrica_estado_retirados.save()
                        #     metrica_estado_inactivo.cantidad = metrica_estado_inactivo.cantidad + 1
                        #     metrica_estado_inactivo.save()
                        #     metrica_estado_activo.cantidad = metrica_estado_activo.cantidad - 1
                        #     metrica_estado_activo.save()
                        # else:
                        fecha_caso_especial = Asistencia.objects.filter(inscripcion=inscripcion, asistio=True).order_by('fecha_asistencia').last().fecha_asistencia
                        fecha_auxiliar = datetime.datetime(fecha_caso_especial.year, fecha_caso_especial.month, 1)
                        metrica_estado_retirados_especial = MetricaEstado.objects.filter(fecha_metrica=fecha_auxiliar, estado=estado_retirados).first()
                        metrica_estado_inactivo_especial = MetricaEstado.objects.filter(fecha_metrica=fecha_auxiliar, estado=estado_inactivo).first()
                        metrica_estado_activo_especial = MetricaEstado.objects.filter(fecha_metrica=fecha_auxiliar, estado=estado_activo).first()
                        metrica_estado_retirados_especial.cantidad = metrica_estado_retirados_especial.cantidad + 1
                        metrica_estado_retirados_especial.save()
                        metrica_estado_inactivo_especial.cantidad = metrica_estado_inactivo_especial.cantidad + 1
                        metrica_estado_inactivo_especial.save()
                        metrica_estado_activo_especial.cantidad = metrica_estado_activo_especial.cantidad - 1
                        metrica_estado_activo_especial.save()

                        inscripcion.grupo.horario.cantidad_alumnos = inscripcion.grupo.horario.cantidad_alumnos - 1
                        inscripcion.grupo.horario.save()
                        inscripcion.grupo.alumnosInscritos = inscripcion.grupo.alumnosInscritos - 1
                        inscripcion.grupo.save()
    else:
        return redirect('asistencia_grupo', id_grupo)
    return asistencia_a_clases(request, id_grupo)

def insertarFechasMetricasEstado():
    #fecha_hoy = datetime.datetime.now()
    fecha_hoy = datetime.datetime.now()
    if MetricaEstado.objects.count() != 0:
        fecha_vieja = MetricaEstado.objects.all().order_by('fecha_metrica').last().fecha_metrica
        mes = fecha_vieja.month + 1
        anio = fecha_vieja.year
        while (anio < fecha_hoy.year or mes <= fecha_hoy.month):
            if mes == 13:
                mes = 1
                anio = anio + 1
            fecha_intermedia = datetime.datetime(anio, mes, 1)
            estados = Estado.objects.all()
            for estado in estados:
                metrica_estado = MetricaEstado.objects.create(fecha_metrica=fecha_intermedia, cantidad = 0, estado=estado)
                metrica_estado.save()
            mes = mes + 1
    else :
        fecha_intermedia = datetime.datetime(fecha_hoy.year, fecha_hoy.month, 1)
        estados = Estado.objects.all()
        for estado in estados:
            metrica_estado = MetricaEstado.objects.create(fecha_metrica=fecha_intermedia, cantidad=0, estado=estado)
            metrica_estado.save()

# def fechas():
#     fecha_hoy = datetime.datetime(2018, 12, 1)      #Simulando fecha actual
#     fecha_vieja = datetime.datetime(2018, 12, 1)    #Simulando ultima fecha sacada de BD
#     mes = fecha_vieja.month + 1
#     anio = fecha_vieja.year
#     while (anio < fecha_hoy.year or mes <= fecha_hoy.month):
#         if mes == 13:
#             mes = 1
#             anio = anio + 1
#         fecha_intermedia = datetime.datetime(anio, mes, 1)
#         print str(fecha_intermedia)                 # En cada print recorrer estados y crear un registro en cero
#         mes = mes + 1
