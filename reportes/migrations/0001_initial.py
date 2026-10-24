# Generated for Stray Animals.
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True
    dependencies = [
        ("usuarios", "0001_initial"),
    ]
    operations = [
        migrations.CreateModel(
            name="Reporte",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("descripcion", models.TextField()),
                ("fotografia", models.ImageField(blank=True, null=True, upload_to="reportes/")),
                ("ubicacion", models.CharField(max_length=255)),
                ("prioridad", models.CharField(choices=[("Baja", "Baja"), ("Media", "Media"), ("Alta", "Alta")], default="Media", max_length=10)),
                ("estatus", models.CharField(choices=[("Reportado", "Reportado"), ("Rescatado", "Rescatado"), ("Temporal", "Temporal"), ("Adoptado", "Adoptado")], default="Reportado", max_length=15)),
                ("fecha_creacion", models.DateTimeField(auto_now_add=True)),
                ("usuario", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="reportes", to="usuarios.perfilusuario")),
            ],
            options={"ordering": ["-fecha_creacion"], "verbose_name": "Reporte", "verbose_name_plural": "Reportes"},
        ),
    ]
