# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from django.http import Http404
from django.views.generic.detail import  DetailView

from apps_cenco.db_app.models import Empleado, Alumno, Grupo, Telefono

# Create your views here.
def detalle_grupo(request, id_grupo):
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
    return render(request, 'modulo_grupos/detalle_grupo.html', context)