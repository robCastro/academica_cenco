# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import User

from datetime import datetime

from django.contrib.auth.decorators import permission_required, login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render,redirect
from django.http import Http404, HttpResponseRedirect
import sys
from django.contrib.auth.models import Group
from apps_cenco.db_app.models import Alumno
from apps_cenco.modulo_alumnos.forms import InsertarAlumnoForm, CrearEncargadoForm, TelefonoForm
from django.shortcuts import render
from django.template import loader
from django.http import Http404, HttpResponse, JsonResponse,HttpResponseServerError
from apps_cenco.db_app.models import Telefono, Grupo, Horario, Encargado

from apps_cenco.modulo_alumnos.forms import ModificarAlumnoForm
from apps_cenco.db_app.models import Alumno,Telefono

@login_required
def consultar_alumnos(request):
    if request.user.groups.filter(name="Asistente").exists():
        alumnos=Alumno.objects.order_by('codigo')
        telefonos = []

        for alumno in alumnos:
            telefonos.append(alumno.telefono_set.first())



        tipos = Horario.objects.raw("select distinct dias_asignados, 1 as codigo from db_app_horario " +
                                    "order by dias_asignados")

        page=request.GET.get('page',1)
        paginator=Paginator(alumnos,10)
        try:
            users = paginator.page(page)
        except PageNotAnInteger:
            users = paginator.page(1)
        except EmptyPage:
            users = paginator.page(paginator.num_pages)

        context = {
            'users':users,
            'alumnos': alumnos,
            'telefonos': telefonos,
            'tipos': tipos
        }

        return render(request, 'modulo_alumnos/consultar_alumnos.html', context)
    else:
        raise Http404('Error, no tiene permiso para esta página')

@login_required
def detalle_alumno(request,id_alumno):
    if request.user.groups.filter(name="Asistente").exists():
        url = "/alumnos/" + str(id_alumno)

        if 'eliminar1' in request.POST:
            alumno = Alumno.objects.get(pk=id_alumno)
            telefonos=Telefono.objects.filter(alumno=alumno)
            for telefono in telefonos:
                if request.POST.get(str(telefono.codigo)):
                    telefono.delete()

            #telefonos = Telefono.objects.order_by('alumno')
            context={
                'alumno': alumno,
                'telefonos': telefonos
            }
            return HttpResponseRedirect(url)
        elif request.method=='POST':
            if request.method == 'POST':
                alum=Alumno.objects.get(pk=id_alumno)


                num=request.POST.get('numero')
                tip=request.POST['tipo']

                telefono = Telefono(numero=num, alumno=alum, tipo=tip)
                telefono.save()
                temp = loader.get_template('modulo_alumnos/nuevo_numero.html').render({'telefono': telefono})
                return HttpResponse(temp)
            else:
                form = TelefonoForm()

            try:
                alumno = Alumno.objects.get(pk=id_alumno)
            except Alumno.DoesNotExist:
                raise Http404('Alumno no Existe')

            telefonos =Telefono.objects.order_by('alumno')

            edad = int((datetime.now().date() - alumno.fechaNacimiento).days / 365.25)
            context = {
                'alumno': alumno,
                'telefonos': telefonos,
                'form': form,
                'edad':edad,

            }
        else:
            form = TelefonoForm()
            telefonos = Telefono.objects.order_by('alumno')
            alumno = Alumno.objects.get(pk=id_alumno)
            edad = int((datetime.now().date() - alumno.fechaNacimiento).days / 365.25)
            telAlum = Telefono.objects.filter(alumno=alumno).count()
            context={
                'edad':edad,
                'alumno':alumno,
                'form': form,
                'telefonos': telefonos,
                'telAlum': telAlum,
            }
        return render(request, 'modulo_alumnos/detalle_alumno.html', context)
    else:
        raise Http404('Error, no tiene permiso para esta página')


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
       raise Http404('Error, no tiene permiso para esta página')

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
     raise Http404('Error, no tiene permiso para esta página')

