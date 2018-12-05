# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden, HttpResponse, JsonResponse, Http404

from apps_cenco.db_app.models import Alumno, Encargado, DetallePago, Estado, DetalleEstado, Colegiatura

from datetime import datetime, timedelta

from math import ceil #Redondea hacia arriba

#librerias para pdf
from io import BytesIO
from reportlab.pdfgen import canvas
from django.conf import settings
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter

# Create your views here.

@login_required
def detalle_pago(request, idAlumno, cod_mensaje = 0):
    if cod_mensaje == '1':
        mensaje = "Pago actualizado!"
    elif cod_mensaje == '2':
        mensaje = "Pago eliminado!"
    else:
        mensaje = ""
    print cod_mensaje, mensaje
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
        permitirModPago = (datetime.date(hoy) - ultimoPago.fecha_pago) < timedelta(days=7) and request.user.groups.filter(name="Director").exists() and ultimoPago != None
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
        print mensaje
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
        'permitirModPago' : permitirModPago,
        'mensaje' : mensaje,
    }
    return render(request, 'modulo_pagos/detalle_pagos.html', context)

@login_required
def modificar_pago(request, idAlumno, idPago):
    #idAlumno necesario para extraer alumno y verificar que es el ultimo pago.
    if request.user.groups.filter(name="Director").exists():
        if request.method == "POST":
            hoy = datetime.today()
            try:
                alumno = Alumno.objects.get(pk = idAlumno)
            except Alumno.DoesNotExist:
                return Http404("Alumno no existe")
            try:
                pago = DetallePago.objects.get(pk = idPago)
            except DetallePago.DoesNotExist:
                return Http404("Pago no existe")
            expediente = alumno.expediente_set.get(activo_expediente=True)
            ultimoPago = expediente.colegiatura_set.get(actual_colegiatura=True).detallepago_set.order_by('fecha_pago').last()
            if ultimoPago != None:
                if (datetime.date(hoy) - ultimoPago.fecha_pago) < timedelta(days=7):
                    if pago.codigo_detalle_pago == ultimoPago.codigo_detalle_pago:
                        expediente.fecha_proximo_pago_exp = expediente.fecha_proximo_pago_exp - timedelta(days=(7 * pago.cantidad_semanas))
                        expediente.pagado_hasta = expediente.pagado_hasta - timedelta(days=(7 * pago.cantidad_semanas))
                        nuevaCantidad = request.POST.get('nuevaCantidad')
                        expediente.fecha_proximo_pago_exp = expediente.fecha_proximo_pago_exp + timedelta(days=(7 * int(nuevaCantidad) ))
                        expediente.pagado_hasta = expediente.pagado_hasta + timedelta(days=(7 * int(nuevaCantidad) ))
                        pago.cantidad_semanas = nuevaCantidad
                        pago.save()
                        expediente.save()
                        return redirect('detalle_pagos_mensaje', idAlumno, 1)
                    else:
                        return HttpResponseForbidden("Solo puede modificar el ultimo pago de cada alumno.")
                else:
                    return HttpResponseForbidden("No se puede cambiar el pago del alumno ya que pasaron demasiados dias.")
            else:
                return Http404("Error, en pagos de alumno, verificar que alumno tenga pagos")
        else:
            return redirect('detalle_pagos', idAlumno)
    else:
        return HttpResponseForbidden("No tiene acceso a esta url")

@login_required
def eliminar_pago(request, idAlumno, idPago):
    # idAlumno necesario para extraer alumno y verificar que es el ultimo pago.
    if request.user.groups.filter(name="Director").exists():
        if request.method == "POST":
            hoy = datetime.today()
            try:
                alumno = Alumno.objects.get(pk=idAlumno)
            except Alumno.DoesNotExist:
                return Http404("Alumno no existe")
            try:
                pago = DetallePago.objects.get(pk=idPago)
            except DetallePago.DoesNotExist:
                return Http404("Pago no existe")
            expediente = alumno.expediente_set.get(activo_expediente=True)
            ultimoPago = expediente.colegiatura_set.get(actual_colegiatura=True).detallepago_set.order_by(
                'fecha_pago').last()
            if ultimoPago != None:
                if (datetime.date(hoy) - ultimoPago.fecha_pago) < timedelta(days=7):
                    if pago.codigo_detalle_pago == ultimoPago.codigo_detalle_pago:
                        expediente.fecha_proximo_pago_exp = expediente.fecha_proximo_pago_exp - timedelta(
                            days=(7 * pago.cantidad_semanas))
                        expediente.pagado_hasta = expediente.pagado_hasta - timedelta(days=(7 * pago.cantidad_semanas))
                        pago.delete()
                        expediente.save()
                        return redirect('detalle_pagos_mensaje', idAlumno, 2)
                    else:
                        return HttpResponseForbidden("Solo puede eliminar el ultimo pago de cada alumno.")
                else:
                    return HttpResponseForbidden("No se puede eliminar el pago del alumno ya que pasaron demasiados dias.")
            else:
                return Http404("Error, en pagos de alumno, verificar que alumno tenga pagos")
        else:
            return redirect('detalle_pagos', idAlumno)
    else:
        return HttpResponseForbidden("No tiene acceso a esta url")

