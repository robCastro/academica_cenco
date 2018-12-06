# -*- coding: utf-8 -*-
from django import forms

from apps_cenco.db_local.models import FooterINFO, ConfigAlumnos, ConfigCentroComputo, ConfigPago


class DetalleFooterForm(forms.ModelForm):
    class Meta:
        model = FooterINFO
        fields = [
            'telefono',
            'correo',
            'direccion',
        ]
        labels = {
            'telefono': 'Teléfono',
            'correo': 'Correo Electrónico',
            'direccion': 'Dirección',
        }
        widgets = {
            'telefono': forms.TextInput(attrs={'class': 'form-control', 'required': True,
                                               'pattern': '[0-9]' + '[0-9]' + '[0-9]' + '[0-9]' +
                                                          '[0-9]' + '[0-9]' + '[0-9]' + '[0-9]'}),
            'correo': forms.EmailInput(attrs={'class': 'form-control', 'required': True}),
            'direccion': forms.Textarea(attrs={'rows': 3, 'cols': 50, 'required': True}),
        }


class ConfigAlumnosForm(forms.ModelForm):
    class Meta:
        model = ConfigAlumnos
        fields = [
            'cant_dias_desactivar_alumno',
        ]
        labels = {
            'cant_dias_desactivar_alumno': 'Días para desactivar',
        }
        widgets = {
            'cant_dias_desactivar_alumno': forms.NumberInput(attrs={'class': 'form-control', 'required': True}),

        }


class ConfigCompForm(forms.ModelForm):
    class Meta:
        model = ConfigCentroComputo
        fields = [
            'cant_computadoras_disp',
        ]
        labels = {
            'cant_computadoras_disp': 'Cantidad de Computadoras Disponibles',
        }
        widgets = {
            'cant_computadoras_disp': forms.NumberInput(attrs={'class': 'form-control', 'required': True}),

        }


class ConfigPagoForm(forms.ModelForm):
    class Meta:
        model = ConfigPago
        fields = [
            'cant_dias_mod_pago',
        ]
        labels = {
            'cant_dias_mod_pago': 'Cantidad de Días Para Modificar o Eliminar Pagos',
        }
        widgets = {
            'cant_dias_mod_pago': forms.NumberInput(attrs={'class': 'form-control', 'required': True}),

        }