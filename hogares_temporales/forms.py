from django import forms
from .models import HogarTemporal


class HogarTemporalForm(forms.ModelForm):
    class Meta:
        model = HogarTemporal
        fields = ["usuario", "capacidad", "disponibilidad"]
