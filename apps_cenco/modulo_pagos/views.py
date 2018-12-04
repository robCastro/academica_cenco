# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden, HttpResponse, JsonResponse, Http404
from django.core.serializers import serialize  #Para convertir QuerySet a JSON

from apps_cenco.db_app.models import Alumno, Encargado, DetallePago, Estado, Grupo, Colegiatura

from datetime import datetime, timedelta

from math import ceil #Redondea hacia arriba
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
            print (pagos)
            # Si todos los registros están marcados
            if marcados:
                if imprimir:
                    for pago in pagos:
                        codigosRecibos.append(pago.codigo_detalle_pago)
                    print ("Llamada a la funcion de impresion aqui, todos los pagos")
                    print (codigosRecibos)
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
                    print ("Llamada a la funcion de impresion aqui, solo algunos pagos")
                    print (codigosRecibos)
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

@login_required
def ingresar_pago(request):
    if request.method == "POST":
        #Seccion para guardar pagos
        codColegiatura = request.POST.get('codColegiatura')
        if codColegiatura != None:
            try:
                colegiatura = Colegiatura.objects.get(pk = codColegiatura)
            except Colegiatura.DoesNotExist:
                return HttpResponse('Error en ingreso de pago, refrescar pagina', status=500)
            strCantidadSemanas = request.POST.get('cantidadSemanas')
            try:
                cantidadSemanas = int(strCantidadSemanas, 10)
            except ValueError:
                return HttpResponse('Error en cantidad de Semanas, verificar', status=500)
            if cantidadSemanas > 0:
                aplicarDescuento = request.POST.get('aplicarDescuento')
                pagoAux = cantidadSemanas * float(colegiatura.cuota_semanal)
                print aplicarDescuento, cantidadSemanas, colegiatura.cuota_semanal, pagoAux
                if aplicarDescuento == "true":
                    pagoAux = pagoAux * 0.9
                    print "Aplicando descuento ", pagoAux

                detallePago = DetallePago.objects.create(
                    fecha_pago = datetime.today(),
                    monto_pago = pagoAux,
                    cancelado = True,
                    cantidad_semanas = cantidadSemanas,
                    en_cola = True,
                    colegiatura = colegiatura
                )
                detallePago.save()
                expediente = colegiatura.expediente
                expediente.fecha_proximo_pago_exp = expediente.fecha_proximo_pago_exp + timedelta(days = 7 * cantidadSemanas)
                expediente.pagado_hasta = expediente.pagado_hasta + timedelta(days = 7 * cantidadSemanas)
                expediente.save()
                return HttpResponse("Pago guardado correctamente", status=200)
            else:
                return HttpResponse('Error en cantidad de Semanas, verificar', status=500)
        else:
            return HttpResponse('Error en toma de colegiatura, refrescar pagina', status=500)
    else:
        #Seccion para renderizar pagina
        plantillaBase = "plantillas_base/"
        if request.user.groups.filter(name="Director").exists():
            plantillaBase = plantillaBase + "base_director.html"
        elif request.user.groups.filter(name="Asistente").exists():
            plantillaBase = plantillaBase + "base_asistente.html"
        else:
            return HttpResponseForbidden("No tiene acceso a esta url")
        hoy = datetime.today()
        grupos = Grupo.objects.filter(activo_grupo=True).order_by('codigo')
        alumnos = Alumno.objects.filter(inscripcion__in=grupos.first().inscripcion_set.filter(actual_inscripcion=True)).order_by('codigo')
        codigosAlumnos = []
        codigosColegiaturas = []
        nombresAlumnos = []
        apellidosAlumnos = []
        tiposPago = []
        cuotas = []
        descuentos = []
        for alumno in alumnos:
            codigosAlumnos.append(alumno.codigo)
            nombresAlumnos.append(alumno.nombre)
            apellidosAlumnos.append(alumno.apellido)
            expediente = alumno.expediente_set.get(activo_expediente=True)
            colegiatura = expediente.colegiatura_set.get(actual_colegiatura=True)
            codigosColegiaturas.append(colegiatura.codigo_colegiatura)
            tiposPago.append(colegiatura.forma_pago)
            cuotas.append(colegiatura.cuota_semanal)
            aplicarDescuento = expediente.fecha_proximo_pago_exp + timedelta(days=5) >= datetime.date(hoy)
            descuentos.append(aplicarDescuento)
            #descuentos.append((expediente.fecha_proximo_pago_exp - datetime.date(hoy)) > timedelta(days=5))
        alumnoAux = alumnos.first()
        expediente = alumnoAux.expediente_set.get(activo_expediente=True)
        aplicaDescuento = (expediente.fecha_proximo_pago_exp - datetime.date(hoy)) > timedelta(days = 5)
        colegiatura = expediente.colegiatura_set.get(actual_colegiatura=True)
        context = {
            'grupos' : grupos,
            'alumnos' : alumnos,
            'plantillaBase' : plantillaBase,
            'alumnoAux' : alumnoAux,
            'aplicaDescuento' : aplicaDescuento,
            'colegiatura' : colegiatura,
            'codigosAlumnos': codigosAlumnos,
            'nombresAlumnos': nombresAlumnos,
            'apellidosAlumnos': apellidosAlumnos,
            'codigosColegiaturas': codigosColegiaturas,
            'tiposPago': tiposPago,
            'cuotas': cuotas,
            'descuentos': descuentos,
        }
        return render(request, 'modulo_pagos/ingresar_pago.html', context)

