from django import forms
from django.forms import ModelForm

from apps_cenco.db_app.models import Grupo, Empleado, Horario


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
           'profesor'       : 'Profesor encargado:',
        }
        widgets = {
           'fechaInicio'   : forms.TextInput(attrs={'class': 'form-control', 'required': True}),
           'horario'       : forms.Select(attrs={'class':'form-control', 'required':True}),
           'profesor'		: forms.Select(attrs={'class':'form-control', 'required':True}),
        }

    def __init__ (self, *args, **kwargs):
        super(CrearGrupoForm, self).__init__(*args, **kwargs)
        self.fields['profesor'].queryset = Empleado.objects.filter(tipo='Pro')