@login_required
def ver_cola_impresion(request):
    plantillaBase = "plantillas_base/"
    if request.user.groups.filter(name="Asistente").exists():
        plantillaBase = plantillaBase + "base_asistente.html"
    elif request.user.groups.filter(name="Director").exists():
        plantillaBase = plantillaBase + "base_director.html"
    else:
        return HttpResponseForbidden("No tiene acceso a esta pagina")
    pagos = DetallePago.objects.filter(en_cola=True).order_by('codigo_detalle_pago')
    for pago in pagos:
        pago.nombreAlumno = pago.colegiatura.expediente.alumno.nombre
        pago.tipo = pago.colegiatura.forma_pago
    context = {
        'pagos' : pagos,
        'plantillaBase' : plantillaBase,
    }
    return render(request, 'modulo_pagos/cola_impresion.html', context)

@login_required
def imprimir_cola(request):
    if request.method == "POST":
        if request.user.groups.filter(name="Asistente").exists() or request.user.groups.filter(name="Director").exists():
            marcados = request.POST.get('chxMarcados')
            imprimir = request.POST.get('chxImprimir')
            pagos = DetallePago.objects.filter(en_cola=True)
            codigosRecibos = []
            codigos=""
            print (pagos)
            # Si todos los registros están marcados
            if marcados:
                if imprimir:
                    for pago in pagos:
                        codigos=codigos+str(pago.codigo_detalle_pago)+"s"
                        codigosRecibos.append(pago.codigo_detalle_pago)
                    return redirect('pagos_pdf', codigos=codigos)
                else:
                    for pago in pagos:
                        pago.en_cola = False
                        pago.save()
                    print ("Fin de sacado de cola de TODOS")
            else:
                if imprimir:
                    for pago in pagos:
                        if request.POST.get(str(pago.codigo_detalle_pago)):
                            codigosRecibos.append(pago.codigo_detalle_pago)
                            codigos = codigos + str(pago.codigo_detalle_pago) + "s"
                    return redirect('pagos_pdf', codigos=codigos)
                else:
                    for pago in pagos:
                        if request.POST.get(str(pago.codigo_detalle_pago)):
                            pago.en_cola = False
                            pago.save()
                    print ("Fin de sacado de cola de ALGUNOS")
            return redirect('cola_pagos')
        else:
            return HttpResponseForbidden("No tiene acceso a esta pagina")
    else:
        return redirect('cola_pagos')


@login_required
def ver_alumnos(request):
    if request.user.groups.filter(name="Director").exists():
        estadoActivo = Estado.objects.get(tipo_estado="Activo")
        detallesEstadosActivos = estadoActivo.detalleestado_set.filter(actual_detalle_e=True)
        alumnos = Alumno.objects.filter(detalleestado__in=detallesEstadosActivos).order_by('codigo')
        context = {
            'alumnos' : alumnos,
        }
        return render(request,'modulo_pagos/director_verAlumnos.html', context)
    else:
        return HttpResponseForbidden("No tiene acceso a esta pagina")


