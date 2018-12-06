# -*- coding: utf-8 -*-
from django import forms

from apps_cenco.db_app.models import Materia, Documento


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


class SubirDocumentoForm(forms.ModelForm):
    class Meta:
        model = Documento
        fields = [
            'materia',
            'nombre_doc',
            'descripcion_doc',
            'archivo',

        ]
        labels = {
            'materia': 'Seleccione un Materia',
            'nombre_doc': 'Nombre del Documento',
            'descripcion_doc': 'Descripción',
            'archivo': 'Seleccione un archivo',
        }

        widgets = {
            'materia': forms.Select(attrs={'class': 'form-control', 'required': True}),
            'nombre_doc': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'descripcion_doc': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
        }
