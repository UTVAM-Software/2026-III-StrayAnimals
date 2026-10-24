# Generated for Stray Animals.
import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True
    dependencies = [
        ("usuarios", "0001_initial"),
    ]
    operations = [
        migrations.CreateModel(
            name="HogarTemporal",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("capacidad", models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1)])),
                ("disponibilidad", models.BooleanField(default=True)),
                ("usuario", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="hogares_temporales", to="usuarios.perfilusuario")),
            ],
            options={"ordering": ["-disponibilidad", "capacidad"], "verbose_name": "Hogar temporal", "verbose_name_plural": "Hogares temporales"},
        ),
    ]
