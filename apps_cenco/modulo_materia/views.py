# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import render, get_object_or_404

# Create your views here.
from apps_cenco.db_app.models import Materia, Documento, Alumno, DetallePensum, Cursa
from apps_cenco.modulo_materia.forms import CrearEditarMateriaForm, SubirDocumentoForm

@login_required
def crear_materia(request):
    if request.user.groups.filter(name="Director").exists():
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
    else:
        return HttpResponseForbidden('No tiene acceso a esta dirección')


@login_required
def editar_materia(request, id_materia):
    if request.user.groups.filter(name="Director").exists():
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
    else:
        return HttpResponseForbidden('No tiene acceso a esta dirección')


@login_required
def subir_documentos(request):
    if request.user.groups.filter(name="Director").exists():
        if request.method == 'POST' and request.FILES['archivo']:
            form = SubirDocumentoForm(request.POST, request.FILES)
            form2 = SubirDocumentoForm()
            if form.is_valid():
                form.save()
                mensaje = 'Documento subido con exito'
                context = {'mensaje': mensaje, 'form': form2 ,'post': True}
                return render(request, 'modulo_materia/subir_documentos.html', context)
            else:
                mensaje = 'Se recibieron datos incorrectos'
                context = {'mensaje': mensaje , 'form': form2 , 'post': True}
                return render(request, 'modulo_materia/subir_documentos.html', context)
        else:
            form = SubirDocumentoForm()
            context = {'form': form}
            return render(request, 'modulo_materia/subir_documentos.html', context)
    else:
        return HttpResponseForbidden('No tiene acceso a esta dirección')


@login_required
def descargar_documentos(request):
    if request.user.groups.filter(name="Profesor").exists():
        materias = Materia.objects.all().order_by('codigo_materia')
        documentos = Documento.objects.all().order_by('codigo_doc')
        context = {'materias': materias, 'documentos': documentos}
        return render(request, 'modulo_materia/descargar_documentos.html', context)
    else:
        return HttpResponseForbidden('No tiene acceso a esta dirección')


@login_required
def consultar_material(request):
    if request.user.groups.filter(name="Alumno").exists():
        user = request.user
        alumno = get_object_or_404(Alumno, username=user)
        cursa = get_object_or_404(Cursa, alumno=alumno, actual_cursa=True)
        documentos = Documento.objects.filter(materia=cursa.materia).order_by('codigo_doc')
        context = {'documentos': documentos, 'materia': cursa.materia}
        return render(request, 'modulo_materia/consultar_material.html', context)
    else:
        return HttpResponseForbidden('No tiene acceso a esta dirección')
