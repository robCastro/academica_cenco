# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, update_session_auth_hash
from django.contrib.auth.models import User
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django import forms
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.models import Group
from django.contrib import messages

from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.models import User
from django.views.decorators.csrf import requires_csrf_token

from apps_cenco.db_app.models import Alumno, Horario, Empleado
from apps_cenco.login.forms import AsistenteCredencialesPropiasForm, AlumnoCredencialesPropiasForm, ModCredAsistForm


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
                    mensaje = "Cambios realizados"
                    clase_mensaje = "card border-info mb-3"
                    return redirect('director_credenciales_propias')
            else:
                mensaje = "Contraseña incorrecta"
                clase_mensaje = "card border-danger mb-3"
        contexto = {
            "mensaje" : mensaje,
            "clase_mensaje" : clase_mensaje,
        }
        return render(request, "login/director_credenciales_propias.html", contexto)
    else:
        raise Http404('Error, no tiene permiso para esta página')
@requires_csrf_token

@login_required
def consultar_alumnos(request):
    user = User.objects.get(username = request.user)
    if user.groups.filter(name = "Director").exists():

        if request.method == 'POST':
            idAlumno=request.POST.get('id_alumno')
            alumno = Alumno.objects.get(pk=idAlumno)
            contra1=request.POST.get('contrasena1')
            contra2 = request.POST.get('contrasena2')
            nomUsuarioNuevo=request.POST.get('nombre_usuario_nuevo')
            print idAlumno,contra1,contra2,nomUsuarioNuevo
            nomUsuarioActual=request.POST.get('nombre_usuario_actual')
            existe=User.objects.filter(username=nomUsuarioNuevo).count()

            if nomUsuarioNuevo!=nomUsuarioActual:
                if existe:
                    raise forms.ValidationError('El nombre de usuario ya existe')
                elif contra1 and contra2 and contra1 != contra2:
                    raise forms.ValidationError('Las contraseñas no coinciden')
                else:
                    alumno.username.username=nomUsuarioNuevo
                    alumno.username.set_password(contra1)
                    alumno.username.save()
                    messages.success(request, 'Las credenciales han sido modificadas')

                    return HttpResponseRedirect('/credenciales/alumnos/')

        else:

            form = ModCredAsistForm()
            alumnos = Alumno.objects.order_by('codigo')
            telefonos = []

            for alumno in alumnos:
                telefonos.append(alumno.telefono_set.first())

            tipos = Horario.objects.raw("select distinct dias_asignados, 1 as codigo from db_app_horario " +
                                        "order by dias_asignados")

            page = request.GET.get('page', 1)
            paginator = Paginator(alumnos, 10)
            try:
                users = paginator.page(page)
            except PageNotAnInteger:
                users = paginator.page(1)
            except EmptyPage:
                users = paginator.page(paginator.num_pages)

            context = {
                'form': form,
                'users': users,
                'alumnos': alumnos,
                'telefonos': telefonos,
                'tipos': tipos
            }

        return render(request, 'login/credenciales_alumno.html', context)
    else:
        raise Http404('Error, no tiene permiso para esta página')

@login_required
def consultar_alumnos(request):
    user = User.objects.get(username = request.user)
    if user.groups.filter(name = "Director").exists():

        if request.method == 'POST':
            idAlumno=request.POST.get('id_alumno')
            alumno = Alumno.objects.get(pk=idAlumno)
            contra1=request.POST.get('contrasena1')
            contra2 = request.POST.get('contrasena2')
            nomUsuarioNuevo=request.POST.get('nombre_usuario_nuevo')
            print idAlumno,contra1,contra2,nomUsuarioNuevo
            nomUsuarioActual=request.POST.get('nombre_usuario_actual')
            existe=User.objects.filter(username=nomUsuarioNuevo).count()

            if nomUsuarioNuevo!=nomUsuarioActual:
                if existe:
                    raise forms.ValidationError('El nombre de usuario ya existe')
                elif contra1 and contra2 and contra1 != contra2:
                    raise forms.ValidationError('Las contraseñas no coinciden')
                else:
                    alumno.username.username=nomUsuarioNuevo
                    alumno.username.set_password(contra1)
                    alumno.username.save()
                    messages.success(request, 'Las credenciales han sido modificadas')

                    return HttpResponseRedirect('/credenciales/alumnos/')

        else:

            form = ModCredAsistForm()
            alumnos = Alumno.objects.order_by('codigo')
            telefonos = []

            for alumno in alumnos:
                telefonos.append(alumno.telefono_set.first())

            tipos = Horario.objects.raw("select distinct dias_asignados, 1 as codigo from db_app_horario " +
                                        "order by dias_asignados")

            page = request.GET.get('page', 1)
            paginator = Paginator(alumnos, 10)
            try:
                users = paginator.page(page)
            except PageNotAnInteger:
                users = paginator.page(1)
            except EmptyPage:
                users = paginator.page(paginator.num_pages)

            context = {
                'form': form,
                'users': users,
                'alumnos': alumnos,
                'telefonos': telefonos,
                'tipos': tipos
            }

        return render(request, 'login/credenciales_alumno.html', context)
    else:
        raise Http404('Error, no tiene permiso para esta página')

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
            messages.success(request,'Sus credenciales han sido modificadas')
            return redirect('asistenteCredencialesPropias')
     else:
        form = AsistenteCredencialesPropiasForm(initial={'usuario':usuario},user=request.user)
     context = {"form": form}
     return render(request, "login/asistente_credenciales_propias.html", context)
    else:
        raise Http404('Error, no tiene permiso para esta página')

