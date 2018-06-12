from django import forms
from django.forms import ModelForm

from apps_cenco.db_app.models import Grupo


class CrearGrupoForm(forms.ModelForm):
    class Meta:
        model = Grupo
        fields = [
            'fechaInicio',
            'horario',
            'profesor',
            ]
        labels = {
            'fechaInicio'	: 'Fecha de inicio:',
            'horario'		: 'Horario asignado:',
            'profesor'      : 'Profesor encargado:',
        }
        widgets = {
            'fechaInicio'   : forms.DateTimeInput(attrs={'class':'form-control', 'required':True,'type':'date'},),
            'horario'       : forms.Select(attrs={'class':'form-control', 'required':True}),
            'profesor'		: forms.Select(attrs={'class':'form-control', 'required':True}),
        }
