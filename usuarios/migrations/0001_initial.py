# Generated for Stray Animals.
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]
    operations = [
        migrations.CreateModel(
            name="Rol",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("nombre_rol", models.CharField(choices=[("Administrador", "Administrador"), ("Voluntario", "Voluntario"), ("Ciudadano", "Ciudadano")], max_length=30, unique=True)),
            ],
            options={"ordering": ["nombre_rol"], "verbose_name": "Rol", "verbose_name_plural": "Roles"},
        ),
        migrations.CreateModel(
            name="PerfilUsuario",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("nombre", models.CharField(max_length=100)),
                ("correo", models.EmailField(max_length=150, unique=True)),
                ("rol", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="perfiles", to="usuarios.rol")),
                ("usuario", models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name="perfil_stray_animals", to=settings.AUTH_USER_MODEL)),
            ],
            options={"ordering": ["nombre"], "verbose_name": "Perfil de usuario", "verbose_name_plural": "Perfiles de usuario"},
        ),
    ]
