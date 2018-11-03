# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from apps_cenco.db_app.models import Materia
from apps_cenco.modulo_materia.forms import CrearEditarMateriaForm


def crear_materia(request):
    editar = False
    if request.method == 'POST':
        form = CrearEditarMateriaForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse('Se ha guardado la nueva materia correctamente')
        else:
            return HttpResponse('Se recibieron datos incorrectos', status=500)
    else:
        form = CrearEditarMateriaForm()
        context = {'form': form, 'editar': editar}
        return render(request,  'modulo_materia/crear_editar_materia.html', context)


def editar_materia(request, id_materia):
    editar = True
    if request.method == 'POST':
        materia = Materia.objects.get(codigo_materia=id_materia)
        form = CrearEditarMateriaForm(request.POST, instance=materia)
        if form.is_valid():
            form.save()
            return HttpResponse('Información de la materia actualizada correctamente')
        else:
            return HttpResponse('Se recibieron datos incorrectos', status=500)
    else:
        materia = Materia.objects.get(codigo_materia= id_materia)
        form = CrearEditarMateriaForm(instance=materia)
        context = {'form': form, 'editar': editar, 'id_materia': id_materia}
        return render(request, 'modulo_materia/crear_editar_materia.html', context)
