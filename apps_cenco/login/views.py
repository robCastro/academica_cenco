# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import forms
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import render, redirect

from django.contrib import messages

from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.models import User
from django.views.decorators.csrf import requires_csrf_token

from apps_cenco.login.forms import AsistenteCredencialesPropiasForm,AlumnoCredencialesPropiasForm

# Create your views here.

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