@login_required
def registro_alumno(request):
    if request.user.groups.filter(name="Asistente").exists():
        if request.method == "POST":
            form = InsertarAlumnoForm(request.POST)
            form3 =TelefonoForm(request.POST)
            if form.is_valid() :
                #gererando el usuario
                nom=request.POST['nombre']
                ape = request.POST['apellido']
                nomb = " ".join(nom.split())
                nomb = nomb.split()
                apell = " ".join(ape.split())
                apell = apell.split()
                usu = str(nomb[0]) + str(apell[0])
                usu=usu.lower()
                #consulta a la base para generar correlativo
                users = User.objects.filter(username__contains=usu)

                cant=users.__len__()
                if cant==0:
                    cant=1
                else:
                    cant=cant+1
                usuario=str(usu)+str(cant)
                correo=request.POST['correo']
                contra=request.POST['fechaNacimiento']
                contra=contra.replace("-","")
                user=User.objects.create_user(username=usuario,email=correo,password=contra,first_name=nom,last_name=ape)
                user.save()
                groupEncargado = Group.objects.get(name='Alumno')
                groupEncargado.user_set.add(user)
                form.save()
                alumno = form.save(commit=False)
                alumno.username=user
                alumno.save()
                id_grupo=request.POST['grupo']
                grupo = Grupo.objects.get(pk=id_grupo)
                grupo.alumnosInscritos= grupo.alumnosInscritos+1
                id_horario= grupo.horario_id
                horario = Horario.objects.get(pk=id_horario)
                grupo.horario.cantidad_alumnos=grupo.horario.cantidad_alumnos+1
                horario.cantidad_alumnos= horario.cantidad_alumnos+1
                grupo.save()
                horario.save()
            # Aqui quizas quepa un else para cuado algo falle. Error 500 talves?

                telefono = Telefono()
                telefono.numero= request.POST['numero']
                telefono.alumno_id = alumno.codigo
                telefono.tipo = request.POST['tipo']
                telefono.save()
                return HttpResponse("Usuario: "+usuario+" Contraseña: "+contra)

        else:
            form = InsertarAlumnoForm()
            form3 = TelefonoForm()
        context = {
            "form": form,
            "form3": form3,
        }
        return render(request, "modulo_alumnos/registrar_alumnos.html", context)
    else:
        raise Http404('Error, no tiene permiso para esta página')

@login_required
def registrar_encargado(request):
    if request.user.groups.filter(name="Asistente").exists():
        if request.method == 'POST':
            form2 = CrearEncargadoForm(request.POST)
            form4 = TelefonoForm(request.POST)
            if form2.is_valid():
                nom = request.POST['nombre']
                ape = request.POST['apellido']
                nomb = " ".join(nom.split())
                nomb = nomb.split()
                apell = " ".join(ape.split())
                apell = apell.split()
                usu = str(nomb[0]) + str(apell[0])
                usu=usu.lower()
                # consulta a la base para generar correlativo
                users = User.objects.filter(username__contains=usu)

                cant = users.__len__()
                if cant == 0:
                    cant = 1
                else:
                    cant = cant + 1

                usuario = str(usu) + str(cant)
                correo = request.POST['correo']
                contra = request.POST['fechaNacimiento']
                contra = contra.replace("-", "")
                user = User.objects.create_user(username=usuario, email=correo, password=contra,first_name=nom,last_name=ape)
                user.save()
                groupEncargado = Group.objects.get(name='Encargado')
                groupEncargado.user_set.add(user)
                form2.save()
                #alumno = form2.save(commit=False)

                encargado = form2.save(commit=False)

                encargado.username = user
                encargado.save()
                id=encargado.codigo.__str__()
                nombre= encargado.nombre+" "+encargado.apellido

                telefono = Telefono()
                telefono.numero = request.POST['numero']
                telefono.encargado_id = encargado.codigo
                telefono.tipo=request.POST['tipo']
                telefono.save()
                return JsonResponse({'mensaje': "Usuario: "+usuario+" Contraseña: "+contra,'Encargado':'<option value="'+id+'">'+nombre+'</option>'})
            # Seria bueno agregar aqui un Internal Server error. Para cuando no guarde bien.

        else:
            form = InsertarAlumnoForm()
            form4 = TelefonoForm()
            context = {
                "form": form,
                "form4": form4,
            }
            return render(request, "modulo_alumnos/registrar_alumnos.html", context)
    else:
        raise Http404('Error, no tiene permiso para esta página')


def inscribirAlumno(request):
    grupos = Grupo.objects.all().order_by('-codigo')
    cantidadGrupos = Grupo.objects.all().count()
    encargados = Encargado.objects.all().order_by('nombre')
    context = {
        'grupos' : grupos,
        'cantidadGrupos' : cantidadGrupos,
        'encargados' : encargados,
    }
    return render(request, "modulo_alumnos/inscribir_alumnos.html", context)

def registrarEncargado(request):
    nombre = request.POST.get("txtNombreEncargado")
    apellido = request.POST.get("txtApellidoEncargado")
    direccion = request.POST.get("txtDireccionEncargado")
