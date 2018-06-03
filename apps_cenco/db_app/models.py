# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models

# Create your models here.
class Empleado (models.Model):
    codigo = models.AutoField(primary_key=True)
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

class Grupo(models.Model):
    codigo = models.AutoField(primary_key=True)
    opciones_horario = (
        ('Por la mañana',(
            ('L y M 7 - 9', 'Lunes y Miercoles, 7 a 9'),
            ('L y M 9 - 11', 'Lunes y Miercoles, 9 a 11'),
            ('M y J 7 - 9', 'Martes y Jueves, 7 a 9'),
            ('M y J 9 - 11', 'Martes y Jueves, 9 a 11'),
            ('S 7 - 11', 'Sabados 7 a 11'),
            ('D 7 - 11', 'Domingos 7 a 11')
        )
        ),
        ('Por la tarde',(
            ('L y M 1 - 3', 'Lunes y Miercoles, 1:30 a 3:30'),
            ('L y M 3 - 5', 'Lunes y Miercoles, 3:30 a 5:30'),
            ('M y J 1 - 3', 'Martes y Jueves, 1:30 a 3:30'),
            ('M y J 3 - 5', 'Martes y Jueves, 3:30 a 5:30'),
            ('S 1 - 5', 'Sabados 1:30 a 5:30'),
        )
        )
    )
    horario = models.CharField(max_length=11, choices=opciones_horario)
    fechaInicio = models.DateField()
    profesor = models.ForeignKey(Empleado, on_delete=models.PROTECT, blank=False)
    def __unicode__(self):
        return self.horario

class Encargado (models.Model):
    codigo = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=40)
    apellido = models.CharField(max_length=40)
    direccion = models.TextField()
    correo = models.EmailField(blank=True)
    fechaNacimiento = models.DateField()
    dui = models.CharField(max_length=10)
    def __unicode__(self):
        return self.nombre + " " + self.apellido

class Alumno (models.Model):
    codigo = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=40)
    apellido = models.CharField(max_length=40)
    direccion = models.TextField()
    correo = models.EmailField(blank=True)
    fechaNacimiento = models.DateField()
    dui = models.CharField(max_length=10, blank=True)
    encargado = models.ForeignKey(Encargado, on_delete=models.PROTECT)
    grupo = models.ForeignKey(Grupo, on_delete=models.PROTECT)
    def __unicode__(self):
        return self.nombre + " " + self.apellido


class Telefono (models.Model):
    numero = models.CharField(max_length=8, primary_key=True)
    alumno = models.ForeignKey(Alumno, on_delete=models.CASCADE, null=True, blank=True)
    encargado = models.ForeignKey(Encargado, on_delete=models.CASCADE, null=True, blank=True)
    empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE, null=True, blank=True)
    def __unicode__(self):
        return self.numero