# Stray Animals — Entregable 2-B

Proyecto base Django con ORM modular, migraciones iniciales y diagramas de base de datos en formatos de imagen.

## Aplicaciones por módulo

- `usuarios`: roles y perfil asociado al usuario de autenticación de Django.
- `reportes`: reportes de perros en situación de calle.
- `hogares_temporales`: capacidad y disponibilidad de hogares temporales.
- `adopciones`: solicitudes de adopción relacionadas con un reporte y un usuario.

Se utiliza el modelo de autenticación predeterminado de Django para no romper una instalación que ya tenga superusuario creado. Los datos propios del proyecto (nombre, correo de contacto y rol) se almacenan en `PerfilUsuario`, relacionado uno a uno con `auth.User`.

## Requisitos

Python 3.10 o posterior recomendado.

## Instalación en Windows (PowerShell o CMD)

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Abrir `http://127.0.0.1:8000/admin/`.

Si ya tienes un proyecto Django y un superusuario, copia las carpetas de apps y adapta `INSTALLED_APPS`, las rutas y las migraciones. No reemplaces tu `settings.py` sin respaldarlo.

## Migraciones

Las migraciones iniciales están incluidas en `migrations/`. Para comprobarlas o generar una migración nueva después de modificar modelos:

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py showmigrations
```

## Diagramas

Los esquemas del modelo conceptual y lógico están en `documentacion/base_datos/` como SVG. No se incluyen PDF en esa carpeta.

## Git y Pull Request

```bash
git checkout -b feature/modelos-orm
git add .
git commit -m "Agrega modelos ORM y migraciones de Stray Animals"
git push -u origin feature/modelos-orm
```

En GitHub, crear un Pull Request hacia `main` (o la rama principal definida por el equipo), solicitar revisión, atender comentarios y fusionarlo únicamente cuando esté aprobado. Verificar que el PR aparezca como merged.

## Notas del modelo

- Las claves primarias y foráneas se generan mediante Django.
- Las contraseñas las administra Django con su mecanismo de hash; nunca se guardan contraseñas en texto plano.
- La fotografía de un reporte es opcional; para cargar imágenes se necesita Pillow.
- Las solicitudes de adopción guardan el estado `Pendiente`, `Aprobada` o `Rechazada`.


## Entregable 3 — Autenticación, CRUD y Control de Acceso

Se integraron:

- Login y Logout con Django Auth.
- Redirecciones `LOGIN_REDIRECT_URL` y `LOGOUT_REDIRECT_URL`.
- CRUD/Listado de `Rol`, `PerfilUsuario`, `Reporte`, `HogarTemporal` y `SolicitudAdopcion`.
- CRUD/Listado desde la propia aplicación de Django Auth: `User`, `Group` y `Permission`.
- Asignación de grupos y permisos directos a usuarios.
- Asignación de permisos a grupos.
- Protección explícita de cada vista con `@login_required` y `@permission_required(..., raise_exception=True)` para mitigar OWASP A01 Broken Access Control.
- Protección para impedir que un usuario elimine su propia cuenta durante una sesión activa.

### Comandos de comprobación

```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py makemigrations --check
python manage.py check
python manage.py runserver
```

Después abre `http://127.0.0.1:8000/login/`.

### Prueba recomendada de Broken Access Control

1. Inicia sesión como superusuario y crea un usuario normal.
2. Intenta acceder a `/usuarios/auth/usuarios/` con ese usuario sin `auth.view_user`: debe responder 403.
3. Asigna el permiso `Can view user` desde un grupo o directamente al usuario.
4. Repite el acceso: ahora debe permitirse el listado.
5. Comprueba lo mismo para agregar, cambiar y eliminar.
