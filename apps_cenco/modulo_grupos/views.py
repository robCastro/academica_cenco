# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import ProtectedError, Q
from django.shortcuts import render, render_to_response, redirect
from django.http import Http404, HttpResponse, JsonResponse
from django.shortcuts import render, render_to_response, redirect
from django.http import Http404, HttpResponse
from django.template import loader
from django.views.generic.detail import  DetailView
import itertools

from apps_cenco.db_app.models import Empleado, Alumno, Grupo, Telefono, Horario


# Create your views here.
from apps_cenco.modulo_grupos.forms import CrearGrupoForm


# Consulta y guarda nuevos grupos.
@login_required
def consultar_grupos(request):
    user = User.objects.get(username=request.user)
    if user.groups.filter(name="Director").exists():
        if request.method == 'POST':
            form = CrearGrupoForm(request.POST)
            if form.is_valid():
                form.save()
                grupo = form.save(commit=False)
                temp = loader.get_template('modulo_grupos/div_nuevo_grupo.html').render({'grupo': grupo})
                return HttpResponse(temp)
            else:
                return HttpResponse("")
        else:
            form = CrearGrupoForm()
            limite_por_horario = 15*2
            min_alum_inscritos = 5
            grupos = Grupo.objects.order_by('codigo')
            horarios = Horario.objects.order_by('codigo')
            horarios_exceso = []
            grupos_cant_baja = []
            tipos = Horario.objects.raw("select distinct dias_asignados, 1 as codigo from db_app_horario " +
                                        "order by dias_asignados")
            for horario in horarios:
                if horario.cantidad_alumnos > limite_por_horario:
                    horarios_exceso.append(horario)

            for grupo in grupos:
                if grupo.alumnosInscritos < min_alum_inscritos:
                    grupos_cant_baja.append(grupo)

            variables = {'grupos': grupos, 'horarios': horarios, 'horarios_exceso': horarios_exceso,
                         'grupos_cant_baja': grupos_cant_baja, 'lim_horario': limite_por_horario,
                         'min_alumnos': min_alum_inscritos, 'form': form, 'tipos': tipos}

            return render(request, 'modulo_grupos/consultar_grupos.html', variables)
    else:
        return render(request, "plantillas_base/base.html")

@login_required
def detalle_grupo(request, id_grupo):
    user = User.objects.get(username=request.user)
    if user.groups.filter(name="Director").exists():
        try:
            grupo = Grupo.objects.get(pk=id_grupo)
        except Grupo.DoesNotExist:
            raise Http404('Grupo no Existe')
        if request.method == 'POST':
            codProfesor = request.POST.get('cbxProfesores')
            if codProfesor != grupo.profesor.codigo and codProfesor != None:
                nuevoProfesor = Empleado.objects.get(pk = codProfesor)
                grupo.profesor = nuevoProfesor
            if request.POST.get('cambioGrupo'):
                alumnos = grupo.alumno_set.all()
                codGrupo = request.POST.get('cbxGrupos')
                nuevoGrupo = Grupo.objects.get(pk=codGrupo)
                for alumno in alumnos:
                    if request.POST.get(str(alumno.codigo)): #extrayendo los checkbox de alumnos
                        alumno.grupo = nuevoGrupo
                        grupo.alumnosInscritos = grupo.alumnosInscritos - 1
                        nuevoGrupo.alumnosInscritos = nuevoGrupo.alumnosInscritos + 1
                        if grupo.horario != nuevoGrupo.horario:
                            grupo.horario.cantidad_alumnos = grupo.horario.cantidad_alumnos - 1
                            nuevoGrupo.horario.cantidad_alumnos = nuevoGrupo.horario.cantidad_alumnos + 1
                        alumno.save()
                grupo.horario.save()
                nuevoGrupo.horario.save()
                nuevoGrupo.save()
            grupo.save()
        alumnos = grupo.alumno_set.all().order_by('codigo')
        telefonos = []
        for alumno in alumnos:
            telefonos.append(alumno.telefono_set.first())
        profesores = Empleado.objects.all().filter(tipo='Pro').exclude(codigo = grupo.profesor.codigo)
        grupos = Grupo.objects.exclude(codigo = grupo.codigo).order_by('codigo')
        context = {
            'grupo' : grupo,
            'alumnos' : alumnos,
            'telefonos' : telefonos,
            'profesores' : profesores,
            'grupos' : grupos
        }
        return render(request, 'modulo_grupos/detalle_grupo2.html', context)
    else:
        return render(request, "plantillas_base/base.html")

