from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import SolicitudAdopcionForm
from .models import SolicitudAdopcion


@login_required
@permission_required("adopciones.view_solicitudadopcion", raise_exception=True)
def lista(request):
    objetos = SolicitudAdopcion.objects.select_related("reporte", "usuario_interesado").all()
    return render(request, "adopciones/lista.html", {"objetos": objetos})


@login_required
@permission_required("adopciones.add_solicitudadopcion", raise_exception=True)
def crear(request):
    form = SolicitudAdopcionForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect("adopciones:lista")
    return render(request, "crud/formulario.html", {"form": form, "titulo": "Crear solicitud de adopción", "cancelar_url": "adopciones:lista"})


@login_required
@permission_required("adopciones.change_solicitudadopcion", raise_exception=True)
def editar(request, pk):
    objeto = get_object_or_404(SolicitudAdopcion, pk=pk)
    form = SolicitudAdopcionForm(request.POST or None, instance=objeto)
    if form.is_valid():
        form.save()
        return redirect("adopciones:lista")
    return render(request, "crud/formulario.html", {"form": form, "titulo": "Editar solicitud de adopción", "cancelar_url": "adopciones:lista"})


@login_required
@permission_required("adopciones.delete_solicitudadopcion", raise_exception=True)
def eliminar(request, pk):
    objeto = get_object_or_404(SolicitudAdopcion, pk=pk)
    if request.method == "POST":
        objeto.delete()
        return redirect("adopciones:lista")
    return render(request, "crud/eliminar.html", {"objeto": objeto, "titulo": "Eliminar solicitud de adopción", "cancelar_url": "adopciones:lista"})
