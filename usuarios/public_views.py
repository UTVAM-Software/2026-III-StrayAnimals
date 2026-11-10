from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.db import transaction
from django.shortcuts import redirect, render
from django.views.decorators.http import require_http_methods
from reportes.models import Reporte
from hogares_temporales.models import HogarTemporal
from adopciones.models import SolicitudAdopcion
from .models import PerfilUsuario, Rol
from .public_forms import EditarMiPerfilForm, RegistroCiudadanoForm
from .security import perfil_de, es_solo_lectura


def portada(request):
    ultimos = Reporte.objects.order_by("-fecha_creacion")[:3]
    return render(request, "inicio.html", {
        "ultimos": ultimos,
        "total_reportes": Reporte.objects.count(),
        "total_adoptados": Reporte.objects.filter(estatus=Reporte.Estatus.ADOPTADO).count(),
        "total_hogares": HogarTemporal.objects.filter(disponibilidad=True).count(),
    })


def acerca(request):
    return render(request, "acerca.html")


@require_http_methods(["GET", "POST"])
def registro(request):
    if request.user.is_authenticated:
        return redirect("inicio")
    form = RegistroCiudadanoForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        with transaction.atomic():
            user = form.save(commit=False)
            user.email = form.cleaned_data["email"]
            user.first_name = form.cleaned_data["nombre"][:150]
            user.is_staff = False
            user.is_superuser = False
            user.save()
            rol, _ = Rol.objects.get_or_create(nombre_rol=Rol.NombreRol.CIUDADANO)
            PerfilUsuario.objects.create(usuario=user, nombre=form.cleaned_data["nombre"], correo=form.cleaned_data["email"], rol=rol)
            group, _ = Group.objects.get_or_create(name="Ciudadano")
            user.groups.add(group)
        login(request, user)
        messages.success(request, "¡Bienvenido a la comunidad! Tu cuenta está lista.")
        return redirect("inicio")
    return render(request, "registration/registro.html", {"form": form})


@login_required
def mi_perfil(request):
    perfil = perfil_de(request)
    if request.method == "POST" and es_solo_lectura(request.user):
        from django.core.exceptions import PermissionDenied
        raise PermissionDenied("Tu cuenta es de Solo lectura.")
    form = None if es_solo_lectura(request.user) else EditarMiPerfilForm(request.POST or None, instance=perfil)
    if request.method == "POST" and form.is_valid():
        with transaction.atomic():
            actualizado = form.save()
            request.user.email = actualizado.correo
            request.user.first_name = actualizado.nombre[:150]
            request.user.save(update_fields=["email", "first_name"])
        messages.success(request, "Tus datos se actualizaron correctamente.")
        return redirect("mi_perfil")
    return render(request, "usuarios/mi_perfil.html", {"form": form, "perfil": perfil})
