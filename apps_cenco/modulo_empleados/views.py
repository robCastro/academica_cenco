# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import User

from datetime import datetime

from django.contrib.auth.decorators import permission_required, login_required
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render,redirect
from django.http import Http404, HttpResponseRedirect, HttpResponseForbidden
import sys
from django.contrib.auth.models import Group
from apps_cenco.db_app.models import Alumno
from apps_cenco.modulo_alumnos.forms import InsertarAlumnoForm, CrearEncargadoForm, TelefonoForm
from django.shortcuts import render
from django.template import loader
from django.http import Http404, HttpResponse, JsonResponse,HttpResponseServerError
from apps_cenco.db_app.models import Telefono, Grupo, Horario, Encargado

from apps_cenco.modulo_alumnos.forms import ModificarAlumnoForm
from apps_cenco.db_app.models import Empleado
from datetime import datetime
from apps_cenco.modulo_empleados.forms import CrearEmpleadoForm

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

@login_required
def consultar_empleados(request):
    if request.user.groups.filter(name="Director").exists():
        empleados= Empleado.objects.filter(estado='activo')
        for empleado in empleados:
            empleado.primerTelefono = empleado.telefono_set.first()

        return render(request, 'modulo_empleados/director_listaEmpleadosActivos.html', {'empleados': empleados})
    else:
        raise Http404('Error, no tiene permiso para ver esta página')

@login_required
def detalle_de_empleado(request,id_empleado):
    if request.user.groups.filter(name="Director").exists():
        empleados = Empleado.objects.filter(estado='activo')
    else:
        raise Http404('Error, no tiene permiso para ver esta página')


@login_required
def dir_crear_empleado(request):
    if request.user.groups.filter(name="Director").exists():
        if request.method == 'POST':
            form = CrearEmpleadoForm(request.POST)
            if form.is_valid():
                empleado = form.save(commit=False)
                empleado.estado = 'activo'
                empleado.save()
                return HttpResponse('Empleado guardado con exito')
            else:
                return HttpResponse('Se reciberon datos incorrectos', status=500)
        else:
            form = CrearEmpleadoForm()
            return render(request, 'modulo_empleados/dir_crear_empleado.html', {'form': form})
    else:
        raise Http404('No tiene permiso para esta ruta')

@login_required
def consultar_empleados_inactivos(request):
    if request.user.groups.filter(name="Director").exists():
        empleados = Empleado.objects.filter(estado='inactivo')
        for empleado in empleados:
            empleado.primerTelefono = empleado.telefono_set.first()
        return render(request, 'modulo_empleados/director_listaEmpleadosInactivos.html', {'empleados': empleados})
    else:
        raise Http404('Error, no tiene permiso para ver esta página')
