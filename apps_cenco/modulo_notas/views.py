# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
import traceback
from decimal import Decimal

from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import render, get_object_or_404

# Create your views here.
from apps_cenco.db_app.models import Empleado, Grupo, Alumno, Inscripcion, Cursa, Materia, Evaluacion, Examen
# from apps_cenco.modulo_notas.forms import CrearEditarExamenForm


def ingresar_nota(request, id_grupo):
    if request.user.groups.filter(name="Profesor").exists():
        empleado = get_object_or_404(Empleado, username=request.user)
        # consulta las MATERIAS que CURSAN los ALUMNOS con DETALLE(activos o inscritos) con INSCRIPCION en un GRUPO.
        materias = Materia.objects.raw(
            'Select codigo_materia, nombre_materia '
            'from db_app_materia as m inner join db_app_cursa as c '
            'on m.codigo_materia = c.materia_id inner join db_app_alumno as a '
            'on c.alumno_id = a.codigo inner join db_app_inscripcion as i '
            'on i.alumno_id = c.alumno_id inner join db_app_grupo as g '
            'on i.grupo_id = ' + id_grupo + ' inner join db_app_detalleestado as d '
            'on d.alumno_id = a.codigo '
            'where d.estado_id between 1 and 2 '
            'group by codigo_materia order by codigo_materia')
        if request.method == 'POST':
            try:
                # form = CrearEditarEvaluacionForm(request.POST)
                json_alumnos = json.loads(request.POST.get('JSONdata'))
                materia = request.POST.get('materia')
                examen = request.POST.get('examen')
                counter = 0
                for d in json_alumnos:
                    evaluacion = Evaluacion()
                    evaluacion.profesor = empleado
                    alumno = Alumno.objects.get(pk=d)
                    cursa = Cursa.objects.get(alumno=alumno, materia=materia)
                    evaluacion.nota_evaluacion = json_alumnos[d]
                    evaluacion.cursa = cursa
                    examen_instance = Examen.objects.get(pk=examen)
                    try:
                        Evaluacion.objects.get(examen= examen_instance, cursa=cursa)
                        return HttpResponse("Ya ha ingresado calificaciones de estos alumnos para el evaluado seleccionado", status=500)
                    except Exception:
                        evaluacion.examen = examen_instance
                        valor_nota = Decimal(examen_instance.ponderacion_examen) * Decimal(evaluacion.nota_evaluacion)
                        cursa.nota_final += valor_nota
                        evaluacion.save()
                        cursa.save()
                        counter += 1
                return HttpResponse(counter.__str__() + ' calificaciones han sido ingresadas con exito.')

            except Exception as e:
                print (e)
                traceback.print_exc()
                return HttpResponse('Ha ocurrido un error procesando la solicitud. Intente de nuevo mas tarde.', status=500)

        else:
            inscripciones = Inscripcion.objects.raw(
                'select codigo_ins, a.codigo, a.nombre, a.apellido, c.materia_id, m.nombre_materia '
                'from db_app_inscripcion as i inner join db_app_alumno as a '
                'on a.codigo = i.alumno_id inner join db_app_detalleestado as d '
                'on d.alumno_id = a.codigo inner join db_app_cursa as c '
                'on a.codigo = c.alumno_id inner join db_app_materia as m '
                'on m.codigo_materia = c.materia_id '
                'where d.estado_id between 1 and 2 and i.grupo_id = ' + id_grupo + ' and d.actual_detalle_e = True')
            grupo = Grupo.objects.get(pk=id_grupo)
            examenes = Examen.objects.all()

            context = {'inscripciones': inscripciones, 'mats': materias, 'grupo':grupo, 'examenes': examenes}
            return render(request, 'modulo_notas/ingresar_modificar_notas.html', context)
    else:
        return HttpResponseForbidden('No tiene permiso para ver este contenido')


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




