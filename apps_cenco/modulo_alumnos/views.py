# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import User

from datetime import datetime
import time

from apps_cenco.modulo_asistencia.views import insertarFechasMetricasEstado

from django.contrib.auth.decorators import permission_required, login_required
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render,redirect
from django.http import Http404, HttpResponseRedirect, HttpResponseForbidden
import sys
from django.contrib.auth.models import Group
from apps_cenco.db_app.models import Alumno, DetalleEstado, Estado, Inscripcion, MetricaEstado
from apps_cenco.modulo_alumnos.forms import InsertarAlumnoForm, CrearEncargadoForm, TelefonoForm
from django.shortcuts import render
from django.template import loader
from django.http import Http404, HttpResponse, JsonResponse,HttpResponseServerError
from apps_cenco.db_app.models import Telefono, Grupo, Horario, Encargado

from apps_cenco.modulo_alumnos.forms import ModificarAlumnoForm
from apps_cenco.db_app.models import Alumno,Telefono
from datetime import datetime


from io import BytesIO
from reportlab.pdfgen import canvas
from django.views.generic import View
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from django.conf import settings

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
        elif 'desactivar' in request.POST:
            alumno = Alumno.objects.get(pk=id_alumno)
            detalleEstado = DetalleEstado.objects.get(alumno=alumno, actual_detalle_e=True)
            detalleEstado.actual_detalle_e=False
            detalleEstado.save()
            DetalleEstado.objects.create(fecha_detalle_e=datetime.now().date(),actual_detalle_e=True,alumno=alumno,estado=Estado.objects.get(tipo_estado='Inactivo'))
            inscripcion = Inscripcion.objects.filter(alumno=alumno, actual_inscripcion=True).first()
            inscripcion.actual_inscripcion = False
            inscripcion.save()
            #grupo=Grupo.objects.get(codigo=alumno.grupo.codigo)
            grupo = inscripcion.grupo
            grupo.alumnosInscritos=grupo.alumnosInscritos-1
            grupo.save()
            grupo.horario.cantidad_alumnos=grupo.horario.cantidad_alumnos-1
            grupo.horario.save()
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

            #activar y desactivar
            try:
                detalleEstado = DetalleEstado.objects.get(alumno=alumno,actual_detalle_e=True)
                estado=detalleEstado.estado.tipo_estado
            except:
                estado=None
            print estado
            context={
                'edad':edad,
                'alumno':alumno,
                'form': form,
                'telefonos': telefonos,
                'telAlum': telAlum,
                'estado':estado,
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

        insertarFechasMetricasEstado()

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
            #validando existencia de encargado
            if codEncargado != "-1":              #codigo -1 es para alumnos independientes
                try:
                    encargado = Encargado.objects.get(codigo=codEncargado)
                except Encargado.DoesNotExist:
                    mensaje = "Error en guardado de alumno, Encargado invalido."
                    print mensaje
                    respuesta = {
                        'mensaje' : mensaje
                    }
                    return JsonResponse(respuesta, status=500)

            #validando existencia de grupo
            try:
                grupo = Grupo.objects.get(codigo=codGrupo)
            except Grupo.DoesNotExist:
                mensaje = "Error en guardado de alumno, Grupo invalido."
                print mensaje
                respuesta = {
                    'mensaje': mensaje
                }
                return JsonResponse(respuesta, status=500)
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
                                           fechaNacimiento=fechaNacimientoConFormato, correo=correo, dui=dui,encargado=encargado)
            else:
                alumno = Alumno.objects.create(username=usuario, nombre=nombre, apellido=apellido, direccion=direccion,
                                               fechaNacimiento=fechaNacimientoConFormato, correo=correo, dui=dui)
            alumno.save()

            #inscripcion
            inscripcion = Inscripcion.objects.create(fecha_inscripcion=datetime.now(), actual_inscripcion=True, alumno = alumno, grupo = grupo)
            inscripcion.save()

            #estado
            estado = Estado.objects.filter(tipo_estado="Inscrito").first()
            detalle_estado = DetalleEstado.objects.create(fecha_detalle_e = datetime.now(), actual_detalle_e=True, estado = estado, alumno = alumno)
            detalle_estado.save()

            #Metrica Estado
            fechaHoy = datetime.now()
            fechaAux = datetime(fechaHoy.year, fechaHoy.month, 1)
            metrica_estado_inscrito = MetricaEstado.objects.filter(fecha_metrica=fechaAux, estado=estado).first()
            metrica_estado_inscrito.cantidad = metrica_estado_inscrito.cantidad + 1
            metrica_estado_inscrito.save()

            #Cantidades en grupos y horarios
            grupo.horario.cantidad_alumnos = grupo.horario.cantidad_alumnos + 1
            grupo.horario.save()
            grupo.alumnosInscritos = grupo.alumnosInscritos + 1
            grupo.save()

            #Guardando telefono
            if numero != "":
                telefono = Telefono.objects.create(numero=numero, tipo=tipo, alumno=alumno)
                telefono.save()
            mensaje = "Alumno Inscrito, Usuario: " + strUsuario + " Contraseña: " + fechaNacimiento
            respuesta = {
                'mensaje': mensaje
            }
            return JsonResponse(respuesta, status=200)
        else:
            grupos = Grupo.objects.all().order_by('-codigo').filter(activo_grupo = True)
            cantidadGrupos = Grupo.objects.all().filter(activo_grupo = True).count()
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
            raise Http404('Error, acceso solo mediante POST')
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

