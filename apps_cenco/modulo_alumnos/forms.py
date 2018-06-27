from django import forms
from django .forms import Form
from apps_cenco.db_app.models import Alumno, Encargado, Telefono
from django import forms
from apps_cenco.db_app.models import Alumno,Encargado

class InsertarAlumnoForm(forms.ModelForm):
    class Meta:
        model= Alumno
        fields =[
            'username',
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
            'username'          : 'Usuario',
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
            'username': forms.HiddenInput(attrs={'class':'form-control','required':True}),
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'apellido': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'direccion': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'correo': forms.EmailInput(attrs={'class': 'form-control', 'required': False}),
            'fechaNacimiento': forms.DateTimeInput(attrs={'class': 'form-control', 'required': True, 'type': 'date'}, ),
            'dui': forms.TextInput(attrs={'class': 'form-control', 'required': False,'pattern':'[0-9]'+'[0-9]'+'[0-9]'+'[0-9]'+'[0-9]'+'[0-9]'+'[0-9]'+'[0-9]'+'[-]'+'[0-9]'}),
            'grupo': forms.Select(attrs={'class': 'form-control', 'required': True}),
            'encargado': forms.Select(attrs={'class': 'form-control', 'required': True}),
        }
    def __init__ (self,*args,**kwargs):
        super(InsertarAlumnoForm,self).__init__(*args,**kwargs)
        self.fields['encargado'].queryset=Encargado.objects.filter()


class TelefonoForm(forms.ModelForm):

    class Meta:
        model = Telefono
        fields =[
            'numero',
            'tipo',
            ]
        labels ={
            'numero': 'Telefono',
            'tipo'  : 'Tipo',
            }

        widgets ={

            'numero':forms.TextInput(attrs={'class':'form-control','required':True,'pattern':'[0-9]'+'[0-9]'+'[0-9]'+'[0-9]'+'[0-9]'+'[0-9]'+'[0-9]'+'[0-9]'}),
            'tipo'  :forms.Select(attrs={'class':'form-control','required':True}),
        }


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
            'correo': 'Correo',
            'fechaNacimiento': 'Fecha de nacimiento',
            'dui': 'Dui',
        }

        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'apellido': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'direccion': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'correo': forms.EmailInput(attrs={'class': 'form-control', 'required': False}),
            'fechaNacimiento': forms.DateTimeInput(attrs={'class': 'form-control', 'required': True, 'type': 'date'}, ),
            'dui': forms.TextInput(attrs={'class': 'form-control', 'required': True,
                                          'pattern': '[0-9]' + '[0-9]' + '[0-9]' + '[0-9]' + '[0-9]' + '[0-9]' + '[0-9]' + '[0-9]' + '[-]' + '[0-9]'}),
        }


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
            'direccion'         : 'Direccion',
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