# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import User

from datetime import datetime

from django.contrib.auth.decorators import permission_required, login_required
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, redirect, get_object_or_404
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

import sys

from apps_cenco.modulo_empleados.forms import CrearEmpleadoForm, CrearTelefonoForm

reload(sys)
sys.setdefaultencoding('utf-8')

@login_required
def consultar_empleados(request):
    if request.user.groups.filter(name="Director").exists():
        empleados= Empleado.objects.filter(estado='inactivo')
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
def dir_ver_empleado(request, id_empleado):
    if request.user.groups.filter(name="Director").exists():
        empleado = get_object_or_404(Empleado, codigo=id_empleado)
        telefonos = ''
        if empleado:
            telefonos = Telefono.objects.filter(empleado=empleado)
        context = {'empleado': empleado, 'telefonos': telefonos}
        return render(request, 'modulo_empleados/director_verEmpleado.html', context)
    else:
        raise Http404('No tiene permiso para esta ruta')


@login_required
def dir_crear_empleado(request):
    if request.user.groups.filter(name="Director").exists():
        if request.method == 'POST':
            form = CrearEmpleadoForm(request.POST)
            formTelefono = CrearTelefonoForm(request.POST)
            print (request.POST)
            if form.is_valid() and formTelefono.is_valid():
                empleado = form.save(commit=False)
                print (request.POST)
                usuario = request.POST.get('username')
                if validar_username(usuario):
                    password = User.objects.make_random_password(
                        length=6,
                        allowed_chars='abcdefghjkmnpqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ23456789')
                    newusername = User.objects.create_user(username=usuario, email=empleado.correo, password=password)
                    empleado.username = newusername
                    empleado.estado = 'activo'
                    telefono = formTelefono.save(commit=False)
                    telefono.empleado = empleado
                    empleado.save()
                    telefono.save()
                    return HttpResponse('Empleado guardado con exito. User: ' + usuario + ' Clave: ' + password)
                else:
                    return HttpResponse('El nombre de usuario no esta disponible', status=500)
            else:
                print (form.errors, formTelefono.errors)
                return HttpResponse('Se reciberon datos incorrectos', status=500)
        else:
            form = CrearEmpleadoForm()
            formTelefono = CrearTelefonoForm()
            return render(request, 'modulo_empleados/dir_crear_empleado.html', {'form': form, 'formT': formTelefono})
    else:
        raise Http404('No tiene permiso para esta ruta')


def validar_username(username):
    try:
        User.objects.get(username=username)
        return False
    except ObjectDoesNotExist:
        return True


@login_required
def verificar_username_libre(request):
    if request.method == 'POST':
        usuario = request.POST.get('nombreUsuario')
        if User.objects.get(username = usuario):
            return HttpResponse('Usuario no disponible', status=500)
        else:
            return HttpResponse('Usuario disponible')