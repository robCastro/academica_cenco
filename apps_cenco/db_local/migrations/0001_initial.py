# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-11-20 17:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ConfigAlumnos',
            fields=[
                ('codigo', models.AutoField(primary_key=True, serialize=False)),
                ('cant_dias_desactivar_alumno', models.IntegerField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ConfigCentroComputo',
            fields=[
                ('codigo', models.AutoField(primary_key=True, serialize=False)),
                ('cant_computadoras_disp', models.IntegerField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ConfigPago',
            fields=[
                ('codigo', models.AutoField(primary_key=True, serialize=False)),
                ('cant_dias_mod_pago', models.IntegerField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='FooterINFO',
            fields=[
                ('codigo', models.AutoField(primary_key=True, serialize=False)),
                ('telefono', models.CharField(max_length=8)),
                ('correo', models.EmailField(blank=True, max_length=254, null=True)),
                ('direccion', models.TextField()),
            ],
        ),
    ]
