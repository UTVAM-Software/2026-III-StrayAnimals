from django.contrib import admin
from .models import SolicitudAdopcion


@admin.register(SolicitudAdopcion)
class SolicitudAdopcionAdmin(admin.ModelAdmin):
    list_display = ("id", "reporte", "usuario_interesado", "estado_solicitud", "fecha_solicitud")
    list_filter = ("estado_solicitud", "fecha_solicitud")
    search_fields = ("usuario_interesado__nombre", "reporte__ubicacion")
    readonly_fields = ("fecha_solicitud",)
