# Generated by Django 4.2.1 on 2023-11-08 15:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('servicios', '0017_remove_serviciolavadotanque_anexo_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='serviciolavadotanque',
            name='material_tanque',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='servicios.materialtanque'),
        ),
        migrations.AlterField(
            model_name='serviciolavadotanque',
            name='ubicacion_tanque',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='servicios.ubicaciontanque'),
        ),
    ]
