# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from apps_cenco.db_app.models import Carrera, Materia, Cursa, DetallePensum
from apps_cenco.modulo_carrera.forms import CrearEditarCarreraForm


@login_required
def crear_carrera(request):
    editar = False
    if request.method == 'POST':
        print ('datos POST')
        print (request.POST)
        form = CrearEditarCarreraForm(request.POST)
        if form.is_valid():
            carrera = form.save(commit=False)
            carrera.pensum_mes_carrera = datetime.today().month
            carrera.pensum_anio_carrera = datetime.today().year
            carrera.save()
            return HttpResponse('Se ha guardado la nueva carrera correctamente')
        else:
            return HttpResponse('Se recibieron datos incorrectos', status=500)
    else:
        form = CrearEditarCarreraForm()
        context = {'form': form, 'editar': editar}
        return render(request,  'modulo_carrera/crear_editar_carrera.html', context)


@login_required
def editar_carrera(request, id_carrera):
    editar = True
    if request.method == 'POST':
        carrera = Carrera.objects.get(codigo_carrera=id_carrera)
        form = CrearEditarCarreraForm(request.POST, instance=carrera)
        if form.is_valid():
            form.save()
            return HttpResponse('Información de la carrera actualizada correctamente')
        else:
            return HttpResponse('Se recibieron datos incorrectos', status=500)
    else:
        carrera = Carrera.objects.get(codigo_carrera= id_carrera)
        form = CrearEditarCarreraForm(instance=carrera)
        context = {'form': form, 'editar': editar, 'id_carrera': id_carrera}
        return render(request, 'modulo_carrera/crear_editar_carrera.html', context)


@login_required
def crear_pensum(request, id_carrera):
    detalle_pensumE = DetallePensum.objects.filter(carrera_id=id_carrera).distinct('carrera_id')
    if not detalle_pensumE:
        carrera = Carrera.objects.get(codigo_carrera=id_carrera)
        if request.method == 'POST':
            lista = request.POST.get('lista')
            list_data = json.loads(lista)
            for a in list_data:
                materia = Materia.objects.get(codigo_materia=list_data[a])
                detalle_pensum = DetallePensum(carrera=carrera, materia=materia, ordinal_materia_cursa=int(a)+1)
                detalle_pensum.save()
            return HttpResponse('Pensum creado con exito.')
        else:
            materias = Materia.objects.all()
            context = {'carrera': carrera, 'materias': materias}
            return render(request, 'modulo_carrera/crear_pensum.html', context)
    else:
        context = {'existente': True}
        return render(request, 'modulo_carrera/crear_pensum.html', context)


@login_required
def consultar_carrera(request):
    carreras = Carrera.objects.all().order_by('codigo_carrera')
    pensum = DetallePensum.objects.all().order_by('ordinal_materia_cursa')
    context = {'carreras': carreras, 'pensum': pensum}
    return render(request, 'modulo_carrera/consultar_carreras.html', context)

