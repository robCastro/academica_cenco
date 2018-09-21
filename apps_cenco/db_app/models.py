# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from time import strftime
from django.contrib.auth.models import User
from django.db import models


class Empleado (models.Model):
    codigo = models.AutoField(primary_key=True)
    username = models.OneToOneField(User, blank=True, null=True, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=40)
    apellido = models.CharField(max_length=40)
    direccion = models.TextField()
    correo = models.EmailField(blank=True)
    dui = models.CharField(max_length=10)
    isss = models.CharField(max_length=9)
    afp = models.CharField(max_length=12)
    nit = models.CharField(max_length=17)
    opciones_tipo = (
        ('Asi', 'Asistente'),
        ('Pro', 'Profesor'),
        ('Tec', 'Tecnico')
    )
    tipo = models.CharField(max_length=3, choices=opciones_tipo, default='Pro')

    opciones_estado=(
        ('activo','activo'),
        ('inactivo', 'inactivo')
    )

    estado=models.CharField(max_length=8, choices=opciones_estado, default='activo')

    def __unicode__(self):
        return self.nombre + " " + self.apellido


class Horario (models.Model):
    dias = (
        ('Lunes y Miercoles', 'Lunes y Miercoles'),
        ('Martes y Jueves', 'Martes y Jueves'),
        ('Domingo', 'Domingo'),
        ('Sabado', 'Sabado'),
        ('Viernes', 'Viernes')
    )
    codigo = models.AutoField(primary_key=True)
    dias_asignados = models.CharField(max_length=40, choices=dias)
    hora_inicio = models.TimeField(auto_now=False, auto_now_add=False)
    hora_fin = models.TimeField(auto_now=False, auto_now_add=False)
    cantidad_alumnos = models.IntegerField(default=0, blank=True)

    def __unicode__(self):
        acronimo = ""
        for i in self.dias_asignados.split(" "):
            acronimo += i[0]+" "
        # La I es para especificar un formato de 12 horas, la base tiene los registros en 24 horas.
        acronimo += " de " + self.hora_inicio.strftime("%I:%M") + " a " + self.hora_fin.strftime("%I:%M")
        return acronimo


class Grupo(models.Model):
    codigo = models.AutoField(primary_key=True)
    fechaInicio = models.DateField()
    alumnosInscritos = models.IntegerField(default=0)
    # activo_grupo = models.BooleanField(default=True)
    # foreign keys
    horario = models.ForeignKey(Horario, on_delete=models.PROTECT)
    profesor = models.ForeignKey(Empleado, on_delete=models.PROTECT, blank=False)

    def __unicode__(self):
        return self.horario.__unicode__() + " (" + str(self.codigo) + ")"


class Encargado (models.Model):
    codigo = models.AutoField(primary_key=True)
    username = models.OneToOneField(User, blank=True, null=True, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=40)
    apellido = models.CharField(max_length=40)
    direccion = models.TextField()
    correo = models.EmailField(blank=True, null=True)
    dui = models.CharField(max_length=10, blank=True, null=True)

    def __unicode__(self):
        return self.nombre + " " + self.apellido


class Alumno (models.Model):
    codigo = models.AutoField(primary_key=True)
    username = models.OneToOneField(User, blank=True, null=True, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=40)
    apellido = models.CharField(max_length=40)
    direccion = models.TextField()
    correo = models.EmailField(blank=True, null=True)
    fechaNacimiento = models.DateField()
    dui = models.CharField(max_length=10, blank=True, null=True)
    solvente = models.BooleanField(default=False)
    # foreign keys
    encargado = models.ForeignKey(Encargado, on_delete=models.PROTECT, null=True, blank=True)
    opciones_estado = (
        ('activo', 'activo'),
        ('inactivo', 'inactivo')
    )

    estado = models.CharField(max_length=8, choices=opciones_estado, default='activo')
    def __unicode__(self):
        return self.nombre + " " + self.apellido

    class Meta:
        permissions = (
            ("ver_alumno", "Ver alumno"),
        )


class Telefono (models.Model):
    TIPOS_CHOICES = (('casa', 'Casa',), ('trabajo', 'Trabajo',), ('movil', 'Movil',))
    codigo = models.AutoField(primary_key=True)
    numero = models.CharField(max_length=8, null=False, blank=False)
    alumno = models.ForeignKey(Alumno, on_delete=models.CASCADE, null=True, blank=True)
    encargado = models.ForeignKey(Encargado, on_delete=models.CASCADE, null=True, blank=True)
    empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE, null=True, blank=True)
    tipo = models.CharField(max_length=20, choices=TIPOS_CHOICES)

    def __unicode__(self):
        return self.numero


# Modelos Agregados en Sprint 2

