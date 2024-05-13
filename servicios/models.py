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
    
    class Meta:        
        verbose_name_plural = "Tipo de Servicios"
    
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nombre

    def get_absolute_url(self):
        return reverse('TipoServicio_detalle', args=[str(self.id)])
    
class EstadoServicio(models.Model):
    class Meta:        
        verbose_name_plural = "Estado de los Servicios"
    nombre = models.CharField(max_length=200)
    
    def __str__(self):
        return self.nombre

    def get_absolute_url(self):
        return reverse('EstadoServicio_detalle', args=[str(self.id)])

class Cliente(models.Model):
    class Meta:        
        verbose_name_plural = "Lista de Clientes"
    ESTADO_CHOICES = (
        ('activo', 'Activo'),
        ('no_activo', 'No Activo'),
    )
    nit = models.IntegerField()
    razon_social = models.CharField(max_length=100)
    telefono = models.CharField(max_length=15)
    contacto = models.CharField(max_length=200)
    email = models.EmailField()
    direccion = models.CharField(max_length=200)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='usuario_creador')
    estado = models.CharField(max_length=10, choices=ESTADO_CHOICES, default='activo')
    
    def __str__(self):
        return self.razon_social
    
class UsuarioCliente(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='usuarios')

    def __str__(self):
        return self.user.username

class Servicio(models.Model):
    class Meta:        
        verbose_name_plural = "Lista de Servicios"
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    tipo_servicio = models.ForeignKey(TipoServicio, on_delete=models.SET_NULL, null=True)
    fecha_inicio = models.DateTimeField(null=True)
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
    class Meta:        
        verbose_name_plural = "Evidencias del Servicio"
    nombre = models.CharField(max_length=200)

    def __str__(self):
        return self.nombre

class Medida(models.Model):
    class Meta:        
        verbose_name_plural = "Tipos de Medida"
    nombre = models.CharField(max_length=200)

    def __str__(self):
        return self.nombre
