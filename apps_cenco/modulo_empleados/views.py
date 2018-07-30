# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.template.loader import get_template

from apps_cenco.db_app.models import Empleado, Telefono, Grupo
from django.contrib.auth.models import User

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

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