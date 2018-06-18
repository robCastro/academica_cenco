# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import sys

from apps_cenco.db_app.models import Alumno
from apps_cenco.modulo_alumnos.forms import InsertarAlumnoForm, CrearEncargadoForm
from django.shortcuts import render
from django.template import loader
from django.http import Http404, HttpResponse


def registro_alumno(request):
    if request.method == "POST":
        form = InsertarAlumnoForm(request.POST)
        if form.is_valid():
            form.save()
        # Aqui quizas quepa un else para cuado algo falle. Error 500 talves?
    form = InsertarAlumnoForm()
    context = {
        "form": form,
    }
    return render(request, "modulo_alumnos/registrar_alumnos.html", context)


def registrar_encargado(request):
    if request.method == 'POST':
        form2 = CrearEncargadoForm(request.POST)
        if form2.is_valid():
            form2.save()
            encargado = form2.save(commit=False)
            id=encargado.codigo.__str__()
            nombre= encargado.nombre+" "+encargado.apellido
            return HttpResponse('<option value="'+id+'">'+nombre+'</option>')
        # Seria bueno agregar aqui un Internal Server error. Para cuando no guarde bien.
    else:
        form = InsertarAlumnoForm()
        context = {
            "form": form,
        }
        return render(request, "modulo_alumnos/registrar_alumnos.html", context)


