from django.db import models
from usuarios.models import PerfilUsuario


class Reporte(models.Model):
    class Prioridad(models.TextChoices):
        BAJA = "Baja", "Baja"
        MEDIA = "Media", "Media"
        ALTA = "Alta", "Alta"

    class Estatus(models.TextChoices):
        REPORTADO = "Reportado", "Reportado"
        RESCATADO = "Rescatado", "Rescatado"
        TEMPORAL = "Temporal", "Temporal"
        ADOPTADO = "Adoptado", "Adoptado"

    usuario = models.ForeignKey(
        PerfilUsuario,
        on_delete=models.PROTECT,
        related_name="reportes",
    )
    descripcion = models.TextField()
    fotografia = models.ImageField(upload_to="reportes/", blank=True, null=True)
    ubicacion = models.CharField(max_length=255)
    prioridad = models.CharField(
        max_length=10,
        choices=Prioridad.choices,
        default=Prioridad.MEDIA,
    )
    estatus = models.CharField(
        max_length=15,
        choices=Estatus.choices,
        default=Estatus.REPORTADO,
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-fecha_creacion"]
        verbose_name = "Reporte"
        verbose_name_plural = "Reportes"

    def __str__(self):
        return f"Reporte #{self.pk} - {self.estatus}"
