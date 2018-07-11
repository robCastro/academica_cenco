# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from time import strftime
from django.contrib.auth.models import User
from django.db import models



class Empleado (models.Model):
    codigo = models.AutoField(primary_key=True)
    username = models.OneToOneField(User,blank=True,null=True,on_delete=models.CASCADE)
    nombre = models.CharField(max_length=40)
    apellido = models.CharField(max_length=40)
    direccion = models.TextField()
    correo = models.EmailField(blank=True)
    fechaNacimiento = models.DateField()
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
    username = models.OneToOneField(User,blank=True,null=True,on_delete=models.CASCADE)
    nombre = models.CharField(max_length=40)
    apellido = models.CharField(max_length=40)
    direccion = models.TextField()
    correo = models.EmailField(blank=True, null=True)
    fechaNacimiento = models.DateField()
    dui = models.CharField(max_length=10, blank=True, null=True)
    encargado = models.ForeignKey(Encargado, on_delete=models.PROTECT, null=True, blank=True)
    grupo = models.ForeignKey(Grupo, on_delete=models.PROTECT)

    def __unicode__(self):
        return self.nombre + " " + self.apellido

    class Meta:
        permissions = (
            ("ver_alumno", "Ver alumno"),
        )

TIPOS_CHOICES = (('casa','Casa',),('trabajo','Trabajo',),('movil', 'Movil',))
class Telefono (models.Model):
    codigo = models.AutoField(primary_key=True)
    numero = models.CharField(max_length=8, null=False,blank=False)
    alumno = models.ForeignKey(Alumno, on_delete=models.CASCADE, null=True, blank=True)
    encargado = models.ForeignKey(Encargado, on_delete=models.CASCADE, null=True, blank=True)
    empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE, null=True, blank=True)
    tipo = models.CharField(max_length=20,choices=TIPOS_CHOICES)

    def __unicode__(self):
        return self.numero