from django.urls import path
from . import views

app_name = "usuarios"

urlpatterns = [
    path("roles/", views.rol_lista, name="rol_lista"),
    path("roles/crear/", views.rol_crear, name="rol_crear"),
    path("roles/<int:pk>/editar/", views.rol_editar, name="rol_editar"),
    path("roles/<int:pk>/eliminar/", views.rol_eliminar, name="rol_eliminar"),

    path("perfiles/", views.perfil_lista, name="perfil_lista"),
    path("perfiles/crear/", views.perfil_crear, name="perfil_crear"),
    path("perfiles/<int:pk>/editar/", views.perfil_editar, name="perfil_editar"),
    path("perfiles/<int:pk>/eliminar/", views.perfil_eliminar, name="perfil_eliminar"),

    path("auth/usuarios/", views.usuario_lista, name="usuario_lista"),
    path("auth/usuarios/crear/", views.usuario_crear, name="usuario_crear"),
    path("auth/usuarios/<int:pk>/editar/", views.usuario_editar, name="usuario_editar"),
    path("auth/usuarios/<int:pk>/eliminar/", views.usuario_eliminar, name="usuario_eliminar"),

    path("auth/grupos/", views.grupo_lista, name="grupo_lista"),
    path("auth/grupos/crear/", views.grupo_crear, name="grupo_crear"),
    path("auth/grupos/<int:pk>/editar/", views.grupo_editar, name="grupo_editar"),
    path("auth/grupos/<int:pk>/eliminar/", views.grupo_eliminar, name="grupo_eliminar"),

    path("auth/permisos/", views.permiso_lista, name="permiso_lista"),
    path("auth/permisos/crear/", views.permiso_crear, name="permiso_crear"),
    path("auth/permisos/<int:pk>/editar/", views.permiso_editar, name="permiso_editar"),
    path("auth/permisos/<int:pk>/eliminar/", views.permiso_eliminar, name="permiso_eliminar"),
]
