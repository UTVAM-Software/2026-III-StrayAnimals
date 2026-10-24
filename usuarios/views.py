from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import Group, Permission, User
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect, render

from .forms import (
    CrearUsuarioForm, EditarUsuarioForm, GroupForm, PermissionForm,
    PerfilUsuarioForm, RolForm,
)
from .models import PerfilUsuario, Rol


@login_required
def inicio(request):
    return render(request, "inicio.html")


# ----- ROLES -----
@login_required
@permission_required("usuarios.view_rol", raise_exception=True)
def rol_lista(request):
    return render(request, "usuarios/rol_lista.html", {"objetos": Rol.objects.all()})


@login_required
@permission_required("usuarios.add_rol", raise_exception=True)
def rol_crear(request):
    form = RolForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect("usuarios:rol_lista")
    return render(request, "crud/formulario.html", {"form": form, "titulo": "Crear rol", "cancelar_url": "usuarios:rol_lista"})


@login_required
@permission_required("usuarios.change_rol", raise_exception=True)
def rol_editar(request, pk):
    objeto = get_object_or_404(Rol, pk=pk)
    form = RolForm(request.POST or None, instance=objeto)
    if form.is_valid():
        form.save()
        return redirect("usuarios:rol_lista")
    return render(request, "crud/formulario.html", {"form": form, "titulo": "Editar rol", "cancelar_url": "usuarios:rol_lista"})


@login_required
@permission_required("usuarios.delete_rol", raise_exception=True)
def rol_eliminar(request, pk):
    objeto = get_object_or_404(Rol, pk=pk)
    if request.method == "POST":
        objeto.delete()
        return redirect("usuarios:rol_lista")
    return render(request, "crud/eliminar.html", {"objeto": objeto, "titulo": "Eliminar rol", "cancelar_url": "usuarios:rol_lista"})


# ----- PERFILES -----
@login_required
@permission_required("usuarios.view_perfilusuario", raise_exception=True)
def perfil_lista(request):
    objetos = PerfilUsuario.objects.select_related("usuario", "rol")
    return render(request, "usuarios/perfil_lista.html", {"objetos": objetos})


@login_required
@permission_required("usuarios.add_perfilusuario", raise_exception=True)
def perfil_crear(request):
    form = PerfilUsuarioForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect("usuarios:perfil_lista")
    return render(request, "crud/formulario.html", {"form": form, "titulo": "Crear perfil", "cancelar_url": "usuarios:perfil_lista"})


@login_required
@permission_required("usuarios.change_perfilusuario", raise_exception=True)
def perfil_editar(request, pk):
    objeto = get_object_or_404(PerfilUsuario, pk=pk)
    form = PerfilUsuarioForm(request.POST or None, instance=objeto)
    if form.is_valid():
        form.save()
        return redirect("usuarios:perfil_lista")
    return render(request, "crud/formulario.html", {"form": form, "titulo": "Editar perfil", "cancelar_url": "usuarios:perfil_lista"})


@login_required
@permission_required("usuarios.delete_perfilusuario", raise_exception=True)
def perfil_eliminar(request, pk):
    objeto = get_object_or_404(PerfilUsuario, pk=pk)
    if request.method == "POST":
        objeto.delete()
        return redirect("usuarios:perfil_lista")
    return render(request, "crud/eliminar.html", {"objeto": objeto, "titulo": "Eliminar perfil", "cancelar_url": "usuarios:perfil_lista"})


# ----- DJANGO AUTH: USER -----
@login_required
@permission_required("auth.view_user", raise_exception=True)
def usuario_lista(request):
    return render(request, "usuarios/usuario_lista.html", {"usuarios": User.objects.prefetch_related("groups").all()})


@login_required
@permission_required("auth.add_user", raise_exception=True)
def usuario_crear(request):
    form = CrearUsuarioForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect("usuarios:usuario_lista")
    return render(request, "crud/formulario.html", {"form": form, "titulo": "Crear usuario", "cancelar_url": "usuarios:usuario_lista"})


