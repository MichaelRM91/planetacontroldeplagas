# Generated by Django 4.2.1 on 2024-01-05 21:52

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('servicios', '0015_servicio_fecha_inicio'),
    ]

    operations = [
        migrations.AlterField(
            model_name='servicio',
            name='fecha_inicio',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
