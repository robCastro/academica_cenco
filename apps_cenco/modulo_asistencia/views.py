# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseForbidden, HttpResponse, JsonResponse, Http404
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
import locale
#locale.setlocale(locale.LC_TIME, 'es_ES')

from io import BytesIO
from reportlab.pdfgen import canvas
from django.views.generic import View
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from django.conf import settings


import datetime

# Create your views here.
from apps_cenco.db_app.models import DetalleEstado, Grupo, Empleado, Alumno, Inscripcion,Estado
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
    user = User.objects.get(username=request.user)
    prof = Empleado.objects.get(username=user)
    if user.groups.filter(name="Profesor").exists():
        grupo = Grupo.objects.get(codigo=id_grupo, profesor=prof)
        inscripciones = grupo.inscripcion_set.filter(actual_inscripcion=True)
        alumnos = []
        for inscripcion in inscripciones:
            alumnos.append(inscripcion.alumno)
        alumnos_ins=[]
        for alum in alumnos:
             deta=DetalleEstado.objects.get(actual_detalle_e=True,alumno_id=alum.codigo)
             estado=Estado.objects.get(codigo_estado=deta.estado_id)
             if estado.tipo_estado=="Activo" or estado.tipo_estado=="Inscrito":
                alumnos_ins.append(alum)
        for alumno in alumnos_ins:
            alumno.primerTelefono = alumno.telefono_set.first()

        context = {'grupo': grupo,
                   'alumnos':alumnos_ins}
        return render(request, 'modulo_asistencia/profesor_detalle_grupo.html', context)
    else:
        raise Http404('Error, no tiene permiso para esta página')


@login_required
def prof_listado_grupo(request, id_grupo):
    user = User.objects.get(username=request.user)
    prof = Empleado.objects.get(username=user)
    if user.groups.filter(name="Profesor").exists():
        grupo = Grupo.objects.get(codigo=id_grupo, profesor=prof)
        inscripciones = grupo.inscripcion_set.filter(actual_inscripcion=True)
        alumnos = []
        for inscripcion in inscripciones:
            alumnos.append(inscripcion.alumno)
        alumnos_ins=[]
        for alum in alumnos:
             deta=DetalleEstado.objects.get(actual_detalle_e=True,alumno_id=alum.codigo)
             estado=Estado.objects.get(codigo_estado=deta.estado_id)
             if estado.tipo_estado=="Activo" or estado.tipo_estado=="Inscrito":
                alumnos_ins.append(alum)
        alumnos_in=sorted(alumnos_ins,key=lambda alumno: alumno.apellido)

    # Generar el Pdf

        response = HttpResponse(content_type='application/pdf')
        # La clase io.BytesIO permite tratar un array de bytes como un fichero binario, se utiliza como almacenamiento temporal
        buffer = BytesIO()
        # Canvas nos permite hacer el reporte con coordenadas X y Y
        pdf = canvas.Canvas(buffer)
        # Llamo al método cabecera donde están definidos los datos que aparecen en la cabecera del reporte.
        # self.cabecera(pdf)
        # Con show page hacemos un corte de página para pasar a la siguiente

        # def cabecera(self, pdf):
        # Utilizamos el archivo logo_django.png que está guardado en la carpeta media/imagenes
        archivo_imagen = settings.MEDIA_ROOT + 'static/img/encabezado.png'
        # Definimos el tamaño de la imagen a cargar y las coordenadas correspondientes
        pdf.drawImage(archivo_imagen, 40, 750, 120, 90, preserveAspectRatio=True)
        # Establecemos el tamaño de letra en 16 y el tipo de letra Helvetica
        pdf.setFont("Helvetica", 16)
        # Dibujamos una cadena en la ubicación X,Y especificada
        gru= "Grupo"+" "+str(grupo.codigo)+", "+str(grupo.horario)
        pdf.drawString(180, 790,gru )
        pdf.setFont("Helvetica", 14)
        pdf.drawString(180, 745, u"Fecha:____/____/________ ")



        #tabla

        # Creamos una tupla de encabezados para neustra tabla
        encabezados = ('Nombre', 'Firma')
        # Creamos una lista de tuplas que van a contener a las personas
        detalles = [(str(alu.apellido)+" "+str(alu.nombre), " ") for alu in alumnos_in]
        # Establecemos el tamaño de cada una de las columnas de la tabla
        detalle_orden = Table([encabezados] + detalles, colWidths=[9 * cm, 5 * cm, 5 * cm, 5 * cm])
        # Aplicamos estilos a las celdas de la tabla
        detalle_orden.setStyle(TableStyle(
            [
                # La primera fila(encabezados) va a estar centrada
                ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
                # Los bordes de todas las celdas serán de color negro y con un grosor de 1
                ('GRID', (0, 0), (2, alumnos_ins.__len__()+1), 1, colors.black),
                # El tamaño de las letras de cada una de las celdas será de 10
                ('FONTSIZE', (0, 0), (-1, -1), 10),
            ]
        ))
        # Establecemos el tamaño de la hoja que ocupará la tabla
        detalle_orden.wrapOn(pdf, 800, 600)
        # Definimos la coordenada donde se dibujará la tabla
        detalle_orden.drawOn(pdf, 100, 600)





        pdf.showPage()
        pdf.save()
        pdf = buffer.getvalue()
        buffer.close()
        response.write(pdf)
        return response

    else:
        raise Http404('Error, no tiene permiso para esta página')


