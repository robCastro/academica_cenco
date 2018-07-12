# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import ProtectedError, Q
from django.shortcuts import render, render_to_response, redirect
from django.http import Http404, HttpResponse, JsonResponse

from apps_cenco.db_app.models import Horario

from apps_cenco.modulo_horarios.forms import CrearHorarioForm, EditarHorarioForm

import sys
reload(sys)
sys.setdefaultencoding('utf-8')


@login_required
def consultar_horario(request):
    user = User.objects.get(username=request.user)
    if user.groups.filter(name="Director").exists():
        form = CrearHorarioForm()
        form2 = EditarHorarioForm()
        horarios = Horario.objects.order_by('dias_asignados')
        tipos = Horario.objects.raw("select distinct dias_asignados, 1 as codigo from db_app_horario " +
                                    "order by dias_asignados")
        context = {'horarios': horarios, 'form': form, 'tipos': tipos, 'form2': form2}
        return render(request, "modulo_horarios/consultar_editar_horario.html", context)
    else:
        raise Http404('Error, no tiene permiso para esta página')

@login_required
def eliminar_horario(request):
    user = User.objects.get(username=request.user)
    if user.groups.filter(name="Director").exists():
        try:
            if request.method == 'POST':
                id = request.POST.get('id')
                if id != '-1':
                    horario = Horario.objects.get(codigo=id)
                    horario.delete()
                    return HttpResponse('', status=200)  # Exito
                else:
                    return HttpResponse('', status=500)
            else:
                return redirect('crud_horario')  # Intento de acceso desde la url.
        except ProtectedError:
            # Fracaso. Error de Servidor por integridad Referencial.
            return HttpResponse('', status=500)
    else:
        raise Http404('Error, no tiene permiso para esta página')

@login_required
def crear_nuevo_horario(request):
    user = User.objects.get(username=request.user)
    if user.groups.filter(name="Director").exists():
        if request.method == 'POST':
            form = CrearHorarioForm(request.POST)
            if form.is_valid():
                instancia = form.save(commit=False)
                if validar_horario(instancia, 'crear'):
                    form.save()
                    respuesta = str(instancia.codigo) + ','
                    respuesta += instancia.dias_asignados + ','
                    respuesta += str(instancia.hora_inicio.strftime("%H:%M")) + ','
                    respuesta += str(instancia.hora_fin.strftime("%H:%M")) + ','
                    respuesta += str(instancia.cantidad_alumnos)
                    return HttpResponse(respuesta, status=200)
                else:
                    # El horario choca
                    return HttpResponse('', status=500)
            else:
                return HttpResponse('', status=500)  # Se envio un form no valido
        else:
            return redirect('crud_horario')  # Intento de acceso desde la url.
    else:
        raise Http404('Error, no tiene permiso para esta página')

@login_required
def editar_horario(request):
    user = User.objects.get(username=request.user)
    if user.groups.filter(name="Director").exists():
        if request.method == 'POST':
            id = request.POST.get('id')
            try:
                horario = Horario.objects.get(codigo=id)
                horario_form = CrearHorarioForm(request.POST, instance=horario)
                if horario_form.is_valid():
                    nuevo_horario= horario_form.save(commit=False)
                    if validar_horario(nuevo_horario, 'editar'):
                        horario_form.save()
                        respuesta = str(nuevo_horario.codigo) + ','
                        respuesta += nuevo_horario.dias_asignados + ','
                        respuesta += str(nuevo_horario.hora_inicio.strftime("%H:%M")) + ','
                        respuesta += str(nuevo_horario.hora_fin.strftime("%H:%M")) + ','
                        respuesta += str(nuevo_horario.cantidad_alumnos)
                        return HttpResponse(respuesta, status=200)  # form valido y guardado con exito
                    else:
                        print('horario en conflicto')
                        return HttpResponse('', status=500)  # horario en conflicto.
                else:
                    print('form no valido')
                    return HttpResponse('', status=500)  # form no valido.

            except ObjectDoesNotExist:
                print('no encuentra el objeto')
                return HttpResponse('', status=500)  # id inexistente.
        else:
            return redirect('crud_horario')  # Intento de acceso desde la url.
    else:
        raise Http404('Error, no tiene permiso para esta página')


# Verifica que el nuevo horario o el horario modificado nunca choque con otro en el mismo día.
def validar_horario(horario, metodo):
    if metodo.__eq__('crear'):
        horarios = Horario.objects.filter(dias_asignados=horario.dias_asignados)
    elif metodo.__eq__('editar'):
        horarios = Horario.objects.filter(~Q(codigo=horario.codigo), dias_asignados=horario.dias_asignados)

    # Se recorren todos los horarios
    for h in horarios:
        # Si la hora de incio del nuevo horario esta en medio de otro horario retorna falso
        if h.hora_inicio < horario.hora_inicio < h.hora_fin:
            return False

        # Si algun horario del mismo dia queda en medio del nuevo horario retorna falso
        if horario.hora_inicio <= h.hora_inicio and h.hora_fin <= horario.hora_fin:
            return False

        # Si la hora de finalizacion del nuevo horario esta en medio de otro retorna falso
        if h.hora_inicio < horario.hora_fin < h.hora_fin:
            return False

        # Si la hora de inicio es mayor a la de finalizacion retorna falso
        if horario.hora_inicio > horario.hora_fin:
            return False

    # Si niguna condicion hizo a la funcion retornar, no hay horarios que choquen y retorna true.
    return True
