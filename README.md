# Stray Animals — Acceso por usuario, superusuario y Solo lectura

Esta versión incorpora **tres tipos de acceso** al proyecto Django + SQLite y conserva los modelos, migraciones, vistas y diseño acogedor de Stray Animals.

## 1. Tipos de cuenta

| Tipo | Forma de alta | Acceso |
|---|---|---|
| Usuario (Ciudadano) | `/registro/` | Consultar reportes y hogares; registrar reportes, hogares y solicitudes propias. |
| Superusuario | `python manage.py createsuperuser` | Administrar todos los modelos y Django Auth (`User`, `Group`, `Permission`) y acceder a `/admin/`. |
| Solo lectura | `python manage.py crear_lector ...` | Consultar reportes, hogares y la lista de solicitudes propias; sin crear, editar ni eliminar. |

**Importante:** todos utilizan la **misma pantalla** `/login/`, con sus credenciales individuales. No existe un selector de roles que permita asumir privilegios. Los permisos de acceso se verifican **en el servidor** mediante Django Auth, decoradores y middleware.

Las cuentas de **Voluntario** y **Administrador** del Entregable anterior siguen estando definidas y no se eliminan, pero este cambio añade específicamente el acceso de Solo lectura y destaca los tres perfiles solicitados.

## 2. Integrar sin perder tu base de datos

1. Haz copia de seguridad de tu carpeta Django y de `db.sqlite3`.
2. Descomprime el ZIP y copia sus archivos encima del proyecto existente, junto a `manage.py`.
3. **No sustituyas `db.sqlite3` ni `.git`**: no vienen incluidos en el ZIP.
4. Si tienes cambios de compañeros en `reportes/views.py` o `adopciones/views.py`, revisa los cambios antes de sobrescribirlos.
5. Abre VS Code y activa tu entorno virtual existente.

```powershell
pip install -r requirements.txt
python manage.py migrate
python manage.py configurar_roles
python manage.py makemigrations --check
python manage.py check
python manage.py test
python manage.py runserver
```

`migrate` aplica la nueva migración `usuarios/migrations/0002_alter_rol_nombre_rol.py` y conserva tus datos. `configurar_roles` asegura los cuatro grupos **Ciudadano, Voluntario, Administrador, Solo lectura**. El grupo de Solo lectura se reinicia para incluir **solo** permisos `view_*` en los tres módulos.

## 3. Crear las cuentas

### A. Cuenta Usuario

Abre `http://127.0.0.1:8000/registro/`. Se crea automáticamente la cuenta nativa `User` de Django y un `PerfilUsuario` con rol **Ciudadano**. Esa persona puede iniciar sesión en `/login/`.

### B. Cuenta Superusuario

Si ya tienes un superusuario, **usa el existente**. Si no tienes:

```powershell
python manage.py createsuperuser
```

La cuenta debe tener `is_superuser=True` e `is_staff=True` para acceder a `/admin/`. Nunca permitas que una persona se haga superusuario por el formulario de registro público.

### C. Cuenta Solo lectura

Ejecuta en PowerShell (cambia los valores por los tuyos):

```powershell
python manage.py crear_lector lector01 --nombre "Invitado de consulta" --correo "lector01@example.com"
```

El comando solicita la contraseña dos veces, **sin mostrarla en pantalla**. Nunca incluyas contraseñas en comandos o repositorios.

La cuenta recibe `Group: Solo lectura`, `Rol: Solo lectura`, `is_staff=False` e `is_superuser=False` y un perfil. Después inicia sesión en `/login/` usando `lector01` y la contraseña creada.

**Alternativa en el panel `/admin/`:** un superusuario puede crear un `User` normal, asignarlo únicamente al grupo `Solo lectura`, mantener desactivados *Es parte del staff* y *Es superusuario* y crear su `PerfilUsuario` con Rol `Solo lectura` y correo único.

## 4. Cómo se aplica la protección OWASP A01

- El grupo `Solo lectura` recibe únicamente `view_reporte`, `view_hogartemporal` y `view_solicitudadopcion`.
- La vista de solicitudes de adopción **filtra por usuario**: el lector no ve solicitudes privadas de otras personas.
- El middleware `usuarios.middleware.RestringirEscrituraSoloLectura` bloquea métodos inseguros (POST, PUT, PATCH, DELETE) para ese grupo; se permite el POST de cierre de sesión.
- Las vistas de escritura además usan `@denegar_escritura_lector`, `@login_required` y `@permission_required`.
- Las plantillas ocultan botones de escritura a cuentas de Solo lectura; **ocultar botones no sustituye el control en el servidor**.
- Los usuarios normales no pueden administrar `User`, `Group` y `Permission`: esas vistas están reservadas al superusuario.
- Un usuario con la combinación contradictoria `Solo lectura` + permiso de crear se mantiene de Solo lectura.

## 5. Verificaciones

```powershell
python manage.py test usuarios.test_tipos_acceso usuarios.tests reportes.tests
```

También puedes probar manualmente:

1. Login de `lector01` → `/reportes/` debe funcionar.
2. Intentar `/reportes/crear/` → **403**.
3. Intentar enviar un POST de creación → **403**.
4. `/mi-perfil/` → muestra la información sin permitir editar.
5. Logout → debe cerrar sesión correctamente.
6. Login de ciudadano → puede crear reportes.
7. Login de superusuario → puede entrar a `/admin/` y administrar usuarios.

**Aviso de pruebas:** se comprobó la sintaxis de Python y la estructura del proyecto. No se pudo instalar Django dentro del entorno de preparación para ejecutar pruebas de integración; ejecútalas en tu VS Code antes de hacer Pull Request.

## 6. GitHub

Agrega solo los archivos de este cambio a una rama nueva y abre un Pull Request hacia `main`. **No agregues `db.sqlite3`, `.venv` o contraseñas**. Si `reportes/views.py` y `adopciones/views.py` le corresponden a tu compañero, coordinen su integración antes del merge.
