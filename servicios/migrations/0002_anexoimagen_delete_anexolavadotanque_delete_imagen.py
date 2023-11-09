# Generated by Django 4.2.1 on 2023-11-08 22:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('servicios', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AnexoImagen',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('imagen', models.ImageField(upload_to='media/anexoImagenes/')),
                ('descripcion', models.TextField()),
                ('servicio_Lavado', models.ForeignKey(default=20, on_delete=django.db.models.deletion.CASCADE, to='servicios.serviciolavadotanque')),
            ],
        ),
        migrations.DeleteModel(
            name='AnexoLavadoTanque',
        ),
        migrations.DeleteModel(
            name='Imagen',
        ),
    ]
