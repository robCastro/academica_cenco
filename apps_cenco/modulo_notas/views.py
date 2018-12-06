# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
import traceback
from decimal import Decimal

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import render, get_object_or_404

# Create your views here.
from apps_cenco.db_app.models import Empleado, Grupo, Alumno, Inscripcion, Cursa, Materia, Evaluacion, Examen, \
    Expediente, DetallePensum
# from apps_cenco.modulo_notas.forms import CrearEditarExamenForm
from apps_cenco.modulo_notas.forms import CrearEditarExamenForm


@login_required
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
#
#

@login_required
def ingresar_evaluaciones(request):
    if request.user.groups.filter(name="Director").exists():
        form = CrearEditarExamenForm()
        materias = Materia.objects.raw(
            'select m.codigo_materia, m.nombre_materia, coalesce(round(sum(ponderacion_examen)*100, 2), 0.00) '
            'as porcentaje from db_app_materia as m left join db_app_examen as e '
            'on e.materia_id = m.codigo_materia '
            'group by codigo_materia order by codigo_materia;')
        if request.method == 'POST':
            form = CrearEditarExamenForm(request.POST)
            if form.is_valid():
                examen = form.save(commit=False)
                set_exams = Examen.objects.filter(materia=examen.materia)
                porcentaje = 0
                for e in set_exams:
                    porcentaje += Decimal(e.ponderacion_examen)
                porcentaje_final = porcentaje + Decimal(examen.ponderacion_examen)
                if porcentaje_final >= 1:
                    context = {'materias': materias, 'post': True, 'alert': True,
                               'mensaje': 'No puede agregar ponderación superior a '+str(round((1-porcentaje)*100, 2))+
                                          '% para esta evaluación.'}
                    return render(request, 'modulo_notas/ingresar_evaluaciones.html', context)
                else:
                    examen.save()
                    context = {'materias': materias, 'post': True, 'mensaje': 'Evaluación agregada con exito.'}
                    return render(request, 'modulo_notas/ingresar_evaluaciones.html', context)
            else:
                context = {'materias': materias, 'post': True, 'error': True, 'mensaje': 'Se recibieron datos incorrectos.'}
                return render(request, 'modulo_notas/ingresar_evaluaciones.html', context)
        else:

            context={'materias': materias, 'form': form}
            return render(request, 'modulo_notas/ingresar_evaluaciones.html', context)
    else:
        return HttpResponseForbidden("No tiene permiso para ver este contenido")


@login_required
def consultar_evaluaciones(request):
    if request.user.groups.filter(name="Director").exists():
        examenes = Examen.objects.all().order_by('materia', 'codigo_examen')
        materias = Materia.objects.raw('Select codigo_materia, nombre_materia from db_app_materia as m '
                                       'inner join db_app_examen as e on e.materia_id = m.codigo_materia '
                                       'group by codigo_materia order by codigo_materia')
        context = {'examenes': examenes, 'materias': materias}
        return render(request, 'modulo_notas/consultar_evaluaciones.html', context)
    else:
        return HttpResponseForbidden("No tiene permiso para ver este contenido")


@login_required
def ver_record_notas(request):
    if request.user.groups.filter(name="Alumno").exists():
        alumno = Alumno.objects.get(username=request.user)
        cursa = Cursa.objects.filter(alumno=alumno).order_by('-actual_cursa')
        evaluaciones = Evaluacion.objects.filter(cursa__in=cursa)
        context = {'evaluaciones': evaluaciones, 'cursa': cursa,'alumno': alumno}
        return render(request, 'modulo_notas/consultar_record_notas.html', context)
    else:
        return HttpResponseForbidden("No tiene permiso para ver este contenido")


@login_required
def finalizar_materia(request, id_alumno):
    if request.user.groups.filter(name="Profesor").exists():
        alumno = Alumno.objects.get(pk=id_alumno)
        cursa = Cursa.objects.filter(alumno=alumno, actual_cursa=True)
        if request.method == 'POST':
            expediente = Expediente.objects.get(alumno=alumno, activo_expediente=True)
            cursa.actual_cursa = False
            detalle_pensum = DetallePensum.objects.filter(carrera=expediente.carrera)
            detalle_actual = ''
            for d in detalle_pensum:
                if d.materia == cursa.materia:
                    detalle_actual = d
                    break
            detalle_nuevo = DetallePensum.objects.get(
                carrera=detalle_actual.carrera, ordinal_materia_cursa=int(detalle_actual.ordinal_materia_cursa)+1)
            nuevo_cursa = Cursa(
                nota_final=0.0000, actual_cursa=True, alumno=alumno, materia=detalle_nuevo.materia)
            nuevo_cursa.save()
            # return render(request, '', ) Redireccionar a la lista de alumnos
        else:
            evaluaciones = Evaluacion.objects.filter(cursa=cursa)
            context = {'evaluaciones': evaluaciones, 'cursa': cursa}
            return render(request, 'modulo_notas/finalizar_materia.html', context)
    else:
        return HttpResponseForbidden("No tiene permiso para ver este contenido")

