from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User, Group, Permission

# Create your models here.


class TipoServicio(models.Model):
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nombre

    def get_absolute_url(self):
        return reverse('categoria_detalle', args=[str(self.id)])

class Cliente(models.Model):
    nit = models.IntegerField()
    razon_social = models.CharField(max_length=100)
    telefono = models.CharField(max_length=15)
    contacto = models.CharField(max_length=15)
    email = models.EmailField()
    direccion = models.CharField(max_length=200)

    def __str__(self):
        return self.nombre

class Servicio(models.Model):
    descripcion = models.TextField(blank=True, null=True)
    tipo_servicio = models.ForeignKey(
        tipoServicio, on_delete=models.SET_NULL, null=True)
    fecha_ejecuicion =models.DateField()
    fecha_vencimiento = models.DateField()
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.tipo_servicio

    def get_absolute_url(self):
        return reverse('servicio_detalle', args=[str(self.id)])

class User(AbstractUser):
    # campos adicionales para el modelo de Usuario
        # Cambiar el atributo related_name para evitar conflictos
    groups = models.ManyToManyField(Group, related_name='users_servicios')
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='users_servicios',
        blank=True,
    )

class AsignacionServicio(models.Model):
    servicio = models.ForeignKey(Servicio, on_delete=models.CASCADE)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha_asignacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.servicio} asignado a {self.usuario.username}"