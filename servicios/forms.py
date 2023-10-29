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
    usuario = forms.ModelChoiceField(
        label="Usuario", queryset=User.objects.all(), empty_label=None
    )
    fecha_ejecucion = forms.DateField(widget=forms.DateInput(attrs={"type": "date"}))
    fecha_vencimiento = forms.DateField(widget=forms.DateInput(attrs={"type": "date"}))


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
        model = Precauciones
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


class ServicioFumigacionForm(forms.ModelForm):
    class Meta:
        model = ServicioFumigacion
        fields = ["lugares_tratados", "tipo_control_implementado"]
        widgets = {
            'lugares_tratados': forms.CheckboxSelectMultiple(),
            'tipo_control_implementado': forms.CheckboxSelectMultiple(),
           # 'servicio': forms.HiddenInput()  # Campo oculto para el servicio
        }
        



class ServicioLavadoTanqueForm(forms.ModelForm):
  
    class Meta:
        model = ServicioLavadoTanque
        fields = '__all__'
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
