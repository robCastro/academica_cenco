# -*- coding: utf-8 -*-
from django import forms

from apps_cenco.db_local.models import FooterINFO


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
