# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import Group
from django.shortcuts import render, redirect


# Create your views here.

def directorCredencialesPropias(request):
    return render(request, "login/director_credenciales_propias.html", {})


# Esta view gestiona la ruta localhost:8000/
def principal(request):
    if request.user.is_authenticated:
        if has_group(request.user, 'Director'):
            return redirect('credenciales_director')

        elif has_group(request.user, 'Asistente'):
            return redirect('home_asistente')

        elif has_group(request.user, 'Alumno'):
            return redirect('home_alumno')

        # return redirect('credenciales_director')
    else:
        return redirect('login')  # Redirecciona al login


def homeAsistente(request):
    return redirect('consultar_grupos')


def homeAlumno(request):
    return redirect('crud_horario')

def has_group(user, group_name):
    group = Group.objects.get(name=group_name)
    return True if group in user.groups.all() else False


