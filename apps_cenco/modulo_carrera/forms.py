# -*- coding: utf-8 -*-
from django import forms

from apps_cenco.db_app.models import Carrera


class CrearEditarCarreraForm(forms.ModelForm):
    class Meta:
        model = Carrera
        fields = [
            'nombre_carrera',
            'descripcion_carrera',
            'cuota_semanal_carrera',
            'precio_inscripcion_carrera',
        ]

        labels = {
            'nombre_carrera':   'Nombre de la Carrera',
            'descripcion_carrera':  'Descripción',
            'cuota_semanal_carrera': 'Cuota Semanal',
            'precio_inscripcion_carrera':   'Costo de Inscripción',
        }

        widgets = {
            'nombre_carrera': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'descripcion_carrera': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'cuota_semanal_carrera': forms.NumberInput(attrs={'class': 'form-control', 'required': True}),
            'precio_inscripcion_carrera': forms.NumberInput(attrs={'class': 'form-control', 'required': True}),
        }