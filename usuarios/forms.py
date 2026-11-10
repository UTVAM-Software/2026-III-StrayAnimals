from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group, Permission, User

from .models import PerfilUsuario, Rol


class RolForm(forms.ModelForm):
    class Meta:
        model = Rol
        fields = ["nombre_rol"]


class PerfilUsuarioForm(forms.ModelForm):
    class Meta:
        model = PerfilUsuario
        fields = ["usuario", "nombre", "correo", "rol"]


class CrearUsuarioForm(UserCreationForm):
    username = forms.CharField(
        label="Nombre de usuario",
        max_length=30,
        help_text="Máximo 30 caracteres.",
        widget=forms.TextInput(
            attrs={"maxlength": "30", "placeholder": "Escribe tu usuario"}
        ),
    )
    email = forms.EmailField(required=True)
    groups = forms.ModelMultipleChoiceField(
        queryset=Group.objects.all(), required=False, widget=forms.CheckboxSelectMultiple
    )
    user_permissions = forms.ModelMultipleChoiceField(
        queryset=Permission.objects.select_related("content_type").all(),
        required=False,
        widget=forms.CheckboxSelectMultiple,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].max_length = 30
        self.fields["username"].widget.attrs.update(
            {"maxlength": "30", "placeholder": "Escribe tu usuario"}
        )
        self.fields["username"].help_text = (
            "Obligatorio. Máximo 30 caracteres. "
            "Se permiten letras, números y @/./+/-/_"
        )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = [
            "username", "first_name", "last_name", "email", "groups",
            "user_permissions", "is_staff", "is_active",
        ]


class EditarUsuarioForm(forms.ModelForm):
    groups = forms.ModelMultipleChoiceField(
        queryset=Group.objects.all(), required=False, widget=forms.CheckboxSelectMultiple
    )
    user_permissions = forms.ModelMultipleChoiceField(
        queryset=Permission.objects.select_related("content_type").all(),
        required=False,
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = User
        fields = [
            "username", "first_name", "last_name", "email", "groups",
            "user_permissions", "is_staff", "is_active",
        ]


class GroupForm(forms.ModelForm):
    permissions = forms.ModelMultipleChoiceField(
        queryset=Permission.objects.select_related("content_type").all(),
        required=False,
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = Group
        fields = ["name", "permissions"]


class PermissionForm(forms.ModelForm):
    class Meta:
        model = Permission
        fields = ["name", "content_type", "codename"]
