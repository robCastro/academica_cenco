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
from datetime import datetime
import itertools

from apps_cenco.db_app.models import Empleado, Alumno, Grupo, Telefono, Horario, Inscripcion

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

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
            grupos = Grupo.objects.order_by('codigo').filter(activo_grupo = True)
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
        raise Http404('Error, no tiene permiso para esta página')

@login_required
def detalle_grupo(request, id_grupo):
    user = User.objects.get(username=request.user)
    if user.groups.filter(name="Director").exists():
        msj = ""
        try:
            grupo = Grupo.objects.get(pk=id_grupo)
        except Grupo.DoesNotExist:
            raise Http404('Grupo no Existe')
        if request.method == 'POST':
            codProfesor = request.POST.get('cbxProfesores')
            if codProfesor != grupo.profesor.codigo and codProfesor != None:
                nuevoProfesor = Empleado.objects.get(pk = codProfesor)
                grupo.profesor = nuevoProfesor
                msj += "Profesor cambiado. "
            if request.POST.get('cambioGrupo'):
                #alumnos = grupo.alumno_set.all()
                inscripciones = grupo.inscripcion_set.filter(actual_inscripcion = True)
                alumnos = []
                for inscripcion in inscripciones:
                    alumnos.append(inscripcion.alumno)
                codGrupo = request.POST.get('cbxGrupos')
                nuevoGrupo = Grupo.objects.get(pk=codGrupo)
                for alumno in alumnos:
                    if request.POST.get(str(alumno.codigo)): #extrayendo los checkbox de alumnos
                        #alumno.grupo = nuevoGrupo
                        viejaInscripcion = Inscripcion.objects.filter(alumno = alumno, actual_inscripcion = True).first()
                        viejaInscripcion.actual_inscripcion = False
                        nuevaInscripcion = Inscripcion.objects.create(alumno = alumno, grupo = nuevoGrupo, actual_inscripcion=True, fecha_inscripcion = datetime.now())
                        viejaInscripcion.save()
                        nuevaInscripcion.save()
                        grupo.alumnosInscritos = grupo.alumnosInscritos - 1
                        nuevoGrupo.alumnosInscritos = nuevoGrupo.alumnosInscritos + 1
                        if grupo.horario != nuevoGrupo.horario:
                            grupo.horario.cantidad_alumnos = grupo.horario.cantidad_alumnos - 1
                            nuevoGrupo.horario.cantidad_alumnos = nuevoGrupo.horario.cantidad_alumnos + 1
                        alumno.save()
                grupo.horario.save()
                nuevoGrupo.horario.save()
                nuevoGrupo.save()
                msj += "Alumnos movidos. "
            grupo.save()
        inscripciones = grupo.inscripcion_set.all().filter(actual_inscripcion=True)
        alumnos = []
        for inscripcion in inscripciones:
            alumnos.append(inscripcion.alumno)
        telefonos = []
        for alumno in alumnos:
            telefonos.append(alumno.telefono_set.first())
        profesores = Empleado.objects.all().filter(tipo='Pro').exclude(codigo = grupo.profesor.codigo)
        grupos = Grupo.objects.exclude(codigo = grupo.codigo).filter(activo_grupo=True).order_by('codigo')
        context = {
            'grupo' : grupo,
            'alumnos' : alumnos,
            'telefonos' : telefonos,
            'profesores' : profesores,
            'grupos' : grupos,
            'usar_msj': msj != "",
            'msj' : msj
        }
        return render(request, 'modulo_grupos/detalle_grupo2.html', context)
    else:
        raise Http404('Error, no tiene permiso para esta página')

@login_required
def eliminarGrupo(request, id_grupo):
    user = User.objects.get(username=request.user)
    if user.groups.filter(name="Director").exists():
        try:
            grupo = Grupo.objects.get(pk=id_grupo)
        except Grupo.DoesNotExist:
            raise Http404('Grupo no Existe')
        if grupo.inscripcion_set.filter(actual_inscripcion = True).count() == 0:
            grupo.activo_grupo = False
            grupo.save()
        return redirect('consultar_grupos')
    else:
        raise Http404('Error, no tiene permiso para esta página')

@login_required
def asist_consultar_grupos(request):
    user = User.objects.get(username=request.user)
    if user.groups.filter(name="Asistente").exists():
        form = CrearGrupoForm()
        limite_por_horario = 15*2
        min_alum_inscritos = 5
        grupos = Grupo.objects.order_by('codigo').filter(activo_grupo = True)
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
        raise Http404('Error, no tiene permiso para esta página')

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
                inscripciones = grupo.inscripcion_set.filter(actual_inscripcion=True, grupo = grupo)
                codAlumnos = []
                for inscripcion in inscripciones:
                    codAlumnos.append(inscripcion.alumno.codigo)
                alumnos = Alumno.objects.filter(pk__in=codAlumnos).order_by('apellido')
                codGrupo = request.POST.get('cbxGrupos')
                nuevoGrupo = Grupo.objects.get(pk=codGrupo)
                for alumno in alumnos:
                    if request.POST.get(str(alumno.codigo)): #extrayendo los checkbox de alumnos
                        print "Moviendo ALumno"
                        #alumno.grupo = nuevoGrupo
                        viejaInscripcion = Inscripcion.objects.filter(alumno=alumno, actual_inscripcion=True).first()
                        viejaInscripcion.actual_inscripcion = False
                        nuevaInscripcion = Inscripcion.objects.create(alumno=alumno, grupo=nuevoGrupo,
                                                                      actual_inscripcion=True,
                                                                      fecha_inscripcion=datetime.now())
                        viejaInscripcion.save()
                        nuevaInscripcion.save()
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
        inscripciones = Inscripcion.objects.filter(actual_inscripcion=True, grupo = grupo)
        codAlumnos = []
        for inscripcion in inscripciones:
            codAlumnos.append(inscripcion.alumno.codigo)
        alumnos = Alumno.objects.filter(pk__in = codAlumnos).order_by('codigo')
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
        raise Http404('Error, no tiene permiso para esta página')


@login_required
def prof_consultar_grupos(request):
    user = User.objects.get(username=request.user)
    prof = Empleado.objects.get(username=user)
    if user.groups.filter(name="Profesor").exists():
        form = CrearGrupoForm()
        limite_por_horario = 15*2
        min_alum_inscritos = 5
        prof=Empleado.objects.get(username=user)
        idProf=prof.codigo
        grupo=Grupo.objects.filter(profesor=idProf, activo_grupo=True)
        grupos = grupo.order_by('codigo')
        horarios = Horario.objects.order_by('codigo')
        horarios_exceso = []
        grupos_cant_baja = []
        tipos = Horario.objects.raw("select distinct dias_asignados, 1 as codigo from db_app_horario " +
                                    "order by dias_asignados")
        for horario in horarios:
            if horario.cantidad_alumnos > limite_por_horario:
                horarios_exceso.append(horario)

        for grup in grupos:
            if grup.alumnosInscritos < min_alum_inscritos:
                grupos_cant_baja.append(grup)

        variables = {'grupos': grupos, 'horarios': horarios, 'horarios_exceso': horarios_exceso,
                     'grupos_cant_baja': grupos_cant_baja, 'lim_horario': limite_por_horario,
                     'min_alumnos': min_alum_inscritos, 'form': form, 'tipos': tipos}

        return render(request, 'modulo_grupos/prof_consultar_grupos.html', variables)
    else:
        raise Http404('Error, no tiene permiso para esta página')
