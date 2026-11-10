from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import PerfilUsuario


class RegistroCiudadanoForm(UserCreationForm):
    nombre = forms.CharField(max_length=100, label="Tu nombre", help_text="Así te identificaremos dentro de la comunidad")
    email = forms.EmailField(max_length=150, label="Correo electrónico")

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "nombre", "email", "password1", "password2")
        labels = {"username": "Nombre de usuario"}

    def clean_email(self):
        email = self.cleaned_data["email"].strip().lower()
        if User.objects.filter(email__iexact=email).exists() or PerfilUsuario.objects.filter(correo__iexact=email).exists():
            raise forms.ValidationError("Este correo ya tiene una cuenta.")
        return email


class EditarMiPerfilForm(forms.ModelForm):
    class Meta:
        model = PerfilUsuario
        fields = ("nombre", "correo")
        labels = {"nombre": "Nombre completo", "correo": "Correo electrónico"}

    def clean_correo(self):
        correo = self.cleaned_data["correo"].strip().lower()
        if PerfilUsuario.objects.filter(correo__iexact=correo).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("Este correo ya está registrado.")
        if User.objects.filter(email__iexact=correo).exclude(pk=self.instance.usuario_id).exists():
            raise forms.ValidationError("Este correo ya pertenece a otro usuario.")
        return correo
