from django import forms
from django.utils import timezone
from .models import AsignacionServicio, Categoria, Cliente, Servicio
from django.contrib.auth.models import User, Group, Permission

class ServicioForm(forms.ModelForm):
    class Meta:
        model = Servicio
        fields = ('nombre', 'descripcion', 'categoria', 'precio', 'duracion','cliente', 'usuario')

    nombre = forms.CharField(
        label='Nombre del servicio',
        widget=forms.TextInput(attrs={'placeholder': 'Ej. Fumigación de cucarachas'})
    )
    descripcion = forms.CharField(
        label='Descripción del servicio',
        required=False,
        widget=forms.Textarea(attrs={'placeholder': 'Ej. Servicio de fumigación para eliminar cucarachas'})
    )
    categoria = forms.ModelChoiceField(
        label='Categoría',
        queryset=Categoria.objects.all(),
        empty_label=None
    )
    precio = forms.DecimalField(
        label='Precio',
        max_digits=6,
        decimal_places=2,
        min_value=0
    )
    duracion = forms.DurationField(
        label='Duración (HH:MM:SS)',
        widget=forms.TextInput(attrs={'placeholder': 'Ej. 01:30:00'}),
        initial=timezone.timedelta(hours=1)
    )
    cliente = forms.ModelChoiceField(
        label='Cliente',
        queryset=Cliente.objects.all(),
        empty_label=None
    )
    usuario = forms.ModelChoiceField(
        label='Usuario',
        queryset=User.objects.all(),
        empty_label=None
    )

class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ('nombre',)