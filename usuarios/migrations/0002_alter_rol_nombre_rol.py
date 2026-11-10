# Agrega Solo lectura a las opciones del modelo sin borrar registros existentes.
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [("usuarios", "0001_initial")]

    operations = [
        migrations.AlterField(
            model_name="rol",
            name="nombre_rol",
            field=models.CharField(
                max_length=30,
                unique=True,
                choices=[
                    ("Administrador", "Administrador"),
                    ("Voluntario", "Voluntario"),
                    ("Ciudadano", "Ciudadano"),
                    ("Solo lectura", "Solo lectura"),
                ],
            ),
        ),
    ]
