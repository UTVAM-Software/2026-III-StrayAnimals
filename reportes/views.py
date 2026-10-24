from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import ReporteForm
from .models import Reporte


@login_required
@permission_required("reportes.view_reporte", raise_exception=True)
def lista(request):
    return render(request, "reportes/lista.html", {"objetos": Reporte.objects.select_related("usuario").all()})


@login_required
@permission_required("reportes.add_reporte", raise_exception=True)
def crear(request):
    form = ReporteForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        return redirect("reportes:lista")
    return render(request, "crud/formulario.html", {"form": form, "titulo": "Crear reporte", "cancelar_url": "reportes:lista", "multipart": True})


@login_required
@permission_required("reportes.change_reporte", raise_exception=True)
def editar(request, pk):
    objeto = get_object_or_404(Reporte, pk=pk)
    form = ReporteForm(request.POST or None, request.FILES or None, instance=objeto)
    if form.is_valid():
        form.save()
        return redirect("reportes:lista")
    return render(request, "crud/formulario.html", {"form": form, "titulo": "Editar reporte", "cancelar_url": "reportes:lista", "multipart": True})


@login_required
@permission_required("reportes.delete_reporte", raise_exception=True)
def eliminar(request, pk):
    objeto = get_object_or_404(Reporte, pk=pk)
    if request.method == "POST":
        objeto.delete()
        return redirect("reportes:lista")
    return render(request, "crud/eliminar.html", {"objeto": objeto, "titulo": "Eliminar reporte", "cancelar_url": "reportes:lista"})
