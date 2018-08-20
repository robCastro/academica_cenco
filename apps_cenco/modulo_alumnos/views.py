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
from django.shortcuts import render
from django.template import loader
from django.http import Http404, HttpResponse, JsonResponse,HttpResponseServerError
from apps_cenco.db_app.models import Telefono, Grupo, Horario, Encargado

from apps_cenco.modulo_alumnos.forms import ModificarAlumnoForm
from apps_cenco.db_app.models import Alumno,Telefono
from datetime import datetime

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

@login_required
def consultar_alumnos(request):
    if request.user.groups.filter(name="Asistente").exists():
        alumnos= Alumno.objects.all()

        for alumno in alumnos:
            alumno.primerTelefono = alumno.telefono_set.first()

        return render(request, 'modulo_alumnos/consultar_alumnos.html', {'alumnos': alumnos})
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
def inscribirAlumno(request):
    import sys
    reload(sys)
    sys.setdefaultencoding('utf-8')
    if request.user.groups.filter(name="Asistente").exists():
        if request.method == 'POST':
            mensaje = ""
            nombre = request.POST.get('nombre')
            apellido = request.POST.get('apellido')
            direccion = request.POST.get('direccion')
            fechaNacimiento = request.POST.get('fechaNacimiento')
            correo = request.POST.get('correo')
            dui = request.POST.get('dui')
            codGrupo = request.POST.get('grupo')
            codEncargado = request.POST.get('encargado')
            numero = request.POST.get('numero')
            tipo = request.POST.get('tipo')
            fechaNacimientoConFormato = datetime.strptime(fechaNacimiento, "%d/%m/%Y").date()
            print codEncargado
            #validando existencia de encargado
            if codEncargado != "-1":              #codigo -1 es para alumnos independientes
                try:
                    encargado = Encargado.objects.get(codigo=codEncargado)
                except Encargado.DoesNotExist:
                    #$ es para hacer split en JS
                    mensaje = "Error en guardado de alumno, Encargado invalido.$"
                    print mensaje
                    return HttpResponse(mensaje, status=500)

            #validando existencia de grupo
            try:
                grupo = Grupo.objects.get(codigo=codGrupo)
            except Grupo.DoesNotExist:
                mensaje = "Error en guardado de alumno, Grupo invalido.$"
                print mensaje
                return HttpResponse(mensaje, status=500)

            # generando usuario
            strUsuario = generarUsuario(nombre, apellido)
            if correo == "":
                usuario = User.objects.create(username=strUsuario, first_name=nombre, last_name=apellido)
            else:
                usuario = User.objects.create(username=strUsuario, first_name=nombre, last_name=apellido, email=correo)
            usuario.set_password(fechaNacimiento)
            usuario.save()
            groupAlumno = Group.objects.get(name='Alumno')
            groupAlumno.user_set.add(usuario)

            if codEncargado != "-1":      #cod -1 es para alumnos independientes
                alumno = Alumno.objects.create(username=usuario,nombre=nombre, apellido=apellido, direccion=direccion,
                                           fechaNacimiento=fechaNacimientoConFormato, correo=correo, dui=dui,encargado=encargado,
                                           grupo=grupo)
            else:
                alumno = Alumno.objects.create(username=usuario, nombre=nombre, apellido=apellido, direccion=direccion,
                                               fechaNacimiento=fechaNacimientoConFormato, correo=correo, dui=dui,
                                               grupo=grupo)
            alumno.save()
            grupo.horario.cantidad_alumnos = grupo.horario.cantidad_alumnos + 1
            grupo.horario.save()
            grupo.alumnosInscritos = grupo.alumnosInscritos + 1
            grupo.save()
            #Guardando telefono
            if numero != "":
                telefono = Telefono.objects.create(numero=numero, tipo=tipo, alumno=alumno)
                telefono.save()
            mensaje = "¡Alumno Inscrito! Usuario: " + strUsuario + " Contraseña: " + fechaNacimiento + "$"
            return HttpResponse(mensaje, status=200)
        else:
            grupos = Grupo.objects.all().order_by('-codigo')
            cantidadGrupos = Grupo.objects.all().count()
            encargados = Encargado.objects.all().order_by('nombre')
            context = {
                'grupos' : grupos,
                'cantidadGrupos' : cantidadGrupos,
                'encargados' : encargados,
            }
            return render(request, "modulo_alumnos/inscribir_alumnos.html", context)
    else:
        raise Http404('Error, no tiene permiso para esta página')

@login_required
def registrarEncargado(request):
    import sys
    reload(sys)
    sys.setdefaultencoding('utf-8')
    if request.user.groups.filter(name="Asistente").exists():
        if request.method == 'POST':
            nombre = request.POST.get("nombre")
            apellido = request.POST.get("apellido")
            direccion = request.POST.get("direccion")
            dui = request.POST.get("dui")
            correo = request.POST.get("correo")

            numTelefono = request.POST.get("numero")
            tipoTelefono = request.POST.get("tipo")

            strUsuario = generarUsuario(nombre, apellido)

            if correo == "":
                usuario = User.objects.create(username=strUsuario, first_name=nombre, last_name=apellido)
            else:
                usuario = User.objects.create(username=strUsuario, first_name=nombre, last_name=apellido,email=correo)
            usuario.set_password(strUsuario)
            usuario.save()
            groupEncargado = Group.objects.get(name='Encargado')
            groupEncargado.user_set.add(usuario)
            encargado = Encargado.objects.create(nombre=nombre, apellido=apellido, direccion=direccion, dui=dui, correo=correo,
                                                 username=usuario)
            encargado.save()
            if numTelefono != "":
                telefono = Telefono.objects.create(numero=numTelefono, encargado=encargado, tipo=tipoTelefono)
                telefono.save()

            respuesta = {
                'mensaje' : 'Usuario: ' + strUsuario + ' Contraseña: ' + strUsuario,
                'codEncargado' : encargado.codigo.__str__(),
                'nombreEncargado': encargado.nombre,
                'apellidoEncargado': encargado.apellido,
                'direccionEncargado': encargado.direccion
            }
            return JsonResponse(respuesta)
        else:
            return Http404('Error, acceso solo mediante POST')
    else:
        raise Http404('Error, no tiene permiso para esta página')

