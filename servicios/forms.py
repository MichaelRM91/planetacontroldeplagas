from django import forms
from django.contrib.auth.models import Group, Permission, User
from django.forms import (
    BaseModelFormSet,
    HiddenInput,
    formset_factory,
    inlineformset_factory,
)
from django.utils import timezone

from .models import *


class ServicioForm(forms.ModelForm):
    class Meta:
        model = Servicio
        fields = [
            "cliente",
            "tipo_servicio",
            "fecha_ejecucion",
            "fecha_vencimiento",
        ]

    cliente = forms.ModelChoiceField(
        label="Cliente", queryset=Cliente.objects.all(), empty_label=None
    )
    tipo_servicio = forms.ModelChoiceField(
        label="Tipo de Servicio", queryset=TipoServicio.objects.all(), empty_label=None
    )
    fecha_ejecucion = forms.DateField(label="Fecha de Ejecución")
    fecha_vencimiento = forms.DateField(label="Fecha de Vencimiento")
    fecha_ejecucion = forms.DateField(widget=forms.DateInput(attrs={"type": "date"}))
    fecha_vencimiento = forms.DateField(widget=forms.DateInput(attrs={"type": "date"}))

    def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            # Establecemos el límite de fecha mínima para evitar seleccionar días pasados
            self.fields['fecha_ejecucion'].widget.attrs['min'] = timezone.now().strftime('%Y-%m-%d')
            self.fields['fecha_vencimiento'].widget.attrs['min'] = timezone.now().strftime('%Y-%m-%d')
class EvidenciaMedidaForm(forms.ModelForm):
    class Meta:
        model = EvidenciaMedida
        fields = '__all__'


class ProductoUtilizadoForm(forms.ModelForm):
    class Meta:
        model = ProductoUtilizado
        fields = '__all__'
        
class RecomendacionesForm(forms.ModelForm):
    class Meta:
        model = ServicioRecomendacion
        fields = '__all__'
        
class PrecaucionesForm(forms.ModelForm):
    class Meta:
        model = ServicioPrecaucion
        fields = '__all__'

class AnexosForm(forms.ModelForm):
    class Meta:
        model = AnexoImagen
        fields = '__all__'
        
class TanquesForm(forms.ModelForm):
    class Meta:
        model = Tanque
        fields = '__all__'
        
    
ServicioFumigacionRecomendacionesFormSet = inlineformset_factory(
    ServicioFumigacion,
    ServicioRecomendacion, 
    form=RecomendacionesForm,
    extra=1
    )

ServicioFumigacionPrecaucionesFormSet = inlineformset_factory(
    ServicioFumigacion, 
    ServicioPrecaucion, 
    form=PrecaucionesForm, 
    extra=1
    )


ServicioFumigacionEvidenciaMedidaFormSet = inlineformset_factory(
    ServicioFumigacion,
    EvidenciaMedida,
    form=EvidenciaMedidaForm,
    extra=1, can_delete=True, can_delete_extra=True  # Cantidad de formularios vacíos adicionales que se mostrarán
)

ServicioFumigacionProductoUtilizadoFormSet = inlineformset_factory(
    ServicioFumigacion,
    ProductoUtilizado,
    form=ProductoUtilizadoForm,
    extra=1, can_delete=True, can_delete_extra=True
)

ServicioLavadoTanqueAnexosFormset = inlineformset_factory(
    ServicioLavadoTanque,
    AnexoImagen,
    form=AnexosForm,
    extra=1, can_delete=True, can_delete_extra=True
)

ServicioLavadoTanqueFormset = inlineformset_factory(
    ServicioLavadoTanque,
    Tanque,
    form=TanquesForm,
    extra=1, can_delete=True, can_delete_extra=True
)


class ServicioFumigacionForm(forms.ModelForm):
    class Meta:
        model = ServicioFumigacion
        fields = ["lugares_tratados", "tipo_control_implementado", "observaciones"]
        widgets = {
            'lugares_tratados': forms.CheckboxSelectMultiple(),
            'tipo_control_implementado': forms.CheckboxSelectMultiple(),
           # 'servicio': forms.HiddenInput()  # Campo oculto para el servicio
        }
        



class ServicioLavadoTanqueForm(forms.ModelForm):
  
    class Meta:
        model = ServicioLavadoTanque
        fields = []
        widgets = {
            'servicio': forms.HiddenInput()  # Campo oculto para el servicio
        }


class AsignacionServicioForm(forms.ModelForm):
    class Meta:
        model = AsignacionServicio
        fields = ["servicio", "tecnico"]

    servicio = forms.ModelChoiceField(
        label="servicio",
        queryset=Servicio.objects.exclude(
            estado_servicio__nombre__in=["Asignado", "Finalizado"]
        ),
        empty_label=None,
    )

class ClienteForm(forms.ModelForm):
    user = forms.ModelChoiceField(
        label='Usuario para el Cliente',
        queryset=User.objects.filter(
            clientes_asociados__isnull=True,  # Filtra usuarios no asociados a un cliente
            tecnico__isnull=True,  # Filtra usuarios no asociados a un técnico
            is_superuser=False
        )
    )

    class Meta:
        model = Cliente
        fields = ['nit', 'razon_social', 'telefono', 'contacto', 'email', 'direccion', 'user']

class FirmaLavadoForm(forms.ModelForm):
    class Meta:
        model = firmas_servicio_Lavado
        fields = ['imagen']

class FirmaFumigacionForm(forms.ModelForm):
    class Meta:
        model = firmas_servicio_fumigacion
        fields = ['imagen']