# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, update_session_auth_hash
from django.contrib.auth.models import User
from django.shortcuts import render
from django import forms
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import render, redirect
from django.contrib.auth.models import Group
from django.contrib import messages

from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.models import User
from django.views.decorators.csrf import requires_csrf_token

from apps_cenco.login.forms import AsistenteCredencialesPropiasForm,AlumnoCredencialesPropiasForm

# Create your views here.

@login_required
def directorCredencialesPropias(request):
    user = User.objects.get(username = request.user)
    if user.groups.filter(name = "Director").exists():
        mensaje = ""
        clase_mensaje = ""
        if request.method == "POST":
            usuarioEscrito = request.POST.get('txtUsuario')
            contraseniaActual = request.POST.get('vieja_contrasenia')
            contraseniaNueva = request.POST.get('contrasenia')
            if user.check_password(contraseniaActual):              #Validando contraseña
                if user.get_username() != usuarioEscrito and User.objects.filter(username = usuarioEscrito).count() > 0:  #Validando usuario unico
                    mensaje = "Usuario ya existe, escoger otro"
                    clase_mensaje = "card border-warning mb-3"
                else:
                    user.username = usuarioEscrito
                    user.set_password(contraseniaNueva)
                    user.save()
                    update_session_auth_hash(request, user)
                    mensaje = "Cambios realizados"
                    clase_mensaje = "card border-info mb-3"
            else:
                mensaje = "Contraseña incorrecta"
                clase_mensaje = "card border-danger mb-3"
        contexto = {
            "mensaje" : mensaje,
            "clase_mensaje" : clase_mensaje,
        }
        return render(request, "login/director_credenciales_propias.html", contexto)
    else:
        return render(request, "plantillas_base/base.html")
@requires_csrf_token
@login_required
def asistenteCredencialesPropias(request):

    id = request.user.id
    usuario = request.user.username
    u = User.objects.get(pk=id)

    if request.user.groups.filter(name="Asistente").exists():
     if request.method == 'POST':
        form = AsistenteCredencialesPropiasForm(request.POST,user=request.user)
        if form.is_valid():
            u.username=form.cleaned_data.get('usuario')
            u.set_password(form.cleaned_data.get('contrasenia1'))
            u.save()
            update_session_auth_hash(request, u)
            messages.success(request,'Sus credenciales han sido modificadas')
            return redirect('asistenteCredencialesPropias')
     else:
        form = AsistenteCredencialesPropiasForm(initial={'usuario':usuario},user=request.user)
     context = {"form": form}
     return render(request, "login/asistente_credenciales_propias.html", context)
    else:
        raise Http404('Error')

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


@login_required
def alumnoCredencialesPropias(request):

    id = request.user.id
    u = User.objects.get(pk=id)

    if request.user.groups.filter(name="Alumno").exists():
     if request.method == 'POST':
        form = AlumnoCredencialesPropiasForm(request.POST,user=request.user)
        if form.is_valid():
            u.set_password(form.cleaned_data.get('contrasenia1'))
            u.save()
            update_session_auth_hash(request, u)
            messages.success(request, 'Su contraseña ha sido modificada')
            return redirect('alumnoCredencialesPropias')
     else:
        form = AlumnoCredencialesPropiasForm(user=request.user)
     context = {"form": form}
     return render(request, "login/alumno_credenciales_propias.html", context)
    else:
        raise Http404('Error')


def log_out(request):
    logout(request)
    return render(request, "plantillas_base/base.html")