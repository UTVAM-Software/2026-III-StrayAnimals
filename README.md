<<<<<<< HEAD
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
=======
# 2026-III-StrayAnimales
>>>>>>> d66b5d73da600342086f0350e89a7b8f062632cc
