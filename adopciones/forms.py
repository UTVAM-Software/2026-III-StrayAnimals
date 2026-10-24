from django import forms
from .models import SolicitudAdopcion


class SolicitudAdopcionForm(forms.ModelForm):
    class Meta:
        model = SolicitudAdopcion
        fields = ["reporte", "usuario_interesado", "estado_solicitud"]
