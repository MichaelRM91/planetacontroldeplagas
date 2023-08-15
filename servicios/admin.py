from django.contrib import admin
from servicios.forms import AsignacionServicioForm, ServicioFumigacionForm

from .models import AsignacionServicio, Cliente, EstadoServicio, Evidencia, EvidenciaMedida, Medida, Producto, Servicio, ServicioFumigacion, ServicioLavadoTanque, Tecnico, TipoServicio, ProductoUtilizado, UnidadMedida, LugaresATratar,TipoControlImplementado

# Register your models here.
admin.site.register(TipoServicio)
admin.site.register(Cliente)
admin.site.register(Evidencia)
admin.site.register(Medida)
admin.site.register(Producto)
admin.site.register(UnidadMedida)
admin.site.register(LugaresATratar)
admin.site.register(TipoControlImplementado)
admin.site.register(ServicioLavadoTanque)
admin.site.register(Servicio)
admin.site.register(EstadoServicio)
admin.site.register(Tecnico)
admin.site.register(ProductoUtilizado)
admin.site.register(EvidenciaMedida)





""" 

class EvidenciaMedidaInline(admin.TabularInline):
    model = EvidenciaMedida
    extra = 1
class ProductoUtilizadoInline(admin.TabularInline):
    model = ProductoUtilizado
    extra = 1 """
class ServicioFumigacionAdmin(admin.ModelAdmin):
    form = ServicioFumigacionForm
    filter_horizontal = ('lugares_tratados','tipo_control_implementado')

admin.site.register(ServicioFumigacion, ServicioFumigacionAdmin)

class AsignacionServicioAdmin(admin.ModelAdmin):
    form = AsignacionServicioForm

admin.site.register(AsignacionServicio, AsignacionServicioAdmin)





