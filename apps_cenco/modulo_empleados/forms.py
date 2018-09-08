# -*- coding: utf-8 -*-
from django import forms

from apps_cenco.db_app.models import Empleado


class CrearEmpleadoForm(forms.ModelForm):
    class Meta:
        model = Empleado
        fields = [
            'username',
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
            'username': 'Nombre de Usuario',
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
            'username': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'apellido': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'direccion': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'correo': forms.EmailInput(attrs={'class': 'form-control', 'required': False}),
            'dui': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'isss': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'afp': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'nit': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'tipo': forms.Select(attrs={'class': 'form-control', 'required': True}),
        }
