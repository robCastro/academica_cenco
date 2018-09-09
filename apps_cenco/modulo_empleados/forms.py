# -*- coding: utf-8 -*-
from django import forms

from apps_cenco.db_app.models import Empleado, Telefono


class CrearEmpleadoForm(forms.ModelForm):
    class Meta:
        model = Empleado
        fields = [
            'nombre',
            'apellido',
            'direccion',
            'correo',
            'dui',
            'isss',
            'afp',
            'nit',
            'tipo',
        ]
        labels = {
            'nombre': 'Nombre',
            'apellido': 'Apellido',
            'direccion': 'Dirección',
            'correo': 'Correo',
            'dui': 'DUI',
            'isss': 'ISSS',
            'afp': 'AFP',
            'nit': 'NIT',
            'tipo': 'Cargo que ocupa',
        }
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'apellido': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'direccion': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'correo': forms.EmailInput(attrs={'class': 'form-control', 'required': False}),
            'dui': forms.TextInput(attrs={'size': '27', 'class': 'form-control', 'pattern':
                '[0-9]' + '[0-9]' + '[0-9]' + '[0-9]' + '[0-9]' + '[0-9]' + '[0-9]' + '[0-9]' + '[-]' + '[0-9]'}),
            'isss': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'afp': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'nit': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'tipo': forms.Select(attrs={'class': 'form-control', 'required': True}),
        }


class CrearTelefonoForm(forms.ModelForm):
    class Meta:
        model = Telefono
        fields = [
            'tipo',
            'numero'
        ]
        labels = {
            'tipo': 'Tipo de Teléfono',
            'numero': 'Número',
        }
        widgets = {
            'tipo': forms.Select(attrs={'class': 'form-control', 'required': True, 'id': 'id_tipo_telefono'}),
            'numero': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
        }

    def add_prefix(self, field_name):
        FIELD_NAME_MAPPING = {'tipo': 'tipo_telefono'}
        # look up field name; return original if not found
        field_name = FIELD_NAME_MAPPING.get(field_name, field_name)
        return super(CrearTelefonoForm, self).add_prefix(field_name)
