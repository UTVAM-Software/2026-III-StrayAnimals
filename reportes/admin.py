from django.contrib import admin
from .models import Reporte


@admin.register(Reporte)
class ReporteAdmin(admin.ModelAdmin):
    list_display = ("id", "usuario", "ubicacion", "prioridad", "estatus", "fecha_creacion")
    list_filter = ("prioridad", "estatus", "fecha_creacion")
    search_fields = ("descripcion", "ubicacion", "usuario__nombre")
    readonly_fields = ("fecha_creacion",)
