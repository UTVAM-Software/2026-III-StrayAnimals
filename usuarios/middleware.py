from django.core.exceptions import PermissionDenied
from django.utils.deprecation import MiddlewareMixin
from .security import es_solo_lectura


class RestringirEscrituraSoloLectura(MiddlewareMixin):
    """Defensa adicional: una cuenta de consulta no puede enviar POST/PUT/PATCH/DELETE.

    Se permite POST a logout para que la persona pueda cerrar sesión; las vistas
    de lectura y las comprobaciones de permisos siguen siendo independientes.
    """

    def process_view(self, request, view_func, view_args, view_kwargs):
        if request.method in ("GET", "HEAD", "OPTIONS"):
            return None
        if not es_solo_lectura(request.user):
            return None
        match = request.resolver_match
        if match is not None and match.url_name == "logout":
            return None
        raise PermissionDenied("Acceso Solo lectura: no está permitido modificar información.")