@login_required
def modificar_alumno2(request, id_alumno):
    import sys
    reload(sys)
    sys.setdefaultencoding('utf-8')
    if request.user.groups.filter(name="Asistente").exists():
        try:
            alumno = Alumno.objects.get(codigo = id_alumno)
        except Alumno.DoesNotExist:
            raise Http404("Alumno no existe")

        fechaFormatoEspecial =  alumno.fechaNacimiento.strftime("%d/%m/%Y")
        cantidadtelefonos = Telefono.objects.filter(alumno=alumno).count()
        hoy = datetime.now()
        esMenor = hoy.year < alumno.fechaNacimiento.year + 18 or hoy.month < alumno.fechaNacimiento.month or hoy.day < alumno.fechaNacimiento.day

        cantidadEncargados = Encargado.objects.all().count() #para validar busquedas o cambios de Indep a Dep
        encargados = Encargado.objects.all()
        if alumno.encargado != None:
            notifTelefonoEnc = Telefono.objects.all().filter(encargado = alumno.encargado).count() == 0,
        else:
            notifTelefonoEnc = False
        context = {
            "alumno" : alumno,
            "encargado" : alumno.encargado,
            "fechaNac" : fechaFormatoEspecial,
            "notifTelefono" : cantidadtelefonos == 0,
            "notifDui" : not esMenor and alumno.dui == "",
            "notifCorreo" : alumno.correo == "",
            "notifTelEnc" : notifTelefonoEnc,
            "esDependiente" : alumno.encargado != None,
            "cantidadEncargados" : cantidadEncargados,
            "encargados" : encargados,
        }
        return render(request, "modulo_alumnos/modificar_alumno2.html", context)
    else:
        raise Http404("No tiene permisos para esta pagina")

@login_required
def guardarModificacionAlumnoDependiente(request):
    import sys
    reload(sys)
    sys.setdefaultencoding('utf-8')
    if request.user.groups.filter(name="Asistente").exists():
        if request.method == "POST":
            #guardando datos generales de alumno
            codigo = request.POST.get('codigo')
            try:
                alumno = Alumno.objects.get(codigo=codigo)
            except Alumno.DoesNotExist:
                raise Http404("Alumno no existe")
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
                alumno.encargado = None
            else:
                print "será Dep"
                cambiarEncargado = request.POST.get('cambiarEncargado')
                if cambiarEncargado == "true":
                    print "se cambiara encargado"
                    codNuevoEncargado = request.POST.get('codNuevoEncargado')
                    if codNuevoEncargado == "":
                        mensaje = "Error, no seleccionó un nuevo encargado."
                        return HttpResponse(mensaje, status=500)
                    try:
                        nuevoEncargado = Encargado.objects.get(codigo=codNuevoEncargado)
                    except Encargado.DoesNotExist:
                        mensaje = "Nuevo Encargado no existe, refresque pagina y escoja de nuevo por favor."
                        print mensaje
                        return HttpResponse(mensaje, status=500)
                    alumno.encargado = nuevoEncargado
                else:
                    print "NO se cambiara encargado"

            alumno.save()

            return HttpResponse(status=200)
        else:
            raise Http404
    else:
        raise Http404("No tiene permisos para esta pagina")

