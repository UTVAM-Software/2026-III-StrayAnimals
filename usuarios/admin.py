from django.contrib import admin
from .models import Rol, PerfilUsuario


@admin.register(Rol)
class RolAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre_rol")
    search_fields = ("nombre_rol",)


@admin.register(PerfilUsuario)
class PerfilUsuarioAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre", "correo", "rol", "usuario")
    list_filter = ("rol",)
    search_fields = ("nombre", "correo", "usuario__username")
