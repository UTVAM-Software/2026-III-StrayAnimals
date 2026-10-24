from django.conf import settings
from django.db import models


class Rol(models.Model):
    class NombreRol(models.TextChoices):
        ADMINISTRADOR = "Administrador", "Administrador"
        VOLUNTARIO = "Voluntario", "Voluntario"
        CIUDADANO = "Ciudadano", "Ciudadano"

    nombre_rol = models.CharField(
        max_length=30,
        choices=NombreRol.choices,
        unique=True,
    )

    class Meta:
        ordering = ["nombre_rol"]
        verbose_name = "Rol"
        verbose_name_plural = "Roles"

    def __str__(self):
        return self.nombre_rol


class PerfilUsuario(models.Model):
    """Datos propios de Stray Animals vinculados al usuario de autenticación Django."""
    usuario = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="perfil_stray_animals",
    )
    nombre = models.CharField(max_length=100)
    correo = models.EmailField(max_length=150, unique=True)
    rol = models.ForeignKey(
        Rol,
        on_delete=models.PROTECT,
        related_name="perfiles",
    )

    class Meta:
        ordering = ["nombre"]
        verbose_name = "Perfil de usuario"
        verbose_name_plural = "Perfiles de usuario"

    def __str__(self):
        return f"{self.nombre} ({self.rol})"
