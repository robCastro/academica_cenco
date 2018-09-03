
from django import forms


class IntervaloFechaForm(forms.Form):
    fechaInicial = forms.DateField()
    fechaFinal = forms.DateField()

    def __init__(self, *args, **kwargs):
        super(IntervaloFechaForm, self).__init__(*args, **kwargs)
        self.fields['fechaInicial'].label = 'Fecha Inicial'
        self.fields['fechaFinal'].label = 'Fecha Final'
