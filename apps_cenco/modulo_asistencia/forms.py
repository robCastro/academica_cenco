
from django import forms


class IntervaloFechaForm(forms.Form):
    fechaInicial = forms.DateField()
    fechaFinal = forms.DateField()

    def __init__(self, *args, **kwargs):
        super(IntervaloFechaForm, self).__init__(*args, **kwargs)
        self.fields['fechaInicial'].label = 'Fecha Inicial'
        self.fields['fechaFinal'].label = 'Fecha Final'


class FechaAsistenciaForm(forms.Form):
    fechaAsistencia = forms.DateField()

    def __init__(self, *args, **kwargs):
        super(FechaAsistenciaForm, self).__init__(*args, **kwargs)
        self.fields['fechaAsistencia'].label = 'Fecha de Asistencia'
