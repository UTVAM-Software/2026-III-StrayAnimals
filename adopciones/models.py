from django.db import models
from usuarios.models import PerfilUsuario
from reportes.models import Reporte


class SolicitudAdopcion(models.Model):
    class EstadoSolicitud(models.TextChoices):
        PENDIENTE = "Pendiente", "Pendiente"
        APROBADA = "Aprobada", "Aprobada"
        RECHAZADA = "Rechazada", "Rechazada"

    reporte = models.ForeignKey(
        Reporte,
        on_delete=models.PROTECT,
        related_name="solicitudes_adopcion",
    )
    usuario_interesado = models.ForeignKey(
        PerfilUsuario,
        on_delete=models.PROTECT,
        related_name="solicitudes_adopcion",
    )
    estado_solicitud = models.CharField(
        max_length=10,
        choices=EstadoSolicitud.choices,
        default=EstadoSolicitud.PENDIENTE,
    )
    fecha_solicitud = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-fecha_solicitud"]
        verbose_name = "Solicitud de adopción"
        verbose_name_plural = "Solicitudes de adopción"

    def __str__(self):
        return f"Solicitud #{self.pk} - {self.estado_solicitud}"
