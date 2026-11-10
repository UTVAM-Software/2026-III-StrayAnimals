
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect, render

from usuarios.security import (
    perfil_de,
    es_administrador,
    denegar_escritura_lector,
)

from .models import SolicitudAdopcion
from .forms import SolicitudAdopcionForm, SolicitudGestionForm


# ==========================================
# LISTAR SOLICITUDES DE ADOPCIÓN
# ==========================================

@login_required
@permission_required(
    "adopciones.view_solicitudadopcion",
    raise_exception=True
)
def lista(request):

    objetos = SolicitudAdopcion.objects.select_related(
        "reporte",
        "usuario_interesado"
    ).order_by("-fecha_solicitud")

    if not es_administrador(request.user):
        objetos = objetos.filter(
            usuario_interesado__usuario=request.user
        )

    return render(
        request,
        "adopciones/lista.html",
        {
            "objetos": objetos,
            "puede_revisar": es_administrador(request.user)
        }
    )


# ==========================================
# CREAR SOLICITUD DE ADOPCIÓN
# ==========================================

@login_required
@permission_required(
    "adopciones.add_solicitudadopcion",
    raise_exception=True
)
@denegar_escritura_lector
def crear(request):

    form = SolicitudAdopcionForm(
        request.POST or None
    )

    if request.method == "POST" and form.is_valid():

        objeto = form.save(commit=False)

        objeto.usuario_interesado = perfil_de(request)

        objeto.estado_solicitud = (
            SolicitudAdopcion.EstadoSolicitud.PENDIENTE
        )

        objeto.save()

        messages.success(
            request,
            "Tu solicitud fue recibida. ¡Gracias por querer adoptar!"
        )

        return redirect("adopciones:lista")

    return render(
        request,
        "crud/formulario.html",
        {
            "form": form,
            "titulo": "Solicitar adopción",
            "descripcion": "Adoptar es abrir un lugar en casa y en el corazón.",
            "cancelar_url": "adopciones:lista"
        }
    )


# ==========================================
# EDITAR Y REVISAR SOLICITUDES
# ==========================================

@login_required
@permission_required(
    "adopciones.change_solicitudadopcion",
    raise_exception=True
)
@denegar_escritura_lector
def editar(request, pk):

    objeto = get_object_or_404(
        SolicitudAdopcion,
        pk=pk
    )

    if not es_administrador(request.user):
        raise PermissionDenied(
            "La aprobación de solicitudes está reservada a administradores."
        )

    form = SolicitudGestionForm(
        request.POST or None,
        instance=objeto
    )

    if request.method == "POST" and form.is_valid():

        form.save()

        messages.success(
            request,
            "Solicitud actualizada correctamente."
        )

        return redirect("adopciones:lista")

    return render(
        request,
        "crud/formulario.html",
        {
            "form": form,
            "titulo": "Revisar solicitud",
            "cancelar_url": "adopciones:lista"
        }
    )


# ==========================================
# ELIMINAR SOLICITUDES
# ==========================================

@login_required
@permission_required(
    "adopciones.delete_solicitudadopcion",
    raise_exception=True
)
@denegar_escritura_lector
def eliminar(request, pk):

    objeto = get_object_or_404(
        SolicitudAdopcion,
        pk=pk
    )

    if not (
        es_administrador(request.user)
        or objeto.usuario_interesado.usuario_id == request.user.pk
    ):
        raise PermissionDenied(
            "No puedes eliminar solicitudes ajenas."
        )

    if request.method == "POST":

        objeto.delete()

        messages.success(
            request,
            "Solicitud eliminada correctamente."
        )

        return redirect("adopciones:lista")

    return render(
        request,
        "crud/eliminar.html",
        {
            "objeto": objeto,
            "titulo": "Eliminar solicitud",
            "cancelar_url": "adopciones:lista"
        }
    )
