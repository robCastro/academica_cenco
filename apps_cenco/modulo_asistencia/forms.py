
from django import forms


class IntervaloFechaForm(forms.Form):
    fechaInicial = forms.DateField()
    fechaFinal = forms.DateField()