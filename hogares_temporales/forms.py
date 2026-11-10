from django import forms
from .models import HogarTemporal

class HogarTemporalForm(forms.ModelForm):
    class Meta:
        model = HogarTemporal
        fields = ["zona", "capacidad", "disponibilidad"]
        labels = {"zona": "Colonia o zona (opcional)", "capacidad": "¿Cuántos perros puedes recibir?", "disponibilidad": "Tengo espacio disponible"}
        widgets = {"zona": forms.TextInput(attrs={"placeholder": "Comparte solo una ubicación general"}), "capacidad": forms.NumberInput(attrs={"min": 1})}