def generarUsuario(nom, ape):
    nomb = " ".join(nom.split())
    nomb = nomb.split()
    apell = " ".join(ape.split())
    apell = apell.split()
    usu = str(nomb[0]) + str(apell[0])
    usu = usu.lower()
    # consulta a la base para generar correlativo
    users = User.objects.filter(username__contains=usu)

    cant = users.__len__()
    if cant == 0:
        cant = 1
    else:
        cant = cant + 1
    usuario = str(usu) + str(cant)
    return usuario

@login_required
def consultar_datos_encargado(request):
    if request.user.groups.filter(name="Encargado").exists():
        encargado = Encargado.objects.get(username=request.user)
        telefonos = Telefono.objects.filter(encargado=encargado)
        context = {
            'encargado': encargado,
            'telefonos': telefonos,
        }
        return render(request, 'modulo_alumnos/encargado_misDatos.html', context)
    else:
        return HttpResponseForbidden('No tiene permiso para esta pagina', status=403)


@login_required
def consultar_datos_encargado_hijos(request):
    if request.user.groups.filter(name="Encargado").exists():
        enc = Encargado.objects.get(username=request.user)
        estudiantes = Alumno.objects.filter(encargado=enc)
        for estudiante in estudiantes:
            phone_rows = ""
            try:
                tels = Telefono.objects.filter(alumno=estudiante)
                for tel in tels:
                    phone_rows += "<tr><td>"+tel.numero+"</td><td>"+tel.tipo+"</td></tr>"
            except ObjectDoesNotExist:
                phone_rows = ""
            estudiante.telefonos = phone_rows

        context = {
            'estudiantes': estudiantes
        }
        return render(request, 'modulo_alumnos/encargado_misHijos.html', context)
    else:
        return HttpResponseForbidden('No tiene permiso para esta pagina', status=403)


def modificar_alumno2(request, id_alumno):
    try:
        alumno = Alumno.objects.get(codigo = id_alumno)
    except Alumno.DoesNotExist:
        return Http404("Alumno no existe")

    fechaFormatoEspecial =  alumno.fechaNacimiento.strftime("%d/%m/%Y")
    cantidadtelefonos = Telefono.objects.filter(alumno=alumno).count()
    hoy = datetime.now()
    esMenor = hoy.year < alumno.fechaNacimiento.year + 18 or hoy.month < alumno.fechaNacimiento.month or hoy.day < alumno.fechaNacimiento.day

    cantidadEncargados = Encargado.objects.all().count() #para validar busquedas o cambios de Indep a Dep
    encargados = Encargado.objects.all()
    context = {
        "alumno" : alumno,
        "encargado" : alumno.encargado,
        "fechaNac" : fechaFormatoEspecial,
        "notifTelefono" : cantidadtelefonos == 0,
        "notifDui" : not esMenor and alumno.dui == "",
        "notifCorreo" : alumno.correo == "",
        "esDependiente" : alumno.encargado != None,
        "cantidadEncargados" : cantidadEncargados,
        "encargados" : encargados,
    }
    return render(request, "modulo_alumnos/modificar_alumno2.html", context)

def guardarModificacionAlumnoDependiente(request):
    import sys
    reload(sys)
    sys.setdefaultencoding('utf-8')
    if request.method == "POST":
        #guardando datos generales de alumno
        codigo = request.POST.get('codigo')
        try:
            alumno = Alumno.objects.get(codigo=codigo)
        except Alumno.DoesNotExist:
            return Http404("Alumno no existe")
        nombreAl = request.POST.get('nombre')
        apellidoAl = request.POST.get('apellido')
        direccionAl = request.POST.get('direccion')
        fechaNacAl = request.POST.get('fechaNacimiento')
        fechaNacimientoConFormato = datetime.strptime(fechaNacAl, "%d/%m/%Y").date()
        duiAl = request.POST.get('dui')
        correoAl = request.POST.get('correo')

        alumno.nombre = nombreAl
        alumno.apellido = apellidoAl
        alumno.direccion = direccionAl
        alumno.fechaNacimiento = fechaNacimientoConFormato
        alumno.dui = duiAl
        alumno.correo = correoAl

        #verificando si el alumno será independiente

        hacerIndep = request.POST.get('hacerIndep')
        if hacerIndep == "true":
            #hacerlo independiente
            print "será Indep"
            #alumno.encargado = None
        else:
            print "será Dep"
            cambiarEncargado = request.POST.get('cambiarEncargado')
            if cambiarEncargado == "true":
                print "se cambiara encargado"
                codNuevoEncargado = request.POST.get('codNuevoEncargado')
                if codNuevoEncargado == "":
                    mensaje = "Error con el nuevo Encargado, refresque pagina y escoja de nuevo por favor.$"
                    return HttpResponse(mensaje, status=500)
                try:
                    nuevoEncargado = Encargado.objects.get(codigo=codNuevoEncargado)
                except Encargado.DoesNotExist:
                    mensaje = "Nuevo Encargado no existe, refresque pagina y escoja de nuevo por favor.$"
                    return HttpResponse(mensaje, status=500)
                alumno.encargado = nuevoEncargado
            else:
                print "NO se cambiara encargado"

        alumno.save()

        return HttpResponse(status=200)
    else:
        return Http404
