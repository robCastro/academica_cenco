# -*- coding: utf-8 -*-
from django import forms

from apps_cenco.db_app.models import Materia


class CrearEditarMateriaForm(forms.ModelForm):
    class Meta:
        model = Materia
        fields = [
            'nombre_materia',
            'descripcion_materia'
        ]
        labels = {
            'nombre_materia': 'Nombre',
            'descripcion_materia': 'Descripción'
        }

        widgets = {
            'nombre_materia': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'descripcion_materia': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
        }