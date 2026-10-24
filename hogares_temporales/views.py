from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import HogarTemporalForm
from .models import HogarTemporal


@login_required
@permission_required("hogares_temporales.view_hogartemporal", raise_exception=True)
def lista(request):
    return render(request, "hogares_temporales/lista.html", {"objetos": HogarTemporal.objects.select_related("usuario").all()})


@login_required
@permission_required("hogares_temporales.add_hogartemporal", raise_exception=True)
def crear(request):
    form = HogarTemporalForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect("hogares_temporales:lista")
    return render(request, "crud/formulario.html", {"form": form, "titulo": "Crear hogar temporal", "cancelar_url": "hogares_temporales:lista"})


@login_required
@permission_required("hogares_temporales.change_hogartemporal", raise_exception=True)
def editar(request, pk):
    objeto = get_object_or_404(HogarTemporal, pk=pk)
    form = HogarTemporalForm(request.POST or None, instance=objeto)
    if form.is_valid():
        form.save()
        return redirect("hogares_temporales:lista")
    return render(request, "crud/formulario.html", {"form": form, "titulo": "Editar hogar temporal", "cancelar_url": "hogares_temporales:lista"})


@login_required
@permission_required("hogares_temporales.delete_hogartemporal", raise_exception=True)
def eliminar(request, pk):
    objeto = get_object_or_404(HogarTemporal, pk=pk)
    if request.method == "POST":
        objeto.delete()
        return redirect("hogares_temporales:lista")
    return render(request, "crud/eliminar.html", {"objeto": objeto, "titulo": "Eliminar hogar temporal", "cancelar_url": "hogares_temporales:lista"})
