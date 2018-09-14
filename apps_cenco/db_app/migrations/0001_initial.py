# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-09-14 14:51
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Alumno',
            fields=[
                ('codigo', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=40)),
                ('apellido', models.CharField(max_length=40)),
                ('direccion', models.TextField()),
                ('correo', models.EmailField(blank=True, max_length=254, null=True)),
                ('fechaNacimiento', models.DateField()),
                ('dui', models.CharField(blank=True, max_length=10, null=True)),
                ('solvente', models.BooleanField(default=False)),
            ],
            options={
                'permissions': (('ver_alumno', 'Ver alumno'),),
            },
        ),
        migrations.CreateModel(
            name='Asistencia',
            fields=[
                ('codigo_asistencia', models.AutoField(primary_key=True, serialize=False)),
                ('fecha_asistencia', models.DateField()),
                ('asistio', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Carrera',
            fields=[
                ('codigo_carrera', models.AutoField(primary_key=True, serialize=False)),
                ('nombre_carrera', models.CharField(max_length=20)),
                ('descripcion_carrera', models.CharField(max_length=200)),
                ('cuota_semanal_carrera', models.DecimalField(decimal_places=2, max_digits=10)),
                ('precio_inscripcion_carrera', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
        migrations.CreateModel(
            name='Colegiatura',
            fields=[
                ('codigo_colegiatura', models.AutoField(primary_key=True, serialize=False)),
                ('cuota_semanal', models.DecimalField(decimal_places=2, max_digits=10)),
                ('forma_pago', models.CharField(max_length=100)),
                ('actual_colegiatura', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Cursa',
            fields=[
                ('codigo_cursa', models.AutoField(primary_key=True, serialize=False)),
                ('evaluacion1', models.DecimalField(decimal_places=4, max_digits=6)),
                ('evaluacion2', models.DecimalField(decimal_places=4, max_digits=6)),
                ('evaluacion3', models.DecimalField(decimal_places=4, max_digits=6)),
                ('nota_final', models.DecimalField(decimal_places=4, max_digits=6)),
                ('alumno', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='db_app.Alumno')),
            ],
        ),
        migrations.CreateModel(
            name='DetalleEstado',
            fields=[
                ('codigo_detalle_e', models.AutoField(primary_key=True, serialize=False)),
                ('fecha_detalle_e', models.DateField()),
                ('actual_detalle_e', models.BooleanField(default=True)),
                ('alumno', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='db_app.Alumno')),
            ],
        ),
        migrations.CreateModel(
            name='DetallePago',
            fields=[
                ('codigo_detalle_pago', models.AutoField(primary_key=True, serialize=False)),
                ('fecha_pago', models.DateField()),
                ('monto_pago', models.DecimalField(decimal_places=2, max_digits=10)),
                ('cancelado', models.BooleanField(default=False)),
                ('cantidad_semanas', models.IntegerField()),
                ('colegiatura', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='db_app.Colegiatura')),
            ],
        ),
        migrations.CreateModel(
            name='DetallePensum',
            fields=[
                ('codigo_detalle_p', models.AutoField(primary_key=True, serialize=False)),
                ('carrera', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='db_app.Carrera')),
            ],
        ),
        migrations.CreateModel(
            name='Documento',
            fields=[
                ('codigo_doc', models.AutoField(primary_key=True, serialize=False)),
                ('nombre_doc', models.CharField(max_length=20)),
                ('descripcion_doc', models.CharField(max_length=200)),
                ('archivo', models.FileField(upload_to=b'')),
            ],
        ),
        migrations.CreateModel(
            name='Empleado',
            fields=[
                ('codigo', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=40)),
                ('apellido', models.CharField(max_length=40)),
                ('direccion', models.TextField()),
                ('correo', models.EmailField(blank=True, max_length=254)),
                ('dui', models.CharField(max_length=10)),
                ('isss', models.CharField(max_length=9)),
                ('afp', models.CharField(max_length=12)),
                ('nit', models.CharField(max_length=17)),
                ('tipo', models.CharField(choices=[('Asi', 'Asistente'), ('Pro', 'Profesor'), ('Tec', 'Tecnico')], default='Pro', max_length=3)),
                ('estado', models.CharField(choices=[('activo', 'activo'), ('inactivo', 'inactivo')], default='activo', max_length=8)),
                ('username', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Encargado',
            fields=[
                ('codigo', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=40)),
                ('apellido', models.CharField(max_length=40)),
                ('direccion', models.TextField()),
                ('correo', models.EmailField(blank=True, max_length=254, null=True)),
                ('dui', models.CharField(blank=True, max_length=10, null=True)),
                ('username', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Estado',
            fields=[
                ('codigo_estado', models.AutoField(primary_key=True, serialize=False)),
                ('tipo_estado', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Expediente',
            fields=[
                ('codigo_expediente', models.AutoField(primary_key=True, serialize=False)),
                ('activo_expediente', models.BooleanField(default=True)),
                ('fecha_inicio_exp', models.DateField()),
                ('fecha_proximo_pago_exp', models.DateField()),
                ('pagado_hasta', models.DateField()),
                ('alumno', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='db_app.Alumno')),
                ('carrera', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='db_app.Carrera')),
            ],
        ),
        migrations.CreateModel(
            name='Grupo',
            fields=[
                ('codigo', models.AutoField(primary_key=True, serialize=False)),
                ('fechaInicio', models.DateField()),
                ('alumnosInscritos', models.IntegerField(default=0)),
                ('activo_grupo', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Horario',
            fields=[
                ('codigo', models.AutoField(primary_key=True, serialize=False)),
                ('dias_asignados', models.CharField(choices=[('Lunes y Miercoles', 'Lunes y Miercoles'), ('Martes y Jueves', 'Martes y Jueves'), ('Domingo', 'Domingo'), ('Sabado', 'Sabado'), ('Viernes', 'Viernes')], max_length=40)),
                ('hora_inicio', models.TimeField()),
                ('hora_fin', models.TimeField()),
                ('cantidad_alumnos', models.IntegerField(blank=True, default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Inscripcion',
            fields=[
                ('codigo_ins', models.AutoField(primary_key=True, serialize=False)),
                ('fecha_inscripcion', models.DateField()),
                ('actual_inscripcion', models.BooleanField(default=True)),
                ('alumno', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='db_app.Alumno')),
                ('grupo', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='db_app.Grupo')),
            ],
        ),
        migrations.CreateModel(
            name='Materia',
            fields=[
                ('codigo_materia', models.AutoField(primary_key=True, serialize=False)),
                ('nombre_materia', models.CharField(max_length=20)),
                ('descripcion_materia', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Telefono',
            fields=[
                ('codigo', models.AutoField(primary_key=True, serialize=False)),
                ('numero', models.CharField(max_length=8)),
                ('tipo', models.CharField(choices=[('casa', 'Casa'), ('trabajo', 'Trabajo'), ('movil', 'Movil')], max_length=20)),
                ('alumno', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='db_app.Alumno')),
                ('empleado', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='db_app.Empleado')),
                ('encargado', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='db_app.Encargado')),
            ],
        ),
        migrations.AddField(
            model_name='grupo',
            name='horario',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='db_app.Horario'),
        ),
        migrations.AddField(
            model_name='grupo',
            name='profesor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='db_app.Empleado'),
        ),
        migrations.AddField(
            model_name='documento',
            name='materia',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='db_app.Materia'),
        ),
        migrations.AddField(
            model_name='detallepensum',
            name='materia',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='db_app.Materia'),
        ),
        migrations.AddField(
            model_name='detalleestado',
            name='estado',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='db_app.Estado'),
        ),
        migrations.AddField(
            model_name='cursa',
            name='materia',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='db_app.Materia'),
        ),
        migrations.AddField(
            model_name='colegiatura',
            name='expediente',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='db_app.Expediente'),
        ),
        migrations.AddField(
            model_name='asistencia',
            name='inscripcion',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='db_app.Inscripcion'),
        ),
        migrations.AddField(
            model_name='alumno',
            name='encargado',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='db_app.Encargado'),
        ),
        migrations.AddField(
            model_name='alumno',
            name='username',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
