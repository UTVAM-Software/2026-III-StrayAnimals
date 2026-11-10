from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [("hogares_temporales", "0001_initial")]
    operations = [migrations.AddField(model_name="hogartemporal", name="zona", field=models.CharField(blank=True, help_text="Colonia o zona aproximada, sin dirección exacta", max_length=120))]