def pdf_pagos(request,codigos):
    if request.user.groups.filter(name="Director").exists() or request.user.groups.filter(name="Asistente").exists():

        codig = codigos.split('s')
        codig.pop(codig.__len__() - 1)






        # Indicamos el tipo de contenido a devolver, en este caso un pdf
        response = HttpResponse(content_type='application/pdf')
        # La clase io.BytesIO permite tratar un array de bytes como un fichero binario, se utiliza como almacenamiento temporal
        buffer = BytesIO()
        # Canvas nos permite hacer el reporte con coordenadas X y Y
        pdf = canvas.Canvas(buffer, pagesize=letter)
        # Llamo al método cabecera donde están definidos los datos que aparecen en la cabecera del reporte.
        # self.cabecera(pdf)
        # Con show page hacemos un corte de página para pasar a la siguiente

        # def cabecera(self, pdf):
        # Utilizamos el archivo logo_django.png que está guardado en la carpeta media/imagenes
        archivo_imagen = settings.MEDIA_ROOT + 'static/img/encabezado.png'
        # Definimos el tamaño de la imagen a cargar y las coordenadas correspondientes
        pdf.drawImage(archivo_imagen, 40, 705, 120, 90, preserveAspectRatio=True)
        # Establecemos el tamaño de letra en 16 y el tipo de letra Helvetica
        pdf.setFont("Helvetica", 16)
        # Dibujamos una cadena en la ubicación X,Y especificada
        pdf.drawString(180, 745, u"CENTRO DE ENSEÑANZA EN COMPUTACIÓN")
        pdf.setFont("Helvetica", 14)
        pagos=[]
        colegiatura=[]
        for cod in codig:
            pagos.append(DetallePago.objects.get(codigo_detalle_pago=int(cod)))


        x = 1
        n = 0
        for pag in pagos:
            pag.en_cola = False
            pag.save()
            t = 1
            n+=1
            if x == 1:
                archivo_imagen = settings.MEDIA_ROOT + 'static/img/encabezado.png'
                # Definimos el tamaño de la imagen a cargar y las coordenadas correspondientes
                pdf.drawImage(archivo_imagen, 40, 705, 120, 90, preserveAspectRatio=True)
                # Establecemos el tamaño de letra en 16 y el tipo de letra Helvetica
                pdf.setFont("Helvetica", 16)
                # Dibujamos una cadena en la ubicación X,Y especificada
                pdf.drawString(180, 745, u"CENTRO DE ENSEÑANZA EN COMPUTACIÓN")
                pdf.setFont("Helvetica", 14)
                pdf.drawString(75, 695, "Fecha de pago: " + str(pag.fecha_pago.strftime("%d/%m/%Y")))
                pdf.drawString(75, 675, "Codigo de pago: " + str(pag.codigo_detalle_pago))
                pdf.drawString(75, 655, "Alumno: " + str(pag.colegiatura.expediente.alumno.nombre)+" "+str(pag.colegiatura.expediente.alumno.apellido))
                pdf.drawString(75, 635, "Tipo de Pago: " + str(pag.colegiatura.forma_pago))
                col=pag.colegiatura.cuota_semanal
                pdf.drawString(75, 615, "Colegiatura: " + str(col))
                can=pag.cantidad_semanas
                pdf.drawString(75, 595, "Cantidad: " + str(can))

                tot=col*can
                monto=pag.monto_pago
                if monto-tot==0:
                    des="No aplica"

                else:
                    des=str(monto-tot)
                pdf.drawString(75, 575, "Descuento: " + des)
                pdf.drawString(75, 555, "Monto: " + str(monto))
                t=0
            if x==2:
                k=380
                archivo_imagen = settings.MEDIA_ROOT + 'static/img/encabezado.png'
                # Definimos el tamaño de la imagen a cargar y las coordenadas correspondientes
                pdf.drawImage(archivo_imagen, 40, 325, 120, 90, preserveAspectRatio=True)
                # Establecemos el tamaño de letra en 16 y el tipo de letra Helvetica
                pdf.setFont("Helvetica", 16)
                # Dibujamos una cadena en la ubicación X,Y especificada
                pdf.drawString(180, 365, u"CENTRO DE ENSEÑANZA EN COMPUTACIÓN")
                pdf.setFont("Helvetica", 14)
                pdf.drawString(75, 695-k, "Fecha de pago: " + str(pag.fecha_pago.strftime("%d/%m/%Y")))
                pdf.drawString(75, 675-k, "Codigo de pago: " + str(pag.codigo_detalle_pago))
                pdf.drawString(75, 655-k, "Alumno: " + str(pag.colegiatura.expediente.alumno.nombre) + " " + str(
                    pag.colegiatura.expediente.alumno.apellido))
                pdf.drawString(75, 635-k, "Tipo de Pago: " + str(pag.colegiatura.forma_pago))
                if pag.colegiatura.forma_pago == "mensual":
                    col = pag.colegiatura.cuota_semanal * 4
                else:
                    col = pag.colegiatura.cuota_semanal

                pdf.drawString(75, 615-k, "Colegiatura: " + str(col))
                can = pag.cantidad_semanas
                pdf.drawString(75, 595-k, "Cantidad: " + str(can))

                tot = col * can
                monto = pag.monto_pago
                if monto - tot == 0:
                    des = "No aplica"

                else:
                    des = str(monto - tot)
                pdf.drawString(75, 575-k, "Descuento: " + des)
                pdf.drawString(75, 555-k, "Monto: " + str(monto))
                if n<pagos.__len__():
                    pdf.showPage()
                x = 1
            if t==0:
                x=2



        pdf.showPage()
        pdf.save()
        pdf = buffer.getvalue()
        buffer.close()
        response.write(pdf)
        return response

    else:
        return HttpResponseForbidden("No tiene acceso a esta pagina")


