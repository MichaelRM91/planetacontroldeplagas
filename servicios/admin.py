from django.contrib import admin
from servicios.forms import *
from django import forms

from .models import *

class infoEmpresaAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.CharField: {'widget': forms.TextInput(attrs={'style': 'width: 40em;'})},
    }
    
class ClienteAdmin(admin.ModelAdmin):
    list_display = ['nit', 'razon_social', 'telefono', 'contacto', 'email', 'direccion', 'estado']
    search_fields = ['nit', 'razon_social', 'telefono', 'contacto', 'email', 'direccion', 'estado']
    formfield_overrides = {
        models.CharField: {'widget': forms.TextInput(attrs={'style': 'width: 40em;'})},
        models.IntegerField: {'widget': forms.TextInput(attrs={'style': 'width: 40em;'})},
        models.ForeignKey: {'widget': forms.Select(attrs={'style': 'width: 40em;'})},
    }

# Register your models here.
admin.site.register(TipoServicio)
admin.site.register(Cliente, ClienteAdmin)
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
admin.site.register(UbicacionRev)
admin.site.register(CategoriaToxicologica)
admin.site.register(Precauciones)
admin.site.register(Recomendaciones)
admin.site.register(ServicioRecomendacion)
admin.site.register(ServicioPrecaucion)
admin.site.register(RevestimientoTanque)
admin.site.register(EstadoTuberias)
admin.site.register(EstadoEmpaques)
admin.site.register(HermeticidadTanque)
admin.site.register(AnexoImagen)
admin.site.register(UbicacionTanque)
admin.site.register(MaterialTanque)
admin.site.register(UnidadMedidaTanque)
admin.site.register(EstadoInternoTanque)
admin.site.register(infoEmpresa, infoEmpresaAdmin)
admin.site.register(firmas_servicio_fumigacion)
admin.site.register(firmas_servicio_Lavado)
admin.site.register(Tanque)

class ServicioFumigacionAdmin(admin.ModelAdmin):
    form = ServicioFumigacionForm
    filter_horizontal = ('lugares_tratados','tipo_control_implementado')

admin.site.register(ServicioFumigacion, ServicioFumigacionAdmin)

class AsignacionServicioAdmin(admin.ModelAdmin):
    form = AsignacionServicioForm

admin.site.register(AsignacionServicio, AsignacionServicioAdmin)

class UsuarioClienteForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Filtrar los usuarios que no están asociados a ningún cliente
        usuarios_cliente = list(UsuarioCliente.objects.all().values_list('user_id', flat=True))
        usuarios_tecnico = list(Tecnico.objects.all().values_list('user_id', flat=True))
        usuarios_superusuario = list(User.objects.filter(is_superuser=True).values_list('id', flat=True))  
        
        usuarios_asociados = usuarios_cliente + usuarios_tecnico + usuarios_superusuario
        
        self.fields['user'].queryset = User.objects.exclude(id__in=usuarios_asociados)

class UsuarioClienteAdmin(admin.ModelAdmin):
    form = UsuarioClienteForm

admin.site.register(UsuarioCliente, UsuarioClienteAdmin)