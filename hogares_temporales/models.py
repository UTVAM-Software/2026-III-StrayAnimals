from django.core.validators import MinValueValidator
from django.db import models
from usuarios.models import PerfilUsuario


class HogarTemporal(models.Model):
    usuario = models.ForeignKey(
        PerfilUsuario,
        on_delete=models.PROTECT,
        related_name="hogares_temporales",
    )
    capacidad = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    disponibilidad = models.BooleanField(default=True)

    class Meta:
        ordering = ["-disponibilidad", "capacidad"]
        verbose_name = "Hogar temporal"
        verbose_name_plural = "Hogares temporales"

    def __str__(self):
        estado = "Disponible" if self.disponibilidad else "No disponible"
        return f"{self.usuario.nombre} - {estado}"
