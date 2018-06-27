from django import forms

from apps_cenco.db_app.models import Horario


class CrearHorarioForm(forms.ModelForm):
    class Meta:
        model = Horario
        fields = [
            'dias_asignados',
            'hora_inicio',
            'hora_fin',
        ]
        labels = {
            'dias_asignados': 'Dias Asignados',
            'hora_inicio': 'Hora de Inicio',
            'hora_fin': 'Hora de Finalizacion',
        }
        widgets = {
            'dias_asignados': forms.Select(attrs={'class': 'form-control', 'required': True}),
            'hora_inicio': forms.DateTimeInput(attrs={'class':'form-control', 'required':True,'type':'time'},),
            'hora_fin': forms.DateTimeInput(attrs={'class':'form-control', 'required':True,'type':'time'},),
        }
