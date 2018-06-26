# -*- coding: utf-8 -*-
from django import forms

from apps_cenco.db_app.models import Alumno,Encargado

class ModificarAlumnoForm(forms.ModelForm):
    class Meta:
        model = Alumno
        fields = [
            'nombre',
            'apellido',
            'direccion',
            'correo',
            'fechaNacimiento',
            'dui',
            'encargado',
            'grupo',
            ]
        labels = {
            'nombre'            : 'Nombre:',
            'apellido'          : 'Apellido:',
            'direccion'         : 'Dirección:',
            'correo'            : 'Correo:',
            'fechaNacimiento'   : 'Fecha de Nacimiento:',
            'dui'               : 'DUI:',
            'encargado'         : 'Encargado:',
        }

        widgets = {
            'nombre'            : forms.TextInput(attrs={'size':'27'}),
            'apellido'          : forms.TextInput(attrs={'size':'27'}),
            'direccion'         : forms.Textarea(attrs={'rows':2, 'cols':25}),
            'correo'            : forms.EmailInput(attrs={'size':'27'}),
            'fechaNacimiento'   : forms.DateInput(attrs={'size':'27'}),
            'dui'               : forms.TextInput(attrs={'size':'27','pattern': '[0-9]'+'[0-9]'+'[0-9]'+'[0-9]'+'[0-9]'+'[0-9]'+'[0-9]'+'[0-9]'+'[-]'+'[0-9]'}),
            'encargado'         : forms.Select(),
            'grupo'             : forms.HiddenInput(),
        }

    def __init__(self,*args,**kwargs):
        super(ModificarAlumnoForm,self).__init__(*args,**kwargs)
        self.fields['encargado'].queryset=Encargado.objects.filter()




