from django import forms
from django.contrib.auth.models import Group, Permission, User
from django.forms import (
    BaseModelFormSet,
    HiddenInput,
    formset_factory,
    inlineformset_factory,
)
from django.utils import timezone

from .models import (
    AsignacionServicio,
    Cliente,
    Evidencia,
    EvidenciaMedida,
    LugaresATratar,
    ProductoUtilizado,
    Servicio,
    ServicioFumigacion,
    ServicioLavadoTanque,
    Tecnico,
    TipoControlImplementado,
    TipoServicio,
)


class ServicioForm(forms.ModelForm):
    class Meta:
        model = Servicio
        fields = [
            "cliente",
            "tipo_servicio",
            "fecha_ejecucion",
            "fecha_vencimiento",
            "estado_servicio",
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
        fields = ["evidencia", "medida"]


class ProductoUtilizadoForm(forms.ModelForm):
    class Meta:
        model = ProductoUtilizado
        fields = ["producto", "cantidad", "unidad_medida"]


ServicioFumigacionEvidenciaMedidaFormSet = inlineformset_factory(
    ServicioFumigacion,
    EvidenciaMedida,
    form=EvidenciaMedidaForm,
    extra=1,  # Cantidad de formularios vacíos adicionales que se mostrarán
)

ServicioFumigacionProductoUtilizadoFormSet = inlineformset_factory(
    ServicioFumigacion,
    ProductoUtilizado,
    form=ProductoUtilizadoForm,
    extra=1,
)


class ServicioFumigacionForm(forms.ModelForm):
       class Meta:
        model = ServicioFumigacion
        fields = ["servicio","lugares_tratados", "tipo_control_implementado"]
        widgets = {
            'lugares_tratados': forms.CheckboxSelectMultiple(),
            'tipo_control_implementado': forms.CheckboxSelectMultiple(),
            'servicio': forms.HiddenInput()  # Campo oculto para el servicio
        }


class ServicioLavadoTanqueForm(forms.ModelForm):
  
    class Meta:
        model = ServicioLavadoTanque
        fields = [
            "ubicacion_tanque",
            "otro_ubicacion_tanque",
            "material_tanque",
            "otro_material_tanque",
            "revestimiento_tanque",
            "volumen_almacenamiento",
            "unidad_medida",
            "estado_interno_tanque",
            "fotos_estado_interno",
            "hermeticidad_tanque",
            "fotos_hermeticidad",
            "estado_empaques",
            "fotos_estado_empaques",
            "estado_tuberias",
            "fotos_estado_tuberias",
            "observaciones_antes",
            "observaciones_despues",
        ]
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
