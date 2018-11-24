# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
import traceback

from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404

# Create your views here.
from apps_cenco.db_app.models import Empleado, Grupo, Alumno, Inscripcion, Cursa, Materia, Evaluacion
from apps_cenco.modulo_notas.forms import CrearEditarEvaluacionForm


def ingresar_nota(request, id_grupo):
    empleado = get_object_or_404(Empleado, username=request.user)
    materias = Materia.objects.raw(
        'Select codigo_materia, nombre_materia '
        'from db_app_materia inner join db_app_cursa on codigo_materia = materia_id '
        'group by codigo_materia order by codigo_materia')
    all_cursa = Cursa.objects.all()
    if request.method == 'POST':
        try:
            form = CrearEditarEvaluacionForm(request.POST)
            json_alumnos = json.loads(request.POST.get('JSONdata'))
            materia = request.POST.get('materia')
            if form.is_valid():
                counter = 0
                lista = []
                for d in json_alumnos:
                    print json_alumnos[d]
                    evaluacion = Evaluacion(**form.cleaned_data)
                    evaluacion.profesor = empleado
                    alumno = Alumno.objects.get(pk=d)
                    cursa = Cursa.objects.get(alumno=alumno, materia= materia)
                    evaluacion.nota_evaluacion = json_alumnos[d]
                    evaluacion.cursa = cursa
                    evaluacion.save()
                    counter +=1
                # Evaluacion.objects.bulk_create(lista)
                return HttpResponse(counter.__str__() + ' calificaciones han sido ingresadas con exito.')
            else:
                print (form.errors)
                return HttpResponse('Se recibieron datos incorrectos', status=500)
        except Exception as e:
            print (e)
            traceback.print_exc()
            return HttpResponse('Ha ocurrido un error procesando la solicitud. Intente de nuevo mas tarde.', status=500)

    else:
        inscripciones = Inscripcion.objects.filter(grupo=id_grupo)
        for i in inscripciones:
            for c in all_cursa:
                if i.alumno == c.alumno:
                    i.materia = c.materia

        form = CrearEditarEvaluacionForm()
        context = {'inscripciones': inscripciones, 'form': form, 'mats': materias, 'id_grupo':id_grupo}
        return render(request, 'modulo_notas/ingresar_modificar_notas.html', context)


# def modificar_nota(request):
#     empleado = get_object_or_404(Empleado, username=request.user)
#     if request.method == 'POST':
#
#     else:
#
#

def ver_record_notas(request):
    dummy = 's'


def finalizar_materia(request):
    dummy = 's'