def filtrarAlumnos(request):
    if request.user.groups.filter(name="Asistente").exists() or request.user.groups.filter(name="Director").exists():
        codGrupo = request.GET.get('cbxGrupos')
        if codGrupo:
            try:
                grupo = Grupo.objects.get(pk = codGrupo)
            except Grupo.DoesNotExist:
                return HttpResponse('Grupo no existe, refresque la pagina', status=500)
            inscripciones = grupo.inscripcion_set.filter(actual_inscripcion=True)
            alumnos = Alumno.objects.filter(inscripcion__in=inscripciones)
            if alumnos.count() > 0:
                hoy = datetime.today()
                codigosAlumnos = []
                codigosColegiaturas = []
                nombresAlumnos = []
                apellidosAlumnos = []
                tiposPago = []
                cuotas = []
                descuentos = []
                for alumno in alumnos:
                    codigosAlumnos.append(alumno.codigo)
                    nombresAlumnos.append(alumno.nombre)
                    apellidosAlumnos.append(alumno.apellido)
                    expediente = alumno.expediente_set.get(activo_expediente=True)
                    colegiatura = expediente.colegiatura_set.get(actual_colegiatura=True)
                    codigosColegiaturas.append(colegiatura.codigo_colegiatura)
                    tiposPago.append(colegiatura.forma_pago)
                    cuotas.append(colegiatura.cuota_semanal)
                    aplicarDescuento = expediente.fecha_proximo_pago_exp + timedelta(days=5) >= datetime.date(hoy)
                    descuentos.append(aplicarDescuento)
                    #descuentos.append((expediente.fecha_proximo_pago_exp - datetime.date(hoy)) > timedelta(days = 5))
                return JsonResponse({
                    'codigosAlumnos' : codigosAlumnos,
                    'nombresAlumnos' : nombresAlumnos,
                    'apellidosAlumnos' : apellidosAlumnos,
                    'codigosColegiaturas' : codigosColegiaturas,
                    'tiposPago' : tiposPago,
                    'cuotas' : cuotas,
                    'descuentos' : descuentos,
                }, status=200)
            else:
                return HttpResponse('No hay alumnos en horario', status=500)
        else:
            return redirect('ingresar_pago')
    else:
        return HttpResponseForbidden("No tiene acceso a esta url")