def pdf_recibo(request,codigo):
    if request.user.groups.filter(name="Director").exists() or request.user.groups.filter(name="Asistente").exists() or request.user.groups.filter(name="Alumno").exists() or request.user.groups.filter(name="Encargado").exists():

        # Indicamos el tipo de contenido a devolver, en este caso un pdf
        response = HttpResponse(content_type='application/pdf')
        # La clase io.BytesIO permite tratar un array de bytes como un fichero binario, se utiliza como almacenamiento temporal
        buffer = BytesIO()
        # Canvas nos permite hacer el reporte con coordenadas X y Y
        pdf = canvas.Canvas(buffer, pagesize=letter)
        # Llamo al método cabecera donde están definidos los datos que aparecen en la cabecera del reporte.
        # self.cabecera(pdf)
        # Con show page hacemos un corte de página para pasar a la siguiente

        # def cabecera(self, pdf):
        # Utilizamos el archivo logo_django.png que está guardado en la carpeta media/imagenes
        archivo_imagen = settings.MEDIA_ROOT + 'static/img/encabezado.png'
        # Definimos el tamaño de la imagen a cargar y las coordenadas correspondientes
        pdf.drawImage(archivo_imagen, 40, 705, 120, 90, preserveAspectRatio=True)
        # Establecemos el tamaño de letra en 16 y el tipo de letra Helvetica
        pdf.setFont("Helvetica", 16)
        # Dibujamos una cadena en la ubicación X,Y especificada
        pdf.drawString(180, 745, u"CENTRO DE ENSEÑANZA EN COMPUTACIÓN")
        pdf.setFont("Helvetica", 14)
        detalle= DetallePago.objects.get(codigo_detalle_pago=codigo)

        archivo_imagen = settings.MEDIA_ROOT + 'static/img/encabezado.png'
        # Definimos el tamaño de la imagen a cargar y las coordenadas correspondientes
        pdf.drawImage(archivo_imagen, 40, 705, 120, 90, preserveAspectRatio=True)
        # Establecemos el tamaño de letra en 16 y el tipo de letra Helvetica
        pdf.setFont("Helvetica", 16)
        # Dibujamos una cadena en la ubicación X,Y especificada
        pdf.drawString(180, 745, u"CENTRO DE ENSEÑANZA EN COMPUTACIÓN")
        pdf.setFont("Helvetica", 14)
        pdf.drawString(75, 695, "Fecha de pago: " + str(detalle.fecha_pago.strftime("%d/%m/%Y")))
        pdf.drawString(75, 675, "Codigo de pago: " + str(detalle.codigo_detalle_pago))
        pdf.drawString(75, 655, "Alumno: " + str(detalle.colegiatura.expediente.alumno.nombre)+" "+str(detalle.colegiatura.expediente.alumno.apellido))
        pdf.drawString(75, 635, "Tipo de Pago: " + str(detalle.colegiatura.forma_pago))
        col=detalle.colegiatura.cuota_semanal
        pdf.drawString(75, 615, "Colegiatura: " + str(col))
        can=detalle.cantidad_semanas
        pdf.drawString(75, 595, "Cantidad: " + str(can))

        tot=col*can
        monto=detalle.monto_pago
        if (monto-tot)==0:
            des="No aplica"
        else:
            des=str(monto-tot)
        pdf.drawString(75, 575, "Descuento: " + des)
        pdf.drawString(75, 555, "Monto: " + str(monto))
        t=0



        pdf.showPage()
        pdf.save()
        pdf = buffer.getvalue()
        buffer.close()
        response.write(pdf)
        return response
    else:
        return HttpResponseForbidden("No tiene acceso a esta pagina")
