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
    user = models.ForeignKey(User, on_delete=models.CASCADE)

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
    estado_servicio = models.ForeignKey(EstadoServicio, on_delete=models.SET_NULL, null=True, default=3)
    
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
    observaciones = models.TextField(max_length=500, null=True)
    

    def __str__(self):
        return f"Servicio de Fumigación: {self.servicio.id}"

    def get_absolute_url(self):
        return reverse('servicio_fumigacion_detalle', args=[str(self.servicio.id)])
    

class Precauciones(models.Model):
    descripcion = models.CharField(max_length=200)
    
    def __str__(self):
        return self.descripcion
    
class Recomendaciones(models.Model):
    descripcion = models.CharField(max_length=200)
    
    def __str__(self):
        return self.descripcion
    
class ServicioRecomendacion(models.Model):
    servicio_fumigacion = models.ForeignKey(ServicioFumigacion, on_delete=models.CASCADE)
    recomendacion = models.ForeignKey(Recomendaciones, on_delete=models.CASCADE)

    def __str__(self):
        return f"Servicio: {self.servicio_fumigacion}, Precauciones: {self.recomendacion}"


class ServicioPrecaucion(models.Model):
    servicio_fumigacion = models.ForeignKey(ServicioFumigacion, on_delete=models.CASCADE)
    precaucion = models.ForeignKey(Precauciones, on_delete=models.CASCADE)

    def __str__(self):
        return f"Servicio: {self.servicio_fumigacion}, Precauciones: {self.precaucion}"

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
    
class RevestimientoTanque(models.Model):
    nombre = models.CharField(max_length=200)

    def __str__(self):
        return self.nombre
    
class EstadoTuberias(models.Model):
    nombre = models.CharField(max_length=200)

    def __str__(self):
        return self.nombre
    
class EstadoEmpaques(models.Model):
    nombre = models.CharField(max_length=200)

    def __str__(self):
        return self.nombre
    
class HermeticidadTanque(models.Model):
    nombre = models.CharField(max_length=200)

    def __str__(self):
        return self.nombre

class Imagen(models.Model):
    imagen = models.ImageField(upload_to='media/anexoImagenes/')
    descripcion = models.TextField()

    def __str__(self):
        return self.descripcion

class AnexoLavadoTanque(models.Model):
    titulo = models.CharField(max_length=100)
    imagenes = models.ManyToManyField(Imagen)
    # Otros campos que puedas necesitar en tu modelo de Anexos

    def __str__(self):
        return self.titulo
class ServicioLavadoTanque(models.Model):
    servicio = models.OneToOneField(Servicio, on_delete=models.CASCADE, related_name='servicio_lavado_tanque')
    ubicacion_tanque = models.ForeignKey(UbicacionTanque, on_delete=models.CASCADE, null=True)
    material_tanque = models.ForeignKey(MaterialTanque, on_delete=models.CASCADE, null=True)
    unidad_medida = models.ForeignKey(UnidadMedidaTanque, on_delete=models.CASCADE, null=True)
    revestimiento_tanque = models.ForeignKey(RevestimientoTanque, on_delete=models.CASCADE, null=True)
    estado_interno_tanque = models.ForeignKey(EstadoInternoTanque, on_delete=models.CASCADE, null=True)
    volumen_almacenamiento = models.FloatField()
    estado_tuberias = models.ForeignKey(EstadoTuberias, on_delete=models.CASCADE)
    estado_empaque = models.ForeignKey(EstadoEmpaques, on_delete=models.CASCADE, null=True)
    hermeticidad_tanque = models.ForeignKey(HermeticidadTanque, on_delete=models.CASCADE)
    observaciones = models.TextField(max_length=500, null=True)
    anexo = models.ForeignKey(AnexoLavadoTanque, on_delete=models.CASCADE, null=True)
    
    #campos otros
    otra_ubicacion_tanque = models.CharField(max_length=50, null=True, blank=True)
    otro_material_tanque = models.CharField(max_length=50, null=True, blank=True)
    
    def __str__(self):
        return f"Servicio de Lavado Tanque: {self.servicio.id}"

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