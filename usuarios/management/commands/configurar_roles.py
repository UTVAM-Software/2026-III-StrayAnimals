from django.contrib.auth.models import Group, Permission
from django.core.management.base import BaseCommand
from usuarios.models import Rol

# Un grupo siempre define el acceso: nunca basta con escoger un rol en HTML.
PERMISOS_POR_GRUPO = {
    "Ciudadano": [
        "reportes.view_reporte", "reportes.add_reporte",
        "hogares_temporales.view_hogartemporal", "hogares_temporales.add_hogartemporal",
        "adopciones.view_solicitudadopcion", "adopciones.add_solicitudadopcion",
    ],
    "Voluntario": [
        "reportes.view_reporte", "reportes.add_reporte", "reportes.change_reporte",
        "hogares_temporales.view_hogartemporal", "hogares_temporales.add_hogartemporal", "hogares_temporales.change_hogartemporal",
        "adopciones.view_solicitudadopcion", "adopciones.add_solicitudadopcion",
    ],
    "Administrador": [
        "reportes.view_reporte", "reportes.add_reporte", "reportes.change_reporte", "reportes.delete_reporte",
        "hogares_temporales.view_hogartemporal", "hogares_temporales.add_hogartemporal", "hogares_temporales.change_hogartemporal", "hogares_temporales.delete_hogartemporal",
        "adopciones.view_solicitudadopcion", "adopciones.add_solicitudadopcion", "adopciones.change_solicitudadopcion", "adopciones.delete_solicitudadopcion",
    ],
    "Solo lectura": [
        "reportes.view_reporte",
        "hogares_temporales.view_hogartemporal",
        # Solo puede ver SUS solicitudes (la vista filtra por usuario).
        "adopciones.view_solicitudadopcion",
    ],
}


class Command(BaseCommand):
    help = "Crea grupos Ciudadano, Voluntario, Administrador y Solo lectura, con permisos de acceso seguros."

    def handle(self, *args, **options):
        for nombre, codigos in PERMISOS_POR_GRUPO.items():
            Rol.objects.get_or_create(nombre_rol=nombre)
            grupo, _ = Group.objects.get_or_create(name=nombre)
            permisos = []
            for item in codigos:
                app, codename = item.split(".", 1)
                permisos.append(Permission.objects.get(content_type__app_label=app, codename=codename))
            if nombre == "Solo lectura":
                # Elimina permisos sobrantes que alguien hubiera asignado al grupo.
                grupo.permissions.set(permisos)
            else:
                # Conserva permisos especiales asignados anteriormente por el equipo.
                grupo.permissions.add(*permisos)
            self.stdout.write(self.style.SUCCESS(f"Grupo '{nombre}': configuración aplicada"))
        self.stdout.write("El registro público solo crea Ciudadanos. Superusuario se crea con createsuperuser.")
