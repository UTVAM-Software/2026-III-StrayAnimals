from functools import wraps
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from .models import PerfilUsuario, Rol


def es_solo_lectura(user):
    """El grupo Solo lectura prima sobre permisos sueltos; nunca limita al superusuario."""
    return (
        user.is_authenticated
        and not user.is_superuser
        and user.groups.filter(name="Solo lectura").exists()
    )


def denegar_escritura_lector(view):
    """Bloquea mutaciones incluso cuando el usuario tiene permisos directos contradictorios."""
    @wraps(view)
    @login_required
    def wrapped(request, *args, **kwargs):
        if es_solo_lectura(request.user):
            raise PermissionDenied("Tu cuenta es de Solo lectura. No puedes crear, editar ni eliminar registros.")
        return view(request, *args, **kwargs)
    return wrapped


def solo_superusuario(view):
    @wraps(view)
    @login_required
    def wrapped(request, *args, **kwargs):
        if not request.user.is_superuser:
            raise PermissionDenied("Esta operación está reservada al superusuario.")
        return view(request, *args, **kwargs)
    return wrapped


def perfil_de(request):
    try:
        return request.user.perfil_stray_animals
    except PerfilUsuario.DoesNotExist:
        if not request.user.is_superuser:
            raise PermissionDenied("Esta cuenta todavía no tiene perfil de Stray Animals. Solicita al administrador que lo configure.")
        rol, _ = Rol.objects.get_or_create(nombre_rol=Rol.NombreRol.ADMINISTRADOR)
        nombre = request.user.get_full_name() or request.user.username
        correo = request.user.email or f"{request.user.username}@local.invalid"
        perfil, _ = PerfilUsuario.objects.get_or_create(usuario=request.user, defaults={"nombre": nombre, "correo": correo, "rol": rol})
        return perfil


def es_coordinador(user):
    if not user.is_authenticated or es_solo_lectura(user):
        return False
    return user.is_superuser or user.groups.filter(name__in=["Administrador", "Voluntario"]).exists()


def es_administrador(user):
    if not user.is_authenticated or es_solo_lectura(user):
        return False
    return user.is_superuser or user.groups.filter(name="Administrador").exists()
