from django import forms
from django .forms import ModelForm
from apps_cenco.db_app.models import Alumno, Encargado


class InsertarAlumnoForm(forms.ModelForm):
    class Meta:
        model= Alumno
        fields =[
            'nombre',
            'apellido',
            'direccion',
            'correo',
            'fechaNacimiento',
            'dui',
            'grupo',
            'encargado',
            ]
        labels ={
            'nombre'            : 'Nombre',
            'apellido'          : 'Apellido' ,
            'direccion'         : 'Direccion',
            'correo'            : 'Correo',
            'fechaNacimiento'   : 'Fecha de Nacimiento',
            'dui'               : 'Dui',
            'grupo'             : 'Grupo',
            'encargado'         : 'Encargado',
        }

        widgets ={
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'apellido': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'direccion': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'correo': forms.EmailInput(attrs={'class': 'form-control', 'required': True}),
            'fechaNacimiento': forms.DateTimeInput(attrs={'class': 'form-control', 'required': True, 'type': 'date'}, ),
            'dui': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'grupo': forms.Select(attrs={'class': 'form-control', 'required': True}),
            'encargado': forms.Select(attrs={'class': 'form-control', 'required': True}),
        }
    def __init__ (self,*args,**kwargs):
        super(InsertarAlumnoForm,self).__init__(*args,**kwargs)
        self.fields['encargado'].queryset=Encargado.objects.filter()


class CrearEncargadoForm(forms.ModelForm):
    class Meta:
        model = Encargado
        fields = [
            'nombre',
            'apellido',
            'direccion',
            'correo',
            'fechaNacimiento',
            'dui',
            ]
        labels = {
            'nombre': 'Nombre',
            'apellido': 'Apellido',
            'direccion': 'Direccion',
            'correo':'Correo',
            'fechaNacimiento': 'Fecha de nacimiento',
            'dui': 'Dui',
        }

        widgets = {
            'nombre': forms.TextInput(attrs={'class':'form-control', 'required': True}),
            'apellido': forms.TextInput(attrs={'class':'form-control', 'required': True}),
            'direccion': forms.TextInput(attrs={'class':'form-control', 'required': True}),
            'correo': forms.EmailInput(attrs={'class':'form-control', 'required': True}),
            'fechaNacimiento': forms.DateTimeInput(attrs={'class':'form-control', 'required':True,'type':'date'},),
            'dui': forms.TextInput(attrs={'class':'form-control', 'required': True}),
        }

