# Generated for Stray Animals.
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True
    dependencies = [
        ("reportes", "0001_initial"),
        ("usuarios", "0001_initial"),
    ]
    operations = [
        migrations.CreateModel(
            name="SolicitudAdopcion",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("estado_solicitud", models.CharField(choices=[("Pendiente", "Pendiente"), ("Aprobada", "Aprobada"), ("Rechazada", "Rechazada")], default="Pendiente", max_length=10)),
                ("fecha_solicitud", models.DateTimeField(auto_now_add=True)),
                ("reporte", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="solicitudes_adopcion", to="reportes.reporte")),
                ("usuario_interesado", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="solicitudes_adopcion", to="usuarios.perfilusuario")),
            ],
            options={"ordering": ["-fecha_solicitud"], "verbose_name": "Solicitud de adopción", "verbose_name_plural": "Solicitudes de adopción"},
        ),
    ]
