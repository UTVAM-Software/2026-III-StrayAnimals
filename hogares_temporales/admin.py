from django.contrib import admin
from .models import HogarTemporal


@admin.register(HogarTemporal)
class HogarTemporalAdmin(admin.ModelAdmin):
    list_display = ("id", "usuario", "capacidad", "disponibilidad")
    list_filter = ("disponibilidad",)
    search_fields = ("usuario__nombre", "usuario__correo")
