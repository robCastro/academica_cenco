# -*- coding: utf-8 -*-
from django import forms

from apps_cenco.db_app.models import Evaluacion, Examen


# class CrearEditarExamenForm(forms.ModelForm):
#     class Meta:
#         model = Examen
#         fields = [
#             'nombre_evaluacion',
#             'ponderacion_evaluacion',
#             'fecha_realizacion_evaluacion',
#         ]
#
#         labels = {
#             'nombre_evaluacion': 'Nombre de la Evaluación',
#             'ponderacion_evaluacion': 'Ponderación',
#             'fecha_realizacion_evaluacion': 'Fecha en que se realizó',
#         }
#
#         widgets = {
#             'nombre_evaluacion': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
#             'ponderacion_evaluacion': forms.NumberInput(attrs={'class': 'form-control', 'required': True}),
#             'fecha_realizacion_evaluacion': forms.DateInput(attrs={'class': 'form-control', 'required': True}),
#         }