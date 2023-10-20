from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType

# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser

class TipoServicio(models.Model):
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nombre

    def get_absolute_url(self):
        return reverse('TipoServicio_detalle', args=[str(self.id)])
    
class EstadoServicio(models.Model):
    nombre = models.CharField(max_length=200)
    
    def __str__(self):
        return self.nombre

    def get_absolute_url(self):
        return reverse('EstadoServicio_detalle', args=[str(self.id)])

class Cliente(models.Model):
    nit = models.IntegerField()
    razon_social = models.CharField(max_length=100)
    telefono = models.CharField(max_length=15)
    contacto = models.CharField(max_length=15)
    email = models.EmailField()
    direccion = models.CharField(max_length=200)

    def __str__(self):
        return self.razon_social

class Servicio(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    tipo_servicio = models.ForeignKey(
        TipoServicio, on_delete=models.SET_NULL, null=True)
    fecha_ejecucion = models.DateField()
    fecha_vencimiento = models.DateField()
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    # Define el valor predeterminado utilizando la instancia de EstadoServicio
    estado_servicio = models.ForeignKey(EstadoServicio, on_delete=models.SET_NULL, null=True, default=EstadoServicio.objects.get(nombre="registrado"))
    
    def __str__(self):
        return f"Cliente: {self.cliente}, Tipo de servicio: {self.tipo_servicio}, Fecha de ejecución: {self.fecha_ejecucion}"

    def get_absolute_url(self):
        return reverse('servicio_detalle', args=[str(self.id)])

class Evidencia(models.Model):
    nombre = models.CharField(max_length=200)

    def __str__(self):
        return self.nombre

class Medida(models.Model):
    nombre = models.CharField(max_length=200)

    def __str__(self):
        return self.nombre
class UnidadMedida(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre
    
class Producto(models.Model):
    nombre = models.CharField(max_length=200)


    def __str__(self):
        return self.nombre



class LugaresATratar(models.Model):
    nombre = models.CharField(max_length=200)

    def __str__(self):
        return self.nombre

class TipoControlImplementado(models.Model):
    nombre = models.CharField(max_length=200)

    def __str__(self):
        return self.nombre


    
class ServicioFumigacion(models.Model):
    servicio = models.OneToOneField(Servicio, on_delete=models.CASCADE, related_name='servicio_fumigacion')
    lugares_tratados = models.ManyToManyField(LugaresATratar, blank=True)
    tipo_control_implementado = models.ManyToManyField(TipoControlImplementado, blank=True)

    def __str__(self):
        return f"Servicio de Fumigación: {self.servicio.id}"

    def get_absolute_url(self):
        return reverse('servicio_fumigacion_detalle', args=[str(self.servicio.id)])

class UbicacionRev(models.Model):
    nombre = models.CharField(max_length=200)

    def __str__(self):
        return self.nombre

class EvidenciaMedida(models.Model):
    servicio_fumigacion = models.ForeignKey(ServicioFumigacion, on_delete=models.CASCADE, related_name='evidencias_medidas')
    evidencia = models.ForeignKey(Evidencia, on_delete=models.CASCADE)
    medida = models.ForeignKey(Medida, on_delete=models.CASCADE)
    ubicacion = models.ForeignKey(UbicacionRev, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.evidencia} - {self.medida}- {self.ubicacion}"
    
class CategoriaToxicologica(models.Model):
    nombre = models.CharField(max_length=200)
    
    def __str__(self):
        return self.nombre
    
class ProductoUtilizado(models.Model):
    servicio_fumigacion = models.ForeignKey(ServicioFumigacion, on_delete=models.CASCADE, related_name='productos_utilizados')
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.DecimalField(max_digits=10, decimal_places=2)
    unidad_medida = models.ForeignKey(UnidadMedida, on_delete=models.CASCADE)
    categoria_toxixologica = models.ForeignKey(CategoriaToxicologica, on_delete=models.CASCADE, default=None)

    def __str__(self):
        return f"{self.producto} - {self.cantidad} {self.unidad_medida}"

class UbicacionTanque(models.Model):
    nombre = models.CharField(max_length=200)

    def __str__(self):
        return self.nombre
    
class MaterialTanque(models.Model):
    nombre = models.CharField(max_length=200)

    def __str__(self):
        return self.nombre
    
    

class UnidadMedidaTanque(models.Model):
    nombre = models.CharField(max_length=200)

    def __str__(self):
        return self.nombre
    
class EstadoInternoTanque(models.Model):
    nombre = models.CharField(max_length=200)

    def __str__(self):
        return self.nombre
class ServicioLavadoTanque(models.Model):
    UBICACION_TANQUE_CHOICES = (
        ('opcion1', 'Opción 1'),
        ('opcion2', 'Opción 2'),
        ('otro', 'Otro'),
    )

    MATERIAL_TANQUE_CHOICES = (
        ('opcion1', 'Opción 1'),
        ('opcion2', 'Opción 2'),
        ('otro', 'Otro'),
    )

    UBICACION_REV_CHOICES = (
        ('opcion1', 'Opción 1'),
        ('opcion2', 'Opción 2'),
        ('otro', 'Otro'),
    )

    UNIDAD_MEDIDA_CHOICES = (
        ('mt3', 'm³'),
        ('lt', 'L'),
    )

    ESTADO_INTERNO_CHOICES = (
        ('opcion1', 'Opción 1'),
        ('opcion2', 'Opción 2'),
    )

    FOTOS_CHOICES = (
        ('opcion1', 'Opción 1'),
        ('opcion2', 'Opción 2'),
    )

    # Campos adicionales
    servicio = models.OneToOneField(Servicio, on_delete=models.CASCADE, related_name='servicio_lavado_tanque')
    ubicacion_tanque = models.CharField(max_length=20, choices=UBICACION_TANQUE_CHOICES)
    otro_ubicacion_tanque = models.CharField(max_length=100, blank=True)
    material_tanque = models.CharField(max_length=20, choices=MATERIAL_TANQUE_CHOICES)
    otro_material_tanque = models.CharField(max_length=100, blank=True)
    revestimiento_tanque = models.CharField(max_length=100)
    volumen_almacenamiento = models.FloatField()
    unidad_medida = models.CharField(max_length=3, choices=UNIDAD_MEDIDA_CHOICES)
    estado_interno_tanque = models.CharField(max_length=20, choices=ESTADO_INTERNO_CHOICES)
    fotos_estado_interno = models.ImageField(upload_to='fotos_estado_interno')
    hermeticidad_tanque = models.CharField(max_length=20, choices=FOTOS_CHOICES)
    fotos_hermeticidad = models.ImageField(upload_to='fotos_hermeticidad')
    estado_empaques = models.CharField(max_length=20, choices=FOTOS_CHOICES)
    fotos_estado_empaques = models.ImageField(upload_to='fotos_estado_empaques')
    estado_tuberias = models.CharField(max_length=20, choices=FOTOS_CHOICES)
    fotos_estado_tuberias = models.ImageField(upload_to='fotos_estado_tuberias')
    observaciones_antes = models.ImageField(upload_to='observaciones_antes')
    observaciones_despues = models.ImageField(upload_to='observaciones_despues')

    def save(self, *args, **kwargs):
        if self.ubicacion_tanque != 'otro':
            self.otro_ubicacion_tanque = ''
        if self.material_tanque != 'otro':
            self.otro_material_tanque = ''
        super().save(*args, **kwargs)

class Tecnico(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Otros campos relevantes para los técnicos, como nombre, apellidos, etc.

    def __str__(self):
        return self.user.username
    
class AsignacionServicio(models.Model):
    servicio = models.ForeignKey(Servicio, on_delete=models.CASCADE)
    tecnico = models.ForeignKey(Tecnico, on_delete=models.CASCADE)
    fecha_asignacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.servicio} asignado a {self.tecnico}"

    def save(self, *args, **kwargs):
        # Obtener el servicio asignado
        servicio = self.servicio
        # Cambiar el estado del servicio
        servicio.estado_servicio = EstadoServicio.objects.get(nombre='Asignado')
        # Guardar el servicio
        servicio.save()
        super().save(*args, **kwargs)


    def get_absolute_url(self):
        return reverse('asignacion_detalle', args=[str(self.id)])
    
    def save(self, *args, **kwargs):
        # Obtener el servicio asignado
        servicio = self.servicio
        # Cambiar el estado del servicio
        servicio.estado_servicio = EstadoServicio.objects.get(nombre='Asignado')
        # Guardar el servicio
        servicio.save()
        super().save(*args, **kwargs)