# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect


# Create your views here.

def directorCredencialesPropias(request):
    return render(request, "login/director_credenciales_propias.html", {})


# Esta view gestiona la ruta localhost:8000/
def principal(request):
    if request.user.is_authenticated:
        # Cambiar estooo
        return redirect('credenciales_director')  # Retornar a alguna homepage,esta no xD
    else:
        return redirect('login')  # Redirecciona al login


