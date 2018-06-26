# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from datetime import datetime

from django.contrib.auth.decorators import permission_required, login_required
from django.shortcuts import render,redirect
from django.http import Http404

# Create your views here.
from apps_cenco.modulo_alumnos.forms import ModificarAlumnoForm
from apps_cenco.db_app.models import Alumno,Telefono

@login_required
@permission_required('db_app.change_alumno')
def modificar_alumno(request,id_alumno):
   if request.user.groups.filter(name="Asistente").exists():
    try:
        alumno = Alumno.objects.get(pk=id_alumno)
        telAlum = Telefono.objects.filter(alumno=alumno).count()
        telEnc = Telefono.objects.filter(encargado=alumno.encargado).count()
    except Alumno.DoesNotExist:
        raise Http404('Alumno no Existe')

    if request.method == 'POST':
        form = ModificarAlumnoForm(request.POST,instance=alumno)
        if form.is_valid():
            form.save()
            return redirect('detalle_alumno', alumno.pk)
    else:
        form = ModificarAlumnoForm(instance=alumno)
    edad = int((datetime.now().date() - alumno.fechaNacimiento).days / 365.25)
    context = {"alumno": alumno, "form": form,"edad": edad,"telAlum":telAlum,"telEnc":telEnc}
    return render(request, 'modulo_alumnos/modificar_alumno.html',context)
   else:
       raise Http404('Error')

@login_required
@permission_required('db_app.ver_alumno')
def ver_alumno_propio(request):
   if request.user.groups.filter(name="Alumno").exists():
    try:
        alumno = Alumno.objects.get(username=request.user)
        telAlum = Telefono.objects.filter(alumno=alumno).count()
        telEnc = Telefono.objects.filter(encargado=alumno.encargado).count()
        if telAlum :
            telefonos=Telefono.objects.filter(alumno=alumno)
        else:
            telefonos=0
    except Alumno.DoesNotExist:
        raise Http404('Alumno no Existe')

    edad = int((datetime.now().date() - alumno.fechaNacimiento).days / 365.25)
    context = {"alumno": alumno,"edad": edad,"telAlum":telAlum,"telEnc":telEnc,"telefonos":telefonos}
    return render(request, 'modulo_alumnos/ver_alumno_propio.html',context)
   else:
     raise Http404('Error')