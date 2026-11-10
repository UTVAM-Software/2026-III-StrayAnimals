from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [("adopciones", "0001_initial")]
    operations = [migrations.AddField(model_name="solicitudadopcion", name="motivo", field=models.TextField(blank=True, help_text="¿Por qué te gustaría adoptar?"))]
