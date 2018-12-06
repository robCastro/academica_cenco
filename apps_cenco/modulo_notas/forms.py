# -*- coding: utf-8 -*-
from django import forms

from apps_cenco.db_app.models import Evaluacion, Examen


class CrearEditarExamenForm(forms.ModelForm):
    class Meta:
        model = Examen
        fields = [
            'nombre_examen',
            'ponderacion_examen',
            'fecha_realizacion_examen',
            'materia',
        ]

        labels = {
            'nombre_examen': 'Nombre de la Evaluación',
            'ponderacion_examen': 'Ponderación',
            'fecha_realizacion_examen': 'Fecha en que se realizará',
            'materia': 'Asignatura',
        }

        widgets = {
            'nombre_examen': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'ponderacion_examen': forms.NumberInput(attrs={'class': 'form-control', 'required': True}),
            'fecha_realizacion_examen': forms.DateInput(attrs={'class': 'form-control', 'required': True}),
            'materia': forms.Select(attrs={'class': 'form-control', 'required': True}),
        }