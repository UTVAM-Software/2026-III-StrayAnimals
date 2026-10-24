# Entregable 3 — Stray Animals

## Funcionalidad implementada

- Login y Logout mediante Django Auth.
- CRUD/Listado de Rol y PerfilUsuario.
- CRUD/Listado de Reporte.
- CRUD/Listado de HogarTemporal.
- CRUD/Listado de SolicitudAdopcion.
- CRUD/Listado de Django Auth: User, Group y Permission.
- Asignación de permisos directos y grupos a User.
- Asignación de permisos a Group.
- Control de acceso en servidor con `login_required` y `permission_required`.
- Respuesta 403 para usuarios autenticados sin permiso.

## Rutas principales

- `/login/`
- `/logout/`
- `/`
- `/reportes/`
- `/hogares-temporales/`
- `/adopciones/`
- `/usuarios/roles/`
- `/usuarios/perfiles/`
- `/usuarios/auth/usuarios/`
- `/usuarios/auth/grupos/`
- `/usuarios/auth/permisos/`
- `/admin/`

## Comprobación local

```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py makemigrations --check
python manage.py check
python manage.py runserver
```

## Evidencia recomendada de OWASP A01

1. Crear un usuario normal sin permisos.
2. Intentar entrar directamente a `/reportes/` o `/usuarios/auth/usuarios/`.
3. Capturar el 403.
4. Asignar el permiso de visualización correspondiente.
5. Repetir la URL y capturar el acceso autorizado.
6. Probar permisos separados para crear, cambiar y eliminar.

## Flujo GitHub

```bash
git checkout -b feature/entregable-3
git add .
git commit -m "Implementa autenticacion CRUD y control de accesos"
git push -u origin feature/entregable-3
```

Después crear Pull Request hacia la rama principal, solicitar revisión, aprobación y hacer merge.