class UnidadMedida(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre
    
class Producto(models.Model):
    class Meta:        
        verbose_name_plural = "Tipos de Producto"
    nombre = models.CharField(max_length=200)


    def __str__(self):
        return self.nombre



class LugaresATratar(models.Model):
    class Meta:        
        verbose_name_plural = "Lista de Lugares Tratados por Servicio"
    nombre = models.CharField(max_length=200)

    def __str__(self):
        return self.nombre

class TipoControlImplementado(models.Model):
    class Meta:        
        verbose_name_plural = "Tipo de Control Implementado"
    nombre = models.CharField(max_length=200)

    def __str__(self):
        return self.nombre
    
    
class ServicioFumigacion(models.Model):
    class Meta:        
        verbose_name_plural = "Listado de Servicio Fumigacion"
    servicio = models.OneToOneField(Servicio, on_delete=models.CASCADE, related_name='servicio_fumigacion')
    lugares_tratados = models.ManyToManyField(LugaresATratar, blank=True)
    tipo_control_implementado = models.ManyToManyField(TipoControlImplementado, blank=True)
    observaciones = models.TextField(max_length=500, null=True)
    

    def __str__(self):
        return f"Servicio de Fumigación: {self.servicio.id}"

    def get_absolute_url(self):
        return reverse('servicio_fumigacion_detalle', args=[str(self.servicio.id)])
    

class Precauciones(models.Model):
    class Meta:        
        verbose_name_plural = "Listado de Precauciones"
    descripcion = models.CharField(max_length=200)
    
    def __str__(self):
        return self.descripcion
    
class Recomendaciones(models.Model):
    class Meta:        
        verbose_name_plural = "Listado de Recomendaciones"
    descripcion = models.CharField(max_length=200)
    
    def __str__(self):
        return self.descripcion
    
class ServicioRecomendacion(models.Model):
    class Meta:        
        verbose_name_plural = "Recomenaciondes por Servicio"
    servicio_fumigacion = models.ForeignKey(ServicioFumigacion, on_delete=models.CASCADE)
    recomendacion = models.ForeignKey(Recomendaciones, on_delete=models.CASCADE)

    def __str__(self):
        return f"Servicio: {self.servicio_fumigacion}, Precauciones: {self.recomendacion}"


class ServicioPrecaucion(models.Model):
    class Meta:        
        verbose_name_plural = "Precauciones por Servicio"
    servicio_fumigacion = models.ForeignKey(ServicioFumigacion, on_delete=models.CASCADE)
    precaucion = models.ForeignKey(Precauciones, on_delete=models.CASCADE)

    def __str__(self):
        return f"Servicio: {self.servicio_fumigacion}, Precauciones: {self.precaucion}"

class UbicacionRev(models.Model):
    class Meta:        
        verbose_name_plural = "Ubicacion Rev"
    nombre = models.CharField(max_length=200)

    def __str__(self):
        return self.nombre

class EvidenciaMedida(models.Model):
    class Meta:        
        verbose_name_plural = "Evidencia"
    servicio_fumigacion = models.ForeignKey(ServicioFumigacion, on_delete=models.CASCADE, related_name='evidencias_medidas')
    evidencia = models.ForeignKey(Evidencia, on_delete=models.CASCADE)
    medida = models.ForeignKey(Medida, on_delete=models.CASCADE)
    ubicacion = models.ForeignKey(UbicacionRev, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.evidencia} - {self.medida}- {self.ubicacion}"
    
class CategoriaToxicologica(models.Model):
    class Meta:        
        verbose_name_plural = "Listado de Categorias Toxicologicas"
    nombre = models.CharField(max_length=200)
    
    def __str__(self):
        return self.nombre
    
class ProductoUtilizado(models.Model):
    class Meta:        
        verbose_name_plural = "Productos Utilizados por Servicio"
    servicio_fumigacion = models.ForeignKey(ServicioFumigacion, on_delete=models.CASCADE, related_name='productos_utilizados')
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.DecimalField(max_digits=10, decimal_places=2)
    unidad_medida = models.ForeignKey(UnidadMedida, on_delete=models.CASCADE)
    categoria_toxixologica = models.ForeignKey(CategoriaToxicologica, on_delete=models.CASCADE, default=None)

    def __str__(self):
        return f"{self.producto} - {self.cantidad} {self.unidad_medida}"

class UbicacionTanque(models.Model):
    class Meta:        
        verbose_name_plural = "Listado de Ubicaciones del Tanque"
    nombre = models.CharField(max_length=200)

    def __str__(self):
        return self.nombre
    
class MaterialTanque(models.Model):
    class Meta:        
        verbose_name_plural = "Listado de Materiales del Tanque"
    nombre = models.CharField(max_length=200)

    def __str__(self):
        return self.nombre
    
class UnidadMedidaTanque(models.Model):
    class Meta:        
        verbose_name_plural = "Listado de las Medidas de Tanque"
    nombre = models.CharField(max_length=200)

    def __str__(self):
        return self.nombre
    
class EstadoInternoTanque(models.Model):
    class Meta:        
        verbose_name_plural = "Listado del Estado Interno del Tanque"
    nombre = models.CharField(max_length=200)

    def __str__(self):
        return self.nombre
    
class RevestimientoTanque(models.Model):
    class Meta:        
        verbose_name_plural = "Listado del Revestimiento del Tanque"
    nombre = models.CharField(max_length=200)

    def __str__(self):
        return self.nombre
    
class EstadoTuberias(models.Model):
    class Meta:        
        verbose_name_plural = "Listado de Estados de las Tuberias"
    nombre = models.CharField(max_length=200)

    def __str__(self):
        return self.nombre
    
class EstadoEmpaques(models.Model):
    class Meta:        
        verbose_name_plural = "Listado de Estado de los Empaques"
    nombre = models.CharField(max_length=200)

    def __str__(self):
        return self.nombre
    
class HermeticidadTanque(models.Model):
    class Meta:        
        verbose_name_plural = "Listado de la Hermeticidad del Tanque"
    nombre = models.CharField(max_length=200)

    def __str__(self):
        return self.nombre



class ServicioLavadoTanque(models.Model):
    class Meta:        
        verbose_name_plural = "Servicios de Lavado de Tanque"
    servicio = models.OneToOneField(Servicio, on_delete=models.CASCADE, related_name='servicio_lavado_tanque')
    def __str__(self):
        return f"Servicio de Lavado Tanque: {self.servicio.id}"
    
class Tanque(models.Model):
    class Meta:        
        verbose_name_plural = "Tanque"
    servicio_lavado = models.ForeignKey(ServicioLavadoTanque, on_delete=models.CASCADE)
    ubicacion_tanque = models.ForeignKey(UbicacionTanque, on_delete=models.CASCADE, null=True, blank=True)
    material_tanque = models.ForeignKey(MaterialTanque, on_delete=models.CASCADE, null=True, blank=True)
    unidad_medida = models.ForeignKey(UnidadMedidaTanque, on_delete=models.CASCADE, null=True)
    revestimiento_tanque = models.ForeignKey(RevestimientoTanque, on_delete=models.CASCADE, null=True)
    estado_interno_tanque = models.ForeignKey(EstadoInternoTanque, on_delete=models.CASCADE, null=True)
    volumen_almacenamiento = models.FloatField()
    estado_tuberias = models.ForeignKey(EstadoTuberias, on_delete=models.CASCADE)
    estado_empaque = models.ForeignKey(EstadoEmpaques, on_delete=models.CASCADE, null=True)
    hermeticidad_tanque = models.ForeignKey(HermeticidadTanque, on_delete=models.CASCADE)
    observaciones = models.TextField(max_length=500, null=True, blank=True)
    
    # Campos otros
    otra_ubicacion_tanque = models.CharField(max_length=50, null=True, blank=True)
    otro_material_tanque = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return f"Tanque ID: {self.id}"
    
class AnexoImagen(models.Model):
    class Meta:        
        verbose_name_plural = "Anexos por Servicio Lavado"
    servicio_lavado = models.ForeignKey(ServicioLavadoTanque, on_delete=models.CASCADE, default=20)
    imagen = models.ImageField(upload_to='media/anexoImagenes/')
    descripcion = models.TextField()

    def __str__(self):
        return self.descripcion

class Tecnico(models.Model):
    class Meta:        
        verbose_name_plural = "Listado de Tecnicos"
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Otros campos relevantes para los técnicos, como nombre, apellidos, etc.

    def __str__(self):
        return self.user.username
    
class AsignacionServicio(models.Model):
    class Meta:        
        verbose_name_plural = "Servicios Asignados"
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
        
        
class infoEmpresa(models.Model):
    class Meta:        
        verbose_name_plural = "Informacion de la Empresa"
    nit = models.CharField(max_length=150)
    direccion = models.CharField(max_length=150)
    telefono = models.CharField(max_length=150)
    celular = models.CharField(max_length=150)
    no_radicado = models.CharField(max_length=150)
    fecha_radicado = models.CharField(max_length=510)
    TRD_radicado = models.CharField(max_length=150)
    concepto_radicado = models.CharField(max_length=200)
    agradecimiento = models.CharField(max_length=200)
    compromiso = models.CharField(max_length=200)
    correo = models.CharField(max_length=150)
    pagina_web = models.CharField(max_length=150)
    procedimiento_basico = models.CharField(max_length=1000)
    
class firmas_servicio_Lavado(models.Model):
    class Meta:        
        verbose_name_plural = "Firmas de Servicio Lavado"
    servicio_Lavado = models.ForeignKey(ServicioLavadoTanque, on_delete=models.CASCADE, default=20, unique=True)
    imagen = models.ImageField(upload_to='media/firmas_lavado/')
   
class firmas_servicio_fumigacion(models.Model):
    class Meta:        
        verbose_name_plural = "Firmas de Servicio Fumigacion"
    servicio_fumigacion = models.ForeignKey(ServicioFumigacion, on_delete=models.CASCADE, default=20, unique=True)
    imagen = models.ImageField(upload_to='media/firmas_fumigacion/')
    