@login_required
def eliminarGrupo(request, id_grupo):
    user = User.objects.get(username=request.user)
    if user.groups.filter(name="Director").exists():
        try:
            grupo = Grupo.objects.get(pk=id_grupo)
        except Grupo.DoesNotExist:
            raise Http404('Grupo no Existe')
        if grupo.alumno_set.all().count() == 0:
            grupo.delete()
        return redirect('consultar_grupos')
    else:
        return render(request, "plantillas_base/base.html")

@login_required
def asist_consultar_grupos(request):
    user = User.objects.get(username=request.user)
    if user.groups.filter(name="Asistente").exists():
        form = CrearGrupoForm()
        limite_por_horario = 15*2
        min_alum_inscritos = 5
        grupos = Grupo.objects.order_by('codigo')
        horarios = Horario.objects.order_by('codigo')
        horarios_exceso = []
        grupos_cant_baja = []
        tipos = Horario.objects.raw("select distinct dias_asignados, 1 as codigo from db_app_horario " +
                                    "order by dias_asignados")
        for horario in horarios:
            if horario.cantidad_alumnos > limite_por_horario:
                horarios_exceso.append(horario)

        for grupo in grupos:
            if grupo.alumnosInscritos < min_alum_inscritos:
                grupos_cant_baja.append(grupo)

        variables = {'grupos': grupos, 'horarios': horarios, 'horarios_exceso': horarios_exceso,
                     'grupos_cant_baja': grupos_cant_baja, 'lim_horario': limite_por_horario,
                     'min_alumnos': min_alum_inscritos, 'form': form, 'tipos': tipos}

        return render(request, 'modulo_grupos/asist_consultar_grupos.html', variables)
    else:
        return render(request, "plantillas_base/base.html")

@login_required
def asist_detalle_grupo(request, id_grupo):
    user = User.objects.get(username=request.user)
    if user.groups.filter(name="Asistente").exists():
        try:
            grupo = Grupo.objects.get(pk=id_grupo)
        except Grupo.DoesNotExist:
            raise Http404('Grupo no Existe')
        if request.method == 'POST':
            codProfesor = request.POST.get('cbxProfesores')
            if request.POST.get('cambioGrupo'):
                alumnos = grupo.alumno_set.all()
                codGrupo = request.POST.get('cbxGrupos')
                nuevoGrupo = Grupo.objects.get(pk=codGrupo)
                for alumno in alumnos:
                    if request.POST.get(str(alumno.codigo)): #extrayendo los checkbox de alumnos
                        alumno.grupo = nuevoGrupo
                        grupo.alumnosInscritos = grupo.alumnosInscritos - 1
                        nuevoGrupo.alumnosInscritos = nuevoGrupo.alumnosInscritos + 1
                        if grupo.horario != nuevoGrupo.horario:
                            grupo.horario.cantidad_alumnos = grupo.horario.cantidad_alumnos - 1
                            nuevoGrupo.horario.cantidad_alumnos = nuevoGrupo.horario.cantidad_alumnos + 1
                        alumno.save()
                grupo.horario.save()
                nuevoGrupo.horario.save()
                nuevoGrupo.save()
            grupo.save()
        alumnos = grupo.alumno_set.all().order_by('codigo')
        telefonos = []
        for alumno in alumnos:
            telefonos.append(alumno.telefono_set.first())
        profesores = Empleado.objects.all().filter(tipo='Pro').exclude(codigo = grupo.profesor.codigo)
        grupos = Grupo.objects.exclude(codigo = grupo.codigo).order_by('codigo')
        context = {
            'grupo' : grupo,
            'alumnos' : alumnos,
            'telefonos' : telefonos,
            'profesores' : profesores,
            'grupos' : grupos
        }
        return render(request, 'modulo_grupos/asist_detalle_grupo.html', context)
    else:
        return render(request, "plantillas_base/base.html")