# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from apps_cenco.db_app.models import Carrera
from apps_cenco.modulo_carrera.forms import CrearEditarCarreraForm

@login_required
def crear_carrera(request):
    editar = False
    if request.method == 'POST':
        print ('datos POST')
        print (request.POST)
        form = CrearEditarCarreraForm(request.POST)
        if form.is_valid():
            form.save()
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

