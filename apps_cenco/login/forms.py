#-*-coding: UTF-8 -*-
from django import forms

from django.contrib.auth.models import User


class AsistenteCredencialesPropiasForm(forms.Form):

    usuario=forms.CharField(max_length=25,widget=forms.TextInput(attrs={'size':'25','requerid':'True','class':'form-control'}),label='Usuario:')
    contrasenia3 = forms.CharField(max_length=15, widget=forms.PasswordInput(attrs={'size': '15', 'requerid': 'True','class':'form-control'}),label='Contraseña antigua:')
    contrasenia1=forms.CharField(max_length=15,widget=forms.PasswordInput(attrs={'size':'15','requerid':'True','class':'form-control'}),label='Contraseña nueva:')
    contrasenia2=forms.CharField(max_length=15,widget=forms.PasswordInput(attrs={'size':'15','requerid':'True','class':'form-control'}),label="Repetir contraseña nueva:")


    def clean_contrasenia2(self):
        contrasenia1 = self.cleaned_data.get('contrasenia1')
        contrasenia2 = self.cleaned_data.get('contrasenia2')
        if contrasenia1 and contrasenia2 and contrasenia1 != contrasenia2:
            raise forms.ValidationError('Las contraseñas no coinciden')
        return contrasenia2

    def clean_usuario(self):
        usuario=self.cleaned_data.get('usuario')
        actual=self.user.username
        existe= User.objects.filter(username = self.cleaned_data.get('usuario')).count()
        if usuario != actual:
            if existe:
                raise forms.ValidationError('El nombre de usuario ya existe')
        return usuario

    def clean_contrasenia3(self):
        contrasenia3=self.cleaned_data.get('contrasenia3')
        if not self.user.check_password(contrasenia3):
            raise forms.ValidationError('La contraseña antigua es incorrecta')
        return contrasenia3


    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(AsistenteCredencialesPropiasForm, self).__init__(*args, **kwargs)


class AlumnoCredencialesPropiasForm(forms.Form):

    contrasenia3 = forms.CharField(max_length=15, widget=forms.PasswordInput(attrs={'size': '15', 'requerid': 'True','class':'form-control'}),label='Contraseña antigua:')
    contrasenia1=forms.CharField(max_length=15,widget=forms.PasswordInput(attrs={'size':'15','requerid':'True','class':'form-control'}),label='Contraseña nueva:')
    contrasenia2=forms.CharField(max_length=15,widget=forms.PasswordInput(attrs={'size':'15','requerid':'True','class':'form-control'}),label="Repetir contraseña nueva:")


    def clean_contrasenia2(self):
        contrasenia1 = self.cleaned_data.get('contrasenia1')
        contrasenia2 = self.cleaned_data.get('contrasenia2')
        if contrasenia1 and contrasenia2 and contrasenia1 != contrasenia2:
            raise forms.ValidationError('Las contraseñas no coinciden')
        return contrasenia2

    def clean_contrasenia3(self):
        contrasenia3=self.cleaned_data.get('contrasenia3')
        if not self.user.check_password(contrasenia3):
            raise forms.ValidationError('La contraseña antigua es incorrecta')
        return contrasenia3


    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(AlumnoCredencialesPropiasForm, self).__init__(*args, **kwargs)

class ModCredAsistForm(forms.Form):

    contrasenia1=forms.CharField(max_length=127, widget=forms.PasswordInput, label='Contraseña')
    contrasenia2=forms.CharField(max_length=127, widget=forms.PasswordInput, label='Repetir')

    def clean_contrasenia2(self):
        contrasenia1 = self.cleaned_data.get('contrasenia1')
        contrasenia2 = self.cleaned_data.get('contrasenia2')
        if contrasenia1 and contrasenia2 and contrasenia1 != contrasenia2:
            raise forms.ValidationError('Las contraseñas no coinciden')
        return contrasenia2

    def clean_usuario(self):
        usuario=self.cleaned_data.get('usuario')
        actual=self.user.username
        existe= User.objects.filter(username = self.cleaned_data.get('usuario')).count()
        if usuario != actual:
            if existe:
                raise forms.ValidationError('El nombre de usuario ya existe')
        return usuario