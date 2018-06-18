# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from apps_cenco.db_app.models import Alumno
from apps_cenco.modulo_alumnos.forms import InsertarAlumnoForm, CrearEncargadoForm
from django.shortcuts import render
from django.template import loader
from django.http import Http404, HttpResponse

def RegistroAlumno(request):
    form = InsertarAlumnoForm(request.POST or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
    form2 = CrearEncargadoForm()
    context ={
        "form":form,
        "form2":form2,
    }
    return render(request,"modulo_alumnos/registrar_alumnos.html",context)

def RegistrEncargado(request):
 if request.method == 'post':
    form2 = CrearEncargadoForm(request.POST)
    form=  InsertarAlumnoForm()
    if form2.is_valid():
        form2.save()
        encargado = form.save(commit=False)
        id=encargado.codigo
        nombre= encargado.nombre+" "+encargado.apellido
        return HttpResponse('<option value="+id+">+nombre+</option>')


