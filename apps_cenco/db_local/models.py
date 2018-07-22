# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import os
appname = os.path.dirname(__file__).split('/')[-1]

# Create your models here.


class FooterINFO(models.Model):

    db = appname
    codigo = models.AutoField(primary_key=True)
    telefono = models.CharField(max_length=8, null=False,blank=False)
    correo = models.EmailField(blank=True, null=True)
    direccion = models.TextField()

