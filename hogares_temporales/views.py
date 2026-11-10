from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect, render
from usuarios.security import perfil_de, es_administrador, denegar_escritura_lector
from .models import HogarTemporal
from .forms import HogarTemporalForm

@login_required
@permission_required("hogares_temporales.view_hogartemporal", raise_exception=True)
def lista(request):
    objetos = HogarTemporal.objects.select_related("usuario").order_by("-disponibilidad", "capacidad")
    return render(request, "hogares_temporales/lista.html", {"objetos": objetos})

@login_required
@permission_required("hogares_temporales.add_hogartemporal", raise_exception=True)
@denegar_escritura_lector
def crear(request):
    form = HogarTemporalForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        obj = form.save(commit=False)
        obj.usuario = perfil_de(request)
        obj.save()
        messages.success(request, "¡Gracias por ofrecer un hogar temporal!")
        return redirect("hogares_temporales:lista")
    return render(request, "crud/formulario.html", {"form": form, "titulo": "Ofrecer un hogar temporal", "descripcion": "Cada espacio disponible puede marcar una gran diferencia.", "cancelar_url": "hogares_temporales:lista"})

@login_required
@permission_required("hogares_temporales.change_hogartemporal", raise_exception=True)
@denegar_escritura_lector
def editar(request, pk):
    objeto = get_object_or_404(HogarTemporal, pk=pk)
    if not (es_administrador(request.user) or objeto.usuario.usuario_id == request.user.pk):
        raise PermissionDenied("No puedes modificar hogares ajenos.")
    form = HogarTemporalForm(request.POST or None, instance=objeto)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Datos del hogar actualizados.")
        return redirect("hogares_temporales:lista")
    return render(request, "crud/formulario.html", {"form": form, "titulo": "Actualizar hogar temporal", "cancelar_url": "hogares_temporales:lista"})

@login_required
@permission_required("hogares_temporales.delete_hogartemporal", raise_exception=True)
@denegar_escritura_lector
def eliminar(request, pk):
    objeto = get_object_or_404(HogarTemporal, pk=pk)
    if not (es_administrador(request.user) or objeto.usuario.usuario_id == request.user.pk):
        raise PermissionDenied("No puedes eliminar hogares ajenos.")
    if request.method == "POST":
        objeto.delete()
        messages.success(request, "Hogar temporal retirado de la lista.")
        return redirect("hogares_temporales:lista")
    return render(request, "crud/eliminar.html", {"objeto": objeto, "titulo": "Eliminar hogar temporal", "cancelar_url": "hogares_temporales:lista"})
