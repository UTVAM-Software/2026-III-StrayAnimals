from django import forms
from .models import SolicitudAdopcion
from reportes.models import Reporte

class SolicitudAdopcionForm(forms.ModelForm):
    class Meta:
        model = SolicitudAdopcion
        fields = ["reporte", "motivo"]
        labels = {"reporte": "¿Qué perrito te gustaría adoptar?", "motivo": "Cuéntanos por qué quieres adoptarlo (opcional)"}
        widgets = {"motivo": forms.Textarea(attrs={"rows": 4, "placeholder": "Un poquito sobre tu hogar y tu interés..."})}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["reporte"].queryset = Reporte.objects.exclude(estatus=Reporte.Estatus.ADOPTADO)

    def clean_reporte(self):
        reporte = self.cleaned_data["reporte"]
        if reporte.estatus == Reporte.Estatus.ADOPTADO:
            raise forms.ValidationError("Este perrito ya fue adoptado.")
        return reporte

class SolicitudGestionForm(forms.ModelForm):
    class Meta:
        model = SolicitudAdopcion
        fields = ["reporte", "motivo", "estado_solicitud"]
        widgets = {"motivo": forms.Textarea(attrs={"rows": 4})}
