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
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'required': True,
                                             'pattern': '^[a-zA-Z]+ ?[a-zA-Z]+$' ,'title': 'Ingrese su nombre o sus nombres con un espacio entre palabras'}),
            'apellido': forms.TextInput(attrs={'class': 'form-control', 'required': True,
                                               'pattern': '^[a-zA-Z]+ ?[a-zA-Z]+$', 'title': 'Ingrese su apellido o apellidos con un espacio entre palabras'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control', 'required': True,
                                                'pattern': '^[a-zA-Z0-9, ]+$', 'title': 'Ingrese su dirección completa'}),
            'correo': forms.TextInput(attrs={'class': 'form-control', 'required': False,
                                             'pattern': '^[\w\d_\.]+@[\w\d_]+\.[\w\d_\.]+$',
                                             'title': 'Ejemplo: MiCorreo@gmail.com'}),
            'dui': forms.TextInput(attrs={'size': '27', 'class': 'form-control',
                                          'pattern': '^[0-9]{8}-[0-9]$', 'title': 'Ejemplo: 12345678-9'}),
            'isss': forms.TextInput(attrs={'class': 'form-control', 'required': True,
                                           'pattern': '^[0-9]{9}$', 'title': 'Ejemplo: 123456789'}),
            'afp': forms.TextInput(attrs={'class': 'form-control', 'required': True,
                                          'pattern': '^[0-9]{12}$', 'title': 'Ejemplo: 123456789012'}),
            'nit': forms.TextInput(attrs={'class': 'form-control', 'required': True,
                                          'pattern': '^[0-9]{4}-[0-9]{6}-[0-9]{3}-[0-9]$',
                                          'title': 'Ejemplo: 1012-010197-412-3'}),
            'tipo': forms.Select(attrs={'class': 'form-control', 'required': True}),
        }
 # formato nit ^[0-9]{4}-[0-9]{6}-[0-9]{3}-[0-9]$



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
