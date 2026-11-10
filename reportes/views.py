
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.core.exceptions import PermissionDenied
from django.db.models.deletion import ProtectedError
from django.shortcuts import get_object_or_404, redirect, render

from .models import Reporte
from .forms import ReporteForm, ReporteGestionForm

from usuarios.security import (
    perfil_de,
    es_coordinador,
    es_administrador,
    denegar_escritura_lector,
)


# ==========================================
# LISTAR REPORTES
# ==========================================

@login_required
@permission_required("reportes.view_reporte", raise_exception=True)
def lista(request):

    estado = request.GET.get("estado", "Todos")

    datos = Reporte.objects.select_related(
        "usuario"
    ).order_by("-fecha_creacion")

    if estado in Reporte.Estatus.values:
        datos = datos.filter(estatus=estado)
    else:
        estado = "Todos"

    return render(
        request,
        "reportes/lista.html",
        {
            "objetos": datos,
            "estado": estado,
            "estados": Reporte.Estatus.choices,
        }
    )


# ==========================================
# VER DETALLES DE UN REPORTE
# ==========================================

@login_required
@permission_required("reportes.view_reporte", raise_exception=True)
def detalle(request, pk):

    objeto = get_object_or_404(
        Reporte.objects.select_related("usuario"),
        pk=pk
    )

    return render(
        request,
        "reportes/detalle.html",
        {"objeto": objeto}
    )


# ==========================================
# CREAR REPORTE
# ==========================================

@login_required
@permission_required("reportes.add_reporte", raise_exception=True)
@denegar_escritura_lector
def crear(request):

    form = ReporteForm(
        request.POST or None,
        request.FILES or None
    )

    if request.method == "POST" and form.is_valid():

        objeto = form.save(commit=False)

        objeto.usuario = perfil_de(request)
        objeto.estatus = Reporte.Estatus.REPORTADO

        objeto.save()

        messages.success(
            request,
            "Gracias por compartir este caso. ¡Ya está registrado!"
        )

        return redirect("reportes:lista")

    return render(
        request,
        "crud/formulario.html",
        {
            "form": form,
            "titulo": "Compartir un reporte",
            "descripcion": "Tu aviso puede ayudar a que alguien lo encuentre y lo acompañe.",
            "cancelar_url": "reportes:lista",
            "multipart": True,
        }
    )


# ==========================================
# EDITAR REPORTE
# ==========================================

@login_required
@permission_required("reportes.change_reporte", raise_exception=True)
@denegar_escritura_lector
def editar(request, pk):

    objeto = get_object_or_404(
        Reporte,
        pk=pk
    )

    if not (
        es_coordinador(request.user)
        or objeto.usuario.usuario_id == request.user.pk
    ):
        raise PermissionDenied(
            "No puedes modificar reportes de otras personas."
        )

    form = ReporteGestionForm(
        request.POST or None,
        request.FILES or None,
        instance=objeto
    )

    if request.method == "POST" and form.is_valid():

        form.save()

        messages.success(
            request,
            "Reporte actualizado correctamente."
        )

        return redirect("reportes:lista")

    return render(
        request,
        "crud/formulario.html",
        {
            "form": form,
            "titulo": "Actualizar reporte",
            "cancelar_url": "reportes:lista",
            "multipart": True,
        }
    )


# ==========================================
# ELIMINAR REPORTE
# ==========================================

@login_required
@permission_required("reportes.delete_reporte", raise_exception=True)
@denegar_escritura_lector
def eliminar(request, pk):

    objeto = get_object_or_404(
        Reporte,
        pk=pk
    )

    if not (
        es_administrador(request.user)
        or objeto.usuario.usuario_id == request.user.pk
    ):
        raise PermissionDenied(
            "No puedes eliminar reportes de otras personas."
        )

    if request.method == "POST":

        try:
            objeto.delete()

            messages.success(
                request,
                "Reporte eliminado correctamente."
            )

        except ProtectedError:

            messages.error(
                request,
                "Este reporte tiene solicitudes vinculadas. "
                "Revisa primero esas solicitudes."
            )

        return redirect("reportes:lista")

    return render(
        request,
        "crud/eliminar.html",
        {
            "objeto": objeto,
            "titulo": "Eliminar reporte",
            "cancelar_url": "reportes:lista",
        }
    )