@login_required
def guardarModificacionAlumnoIndependiente(request):
    mensaje = ""
    import sys
    reload(sys)
    sys.setdefaultencoding('utf-8')
    if request.user.groups.filter(name="Asistente").exists():
        if request.method == "POST":
            codigo = request.POST.get('codigo')
            try:
                alumno = Alumno.objects.get(codigo=codigo)
            except Alumno.DoesNotExist:
                raise Http404("Alumno no existe")
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

            codEncargado = request.POST.get('codEncargado')
            if codEncargado != "":
                try:
                    encargado = Encargado.objects.get(codigo = codEncargado)
                except Encargado.DoesNotExist:
                    mensaje = "Este encargado no existe, favor refrescar e intentar de nuevo."
                    print mensaje
                    return HttpResponse(mensaje, status=500, content_type="text/plain")
                alumno.encargado = encargado
            alumno.save()
        else:
            raise Http404("Pagina solo para metodos POST")
        print "Guardar Indep"
        return HttpResponse(status=200)
    else:
        raise Http404("No tiene permisos para esta pagina")
@login_required
def ConstanciaEstudioPDF(request):
    if request.user.groups.filter(name="Alumno").exists():
        #def get(self, request, *args, **kwargs):
            # Indicamos el tipo de contenido a devolver, en este caso un pdf
            response = HttpResponse(content_type='application/pdf')
            # La clase io.BytesIO permite tratar un array de bytes como un fichero binario, se utiliza como almacenamiento temporal
            buffer = BytesIO()
            # Canvas nos permite hacer el reporte con coordenadas X y Y
            pdf = canvas.Canvas(buffer)
            # Llamo al método cabecera donde están definidos los datos que aparecen en la cabecera del reporte.
            #self.cabecera(pdf)
            # Con show page hacemos un corte de página para pasar a la siguiente

        #def cabecera(self, pdf):
            # Utilizamos el archivo logo_django.png que está guardado en la carpeta media/imagenes
            archivo_imagen = settings.MEDIA_ROOT + 'static/img/encabezado.png'
            # Definimos el tamaño de la imagen a cargar y las coordenadas correspondientes
            pdf.drawImage(archivo_imagen, 40, 750, 120, 90, preserveAspectRatio=True)
            # Establecemos el tamaño de letra en 16 y el tipo de letra Helvetica
            pdf.setFont("Helvetica", 16)
            # Dibujamos una cadena en la ubicación X,Y especificada
            pdf.drawString(180, 790, u"CENTRO DE ENSEÑANZA EN COMPUTACIÓN")
            pdf.setFont("Helvetica", 14)
            alum = Alumno.objects.get(username=request.user)
            nom=alum.nombre+" "+alum.apellido
            pdf.drawString(75, 745, u"A quien corresponda: ")
            pdf.drawString(75, 710, u"El que suscribe, Director de esta institución, hace CONSTAR: ")
            pdf.drawString(75, 695, u"Que ")
            pdf.drawString(105, 695, nom)

            y=(nom.__len__()*7)+110

            dui = alum.dui
            if dui.__len__()==10:
                pdf.drawString(y, 695, u"con dui: ")
                pdf.drawString(y+54, 695, dui)
                pdf.drawString(y + 134, 695, u"es estudiante" )
                pdf.drawString(75, 680, u"de la carrera ")
                pdf.drawString(75, 665, u"en el horario de: ")

            else:
                pdf.drawString(y, 695, u"es estudiante de la institución cursando")
                pdf.drawString(75, 680, u"la carrera ")
                pdf.drawString(75, 665, u"en el horario de: ")

            pdf.drawString(75, 635, u"Para los fines que al interesado le convengan se extiende la presente")

            ahora = str((datetime.now().date()))
            dia= "el dia "+ahora
            pdf.drawString(75, 620, dia)











            pdf.showPage()
            pdf.save()
            pdf = buffer.getvalue()
            buffer.close()
            response.write(pdf)
            return response

    else:
        return HttpResponseForbidden('No tiene permiso para esta pagina', status=403)





@login_required
def constancias(request):
   if request.user.groups.filter(name="Alumno").exists():

    return render(request, 'modulo_alumnos/constancias.html')
   else:
     raise Http404('Error, no tiene permiso para esta página')
