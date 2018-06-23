# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.

def directorCredencialesPropias(request):
    return render(request, "login/director_credenciales_propias.html", {})
