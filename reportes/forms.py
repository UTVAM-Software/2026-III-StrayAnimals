from django import forms
from .models import Reporte

class ReporteForm(forms.ModelForm):
    class Meta:
        model = Reporte
        fields = ["descripcion", "fotografia", "ubicacion", "prioridad"]
        labels = {"descripcion": "¿Cómo es el perrito?", "fotografia": "Fotografía (opcional)", "ubicacion": "Colonia o zona aproximada", "prioridad": "¿Qué tan urgente es?"}
        widgets = {"descripcion": forms.Textarea(attrs={"rows": 4, "placeholder": "Color, tamaño, condición y detalles para reconocerlo..."}), "ubicacion": forms.TextInput(attrs={"placeholder": "Ej. Colonia Centro, cerca del parque"})}

class ReporteGestionForm(forms.ModelForm):
    class Meta:
        model = Reporte
        fields = ["descripcion", "fotografia", "ubicacion", "prioridad", "estatus"]
        widgets = {"descripcion": forms.Textarea(attrs={"rows": 4})}
