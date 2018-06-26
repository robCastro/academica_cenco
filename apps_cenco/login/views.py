# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, update_session_auth_hash
from django.contrib.auth.models import User
from django.shortcuts import render

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

def log_out(request):
    logout(request)
    return render(request, "plantillas_base/base.html")