@login_required
@permission_required("auth.change_user", raise_exception=True)
def usuario_editar(request, pk):
    objeto = get_object_or_404(User, pk=pk)
    form = EditarUsuarioForm(request.POST or None, instance=objeto)
    if form.is_valid():
        form.save()
        return redirect("usuarios:usuario_lista")
    return render(request, "crud/formulario.html", {"form": form, "titulo": "Editar usuario", "cancelar_url": "usuarios:usuario_lista"})


@login_required
@permission_required("auth.delete_user", raise_exception=True)
def usuario_eliminar(request, pk):
    objeto = get_object_or_404(User, pk=pk)
    if objeto.pk == request.user.pk:
        raise PermissionDenied("No puedes eliminar tu propia cuenta mientras tienes la sesión iniciada.")
    if request.method == "POST":
        objeto.delete()
        return redirect("usuarios:usuario_lista")
    return render(request, "crud/eliminar.html", {"objeto": objeto, "titulo": "Eliminar usuario", "cancelar_url": "usuarios:usuario_lista"})


# ----- DJANGO AUTH: GROUP -----
@login_required
@permission_required("auth.view_group", raise_exception=True)
def grupo_lista(request):
    return render(request, "usuarios/grupo_lista.html", {"objetos": Group.objects.prefetch_related("permissions").all()})


@login_required
@permission_required("auth.add_group", raise_exception=True)
def grupo_crear(request):
    form = GroupForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect("usuarios:grupo_lista")
    return render(request, "crud/formulario.html", {"form": form, "titulo": "Crear grupo", "cancelar_url": "usuarios:grupo_lista"})


@login_required
@permission_required("auth.change_group", raise_exception=True)
def grupo_editar(request, pk):
    objeto = get_object_or_404(Group, pk=pk)
    form = GroupForm(request.POST or None, instance=objeto)
    if form.is_valid():
        form.save()
        return redirect("usuarios:grupo_lista")
    return render(request, "crud/formulario.html", {"form": form, "titulo": "Editar grupo", "cancelar_url": "usuarios:grupo_lista"})


@login_required
@permission_required("auth.delete_group", raise_exception=True)
def grupo_eliminar(request, pk):
    objeto = get_object_or_404(Group, pk=pk)
    if request.method == "POST":
        objeto.delete()
        return redirect("usuarios:grupo_lista")
    return render(request, "crud/eliminar.html", {"objeto": objeto, "titulo": "Eliminar grupo", "cancelar_url": "usuarios:grupo_lista"})


# ----- DJANGO AUTH: PERMISSION -----
@login_required
@permission_required("auth.view_permission", raise_exception=True)
def permiso_lista(request):
    objetos = Permission.objects.select_related("content_type").all()
    return render(request, "usuarios/permiso_lista.html", {"objetos": objetos})


@login_required
@permission_required("auth.add_permission", raise_exception=True)
def permiso_crear(request):
    form = PermissionForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect("usuarios:permiso_lista")
    return render(request, "crud/formulario.html", {"form": form, "titulo": "Crear permiso", "cancelar_url": "usuarios:permiso_lista"})


@login_required
@permission_required("auth.change_permission", raise_exception=True)
def permiso_editar(request, pk):
    objeto = get_object_or_404(Permission, pk=pk)
    form = PermissionForm(request.POST or None, instance=objeto)
    if form.is_valid():
        form.save()
        return redirect("usuarios:permiso_lista")
    return render(request, "crud/formulario.html", {"form": form, "titulo": "Editar permiso", "cancelar_url": "usuarios:permiso_lista"})


@login_required
@permission_required("auth.delete_permission", raise_exception=True)
def permiso_eliminar(request, pk):
    objeto = get_object_or_404(Permission, pk=pk)
    if request.method == "POST":
        objeto.delete()
        return redirect("usuarios:permiso_lista")
    return render(request, "crud/eliminar.html", {"objeto": objeto, "titulo": "Eliminar permiso", "cancelar_url": "usuarios:permiso_lista"})
