from getpass import getpass
from django.contrib.auth.models import Group, User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.core.management.base import BaseCommand, CommandError
from django.core.validators import validate_email
from django.db import transaction
from usuarios.models import PerfilUsuario, Rol


class Command(BaseCommand):
    help = "Crea una cuenta de Solo lectura con contraseña solicitada en consola (nunca en argumentos)."

    def add_arguments(self, parser):
        parser.add_argument("username", help="Nombre de inicio de sesión del lector")
        parser.add_argument("--nombre", required=True, help="Nombre que aparecerá en el perfil")
        parser.add_argument("--correo", required=True, help="Correo único del lector")

    def handle(self, *args, **options):
        username = options["username"].strip()
        nombre = options["nombre"].strip()
        correo = options["correo"].strip().lower()
        if not username or not nombre:
            raise CommandError("El usuario y el nombre no pueden estar vacíos.")
        try:
            validate_email(correo)
        except ValidationError as exc:
            raise CommandError("El correo electrónico no es válido.") from exc
        if User.objects.filter(username=username).exists():
            raise CommandError("Ya existe este nombre de usuario.")
        if User.objects.filter(email__iexact=correo).exists() or PerfilUsuario.objects.filter(correo__iexact=correo).exists():
            raise CommandError("Este correo ya está registrado.")
        try:
            clave = getpass("Contraseña: ")
            if clave != getpass("Repite la contraseña: "):
                raise CommandError("Las contraseñas no coinciden.")
            validate_password(clave)
        except ValidationError as exc:
            raise CommandError("Contraseña no válida: " + "; ".join(exc.messages)) from exc
        with transaction.atomic():
            rol, _ = Rol.objects.get_or_create(nombre_rol=Rol.NombreRol.SOLO_LECTURA)
            grupo, _ = Group.objects.get_or_create(name="Solo lectura")
            usuario = User.objects.create_user(
                username=username, email=correo, password=clave,
                first_name=nombre[:150], is_staff=False, is_superuser=False,
            )
            usuario.groups.set([grupo])
            PerfilUsuario.objects.create(usuario=usuario, nombre=nombre, correo=correo, rol=rol)
        self.stdout.write(self.style.SUCCESS(f"Lector '{username}' creado. Solo puede consultar la plataforma."))