# Esta view gestiona la ruta localhost:8000/
def principal(request):
    if request.user.is_authenticated:
        if has_group(request.user, 'Director'):
            return redirect('consultar_grupos')

        elif has_group(request.user, 'Asistente'):
            return redirect('home_asistente')

        elif has_group(request.user, 'Alumno'):
            return redirect('home_alumno')

        # return redirect('credenciales_director')
    else:
        return redirect('login')  # Redirecciona al login


def homeAsistente(request):
    return redirect('asistenteConsultarAlumnos')


def homeAlumno(request):
    return redirect('ver_alumno_propio')

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
            messages.success(request, 'Su contraseña ha sido modificada')
            return redirect('alumnoCredencialesPropias')
     else:
        form = AlumnoCredencialesPropiasForm(user=request.user)
     context = {"form": form}
     return render(request, "login/alumno_credenciales_propias.html", context)
    else:
        raise Http404('Error, no tiene permiso para esta página')


@login_required
def consultar_asistentes(request):
    user = User.objects.get(username = request.user)
    if user.groups.filter(name = "Director").exists():

        if request.method == 'POST':
            idEmpleado=request.POST.get('id_alumno')
            alumno = Empleado.objects.get(pk=idEmpleado)
            contra1=request.POST.get('contrasena1')
            contra2 = request.POST.get('contrasena2')
            nomUsuarioNuevo=request.POST.get('nombre_usuario_nuevo')
            print idEmpleado,contra1,contra2,nomUsuarioNuevo
            nomUsuarioActual=request.POST.get('nombre_usuario_actual')
            existe=User.objects.filter(username=nomUsuarioNuevo).count()

            if nomUsuarioNuevo!=nomUsuarioActual:
                if existe:
                    raise forms.ValidationError('El nombre de usuario ya existe')
                elif contra1 and contra2 and contra1 != contra2:
                    raise forms.ValidationError('Las contraseñas no coinciden')
                else:
                    alumno.username.username=nomUsuarioNuevo
                    alumno.username.set_password(contra1)
                    alumno.username.save()
                    messages.success(request, 'Las credenciales han sido modificadas')

                    return render(request,"login/credenciales_asistente.html")

        else:

            form = ModCredAsistForm()
            asistentes = Empleado.objects.filter(tipo='Asi').order_by('codigo')
            telefonos = []

            for asistente in asistentes:
                telefonos.append(asistente.telefono_set.first())

            tipos = Horario.objects.raw("select distinct dias_asignados, 1 as codigo from db_app_horario " +
                                        "order by dias_asignados")

            page = request.GET.get('page', 1)
            paginator = Paginator(asistentes, 10)
            try:
                users = paginator.page(page)
            except PageNotAnInteger:
                users = paginator.page(1)
            except EmptyPage:
                users = paginator.page(paginator.num_pages)

            context = {
                'form': form,
                'users': users,
                'asistentes': asistentes,
                'telefonos': telefonos,
                'tipos': tipos
            }

            return render(request, 'login/credenciales_asistente.html', context)
    else:
        raise Http404('Error, no tiene permiso para esta página')
@requires_csrf_token

def log_out(request):
    logout(request)
    return render(request, "sesiones/logout.html")

