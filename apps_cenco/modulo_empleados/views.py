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
from django.template import loader
from django.http import Http404, HttpResponse, JsonResponse,HttpResponseServerError
from apps_cenco.db_app.models import Telefono, Grupo, Horario, Encargado
from apps_cenco.modulo_alumnos.forms import ModificarAlumnoForm
from datetime import datetime
from apps_cenco.modulo_empleados.forms import CrearEmpleadoForm
from django.template.loader import get_template
from apps_cenco.db_app.models import Empleado, Telefono, Grupo
from django.contrib.auth.models import User

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

# Create your views here.

@login_required
def modificar_empleado(request,id_empleado):
    if request.user.groups.filter(name="Director").exists():
        if request.method == 'POST':
            mensaje=""
            empleado = Empleado.objects.get(pk=id_empleado)
            telefono = Telefono.objects.filter(empleado=empleado).count()
            if not telefono:
                telefono = Telefono.objects.create(numero='1',empleado=empleado)
            else:
                telefono = empleado.telefono_set.first()

            empleado.nombre = request.POST.get('nombre')
            empleado.apellido = request.POST.get('apellido')
            empleado.direccion = request.POST.get('direccion')
            empleado.dui = request.POST.get('dui')
            numeroTel = request.POST.get('numeroTel')
            tipoTel = request.POST.get('tipoTel')
            empleado.nit = request.POST.get('nit')
            empleado.isss = request.POST.get('isss')
            empleado.afp = request.POST.get('afp')
            correo = request.POST.get('correo')

            if correo:
                empleado.correo=correo

            # Verifica que el profesor tenga grupos asignados
            if empleado.tipo == 'Pro':
                grupo = Grupo.objects.filter(profesor=empleado).count()
                if not grupo:
                    grupo_pc = False
                else:
                    grupo_pc = True
            else:
                #if empleado.tipo == 'Tec':
                    #verificar que el tecnico tenga pcs en uso
                #else:
                grupo_pc = False

            if not grupo_pc:
                empleado.tipo = request.POST.get('tipoEmp')

            empleado.save()

            if numeroTel:
                telefono.numero=numeroTel
                telefono.tipo=tipoTel
                telefono.save()

            mensaje="Empleado modificado con éxito"
            return HttpResponse(mensaje,status=200)
        else:
            empleado = Empleado.objects.get(pk=id_empleado)
            telefono = Telefono.objects.filter(empleado=empleado).count()
            if not telefono:
                telefono = None
            else:
                telefono=empleado.telefono_set.first()

            #Verifica que el profesor tenga grupos asignados
            if empleado.tipo == 'Pro':
                grupo=Grupo.objects.filter(profesor=empleado).count()
                if not grupo:
                    grupo_pc=False
                else:
                    grupo_pc=True
            else:
                # if empleado.tipo == 'Tec':
                    # verificar que el tecnico tenga pcs en uso
                # else:
                grupo_pc=False

            context = {
                'empleado': empleado, 'telefono': telefono,'grupo_pc':grupo_pc,
            }
            return render(request, "modulo_empleados/modificar_empleado.html",context)
    else:
        raise Http404('Error, no tiene permiso para esta página')

@login_required
def director_datos_propios(request):
    if request.user.groups.filter(name="Director").exists():
        if request.method == 'POST':
            user = User.objects.get(username=request.user)
            user.first_name = request.POST.get('nombre')
            user.last_name = request.POST.get('apellido')
            if not user.check_password(request.POST.get('contrasenia1')):
                return HttpResponse('',status=500)
            else:
                user.save()
                mensaje = "Datos modificados con éxito" + "," + user.get_full_name()
                return HttpResponse(mensaje,status=200)
        else:
            user = User.objects.get(username=request.user)
            context = {
                'user': user,
            }
            return render(request, "modulo_empleados/director_datos_propios.html",context)
    else:
        raise Http404('Error, no tiene permiso para esta página')

@login_required
def director_datos_propios_usuario(request):
    if request.user.groups.filter(name="Director").exists():
        if request.method == 'POST':
            user = User.objects.get(username=request.user)
            user.username = request.POST.get('usuario')
            if not user.check_password(request.POST.get('contrasenia2')):
                return HttpResponse('',status=500)
            else:
                user.save()
                mensaje = "Datos modificados con éxito" + "," + user.username
                return HttpResponse(mensaje,status=200)
        else:
            return Http404('Error, acceso solo mediante POST')
    else:
        raise Http404('Error, no tiene permiso para esta página')

@login_required
def director_datos_propios_correo(request):
    if request.user.groups.filter(name="Director").exists():
        if request.method == 'POST':
            user = User.objects.get(username=request.user)
            user.email = request.POST.get('correo')
            if not user.check_password(request.POST.get('contrasenia3')):
                return HttpResponse('',status=500)
            else:
                user.save()
                mensaje = "Datos modificados con éxito" + "," + user.email
                return HttpResponse(mensaje,status=200)
        else:
            return Http404('Error, acceso solo mediante POST')
    else:
        raise Http404('Error, no tiene permiso para esta página')

@login_required
def director_datos_propios_contrasenia(request):
    if request.user.groups.filter(name="Director").exists():
        if request.method == 'POST':
            user = User.objects.get(username=request.user)
            if not user.check_password(request.POST.get('contrasenia4')):
                return HttpResponse('',status=500)
            else:
                user.set_password(request.POST.get('contraseniaNueva'))
                user.save()
                mensaje = "Datos modificados con éxito"
                return HttpResponse(mensaje,status=200)
        else:
            return Http404('Error, acceso solo mediante POST')
    else:
        raise Http404('Error, no tiene permiso para esta página')