class Inscripcion(models.Model):
    codigo_ins = models.AutoField(primary_key=True)
    fecha_inscripcion = models.DateField()
    actual_inscripcion = models.BooleanField(default=True)
    # foreign keys
    alumno = models.ForeignKey(Alumno, on_delete=models.PROTECT, null=False, blank=False)
    grupo = models.ForeignKey(Grupo, on_delete=models.PROTECT, null=True, blank=True)


class Asistencia(models.Model):
    codigo_asistencia = models.AutoField(primary_key=True)
    fecha_asistencia = models.DateField()
    asistio = models.BooleanField(default=False)
    # foreign keys
    inscripcion = models.ForeignKey(Inscripcion, on_delete=models.CASCADE, null=False, blank=False)


class Estado(models.Model):
    codigo_estado = models.AutoField(primary_key=True)
    tipo_estado = models.CharField(max_length=20, null=False, blank=False)

    def __unicode__(self):
        return self.tipo_estado


class DetalleEstado(models.Model):
    codigo_detalle_e = models.AutoField(primary_key=True)
    fecha_detalle_e = models.DateField()
    actual_detalle_e = models.BooleanField(default=True)
    # foreign keys
    alumno = models.ForeignKey(Alumno, on_delete=models.CASCADE, null=False, blank=False)
    estado = models.ForeignKey(Estado, on_delete=models.CASCADE, null=False, blank=False)

    def __unicode__(self):
        return self.alumno.__unicode__() + " "+ self.estado.__unicode__() + " " + str(self.actual_detalle_e)


class Carrera(models.Model):
    codigo_carrera = models.AutoField(primary_key=True)
    nombre_carrera = models.CharField(max_length=20, null=False, blank=False)
    descripcion_carrera = models.CharField(max_length=200, null=False, blank=False)
    cuota_semanal_carrera = models.DecimalField(max_digits=10, decimal_places=2)
    precio_inscripcion_carrera = models.DecimalField(max_digits=10, decimal_places=2)


class Materia(models.Model):
    codigo_materia = models.AutoField(primary_key=True)
    nombre_materia = models.CharField(max_length=20, null=False, blank=False)
    descripcion_materia = models.CharField(max_length=200, null=False, blank=False)


class DetallePensum(models.Model):
    codigo_detalle_p = models.AutoField(primary_key=True)
    # foreign keys
    materia = models.ForeignKey(Materia, on_delete=models.PROTECT, null=False, blank=False)
    carrera = models.ForeignKey(Carrera, on_delete=models.PROTECT, null=False, blank=False)


class Documento(models.Model):
    codigo_doc = models.AutoField(primary_key=True)
    nombre_doc = models.CharField(max_length=20, null=False, blank=False)
    descripcion_doc = models.CharField(max_length=200, null=False, blank=False)
    archivo = models.FileField()
    # foreign keys
    materia = models.ForeignKey(Materia, on_delete=models.PROTECT, null=False, blank=False)


class Expediente(models.Model):
    codigo_expediente = models.AutoField(primary_key=True)
    activo_expediente = models.BooleanField(default=True)
    fecha_inicio_exp = models.DateField()
    fecha_proximo_pago_exp = models.DateField()
    pagado_hasta = models.DateField()
    # foreign keys
    alumno = models.ForeignKey(Alumno, on_delete=models.PROTECT, null=True)
    carrera = models.ForeignKey(Carrera, on_delete=models.PROTECT, null=True)


class Cursa(models.Model):
    codigo_cursa = models.AutoField(primary_key=True)
    Nota_final = models.DecimalField(max_digits=6, decimal_places=4)
    # foreign keys
    materia = models.ForeignKey(Materia, on_delete=models.PROTECT, null=False, blank=False)
    alumno = models.ForeignKey(Alumno, on_delete=models.PROTECT, null=False, blank=False)


class Evaluacion(models.Model):
    codigo_evaluacion = models.AutoField(primary_key=True)
    nombre_eval = models.CharField(max_length=100, null=False, blank=False)
    ponderacion = models.DecimalField(max_digits=6, decimal_places=4)
    # foreign keys
    cursa = models.ForeignKey(Cursa, on_delete=models.PROTECT, null=True)


class Colegiatura(models.Model):
    codigo_colegiatura = models.AutoField(primary_key=True)
    cuota_semanal = models.DecimalField(max_digits=10, decimal_places=2)
    forma_pago = models.CharField(max_length=100, null=False, blank=False)
    actual_colegiatura = models.BooleanField(default=True)
    # foreign keys
    expediente = models.ForeignKey(Expediente, on_delete=models.PROTECT, null=False, blank=False)


class DetallePago(models.Model):
    codigo_detalle_pago = models.AutoField(primary_key=True)
    fecha_pago = models.DateField()
    monto_pago = models.DecimalField(max_digits=10, decimal_places=2)
    cancelado = models.BooleanField(default=False)
    cantidad_semanas = models.IntegerField(blank=False)
    # foreign keys
    colegiatura = models.ForeignKey(Colegiatura, on_delete=models.PROTECT, null=False, blank=False)
