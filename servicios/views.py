from django.contrib import messages
from django.forms import formset_factory
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from .models import AsignacionServicio, EstadoServicio, ServicioFumigacion, ServicioLavadoTanque, TipoServicio, Servicio
from .forms import AsignacionServicioForm, ServicioForm, ServicioFumigacionForm, ServicioLavadoTanqueForm
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Servicio, ServicioFumigacion, ServicioLavadoTanque
from .forms import EvidenciaMedidaForm, ProductoUtilizadoForm

# Create your views here.

def servicios_list(request):
    servicios = Servicio.objects.all()
    return render(request, 'servicios/servicios_list.html', {'servicios': servicios})

def servicio_nuevo(request):
    if request.method == 'POST':
        form = ServicioForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'El servicio se ha creado exitosamente.')
            return redirect('servicios_list')
        else:
            messages.error(request, 'Ha ocurrido un error al crear el servicio. Por favor, revise los campos e inténtelo nuevamente.')
    else:
        form = ServicioForm()
    return render(request, 'servicios/servicio_form.html', {'form': form})

def servicio_edit(request, pk):
    servicio = Servicio.objects.get(pk=pk)
    if request.method == 'POST':
        form = ServicioForm(request.POST, instance=servicio)
        if form.is_valid():
            servicio = form.save()
            return redirect('servicios_list')
    else:
        form = ServicioForm(instance=servicio)
    return render(request, 'servicios/servicio_form.html', {'form': form, 'servicio': servicio})


# servicios/views.py

def crear_servicio_fumigacion(request):
    if request.method == 'POST':
        form = ServicioFumigacionForm(request.POST)
        if form.is_valid():
            servicio = form.save()
            # Realizar acciones adicionales o redireccionar
    else:
        form = ServicioFumigacionForm()

    context = {'form': form}
    return render(request, 'servicios/crear_servicio_fumigacion.html', context)

def crear_servicio_lavado_tanque(request):
    if request.method == 'POST':
        form = ServicioFumigacionForm(request.POST)
        if form.is_valid():
            servicio = form.save()
            # Realizar acciones adicionales o redireccionar
    else:
        form = ServicioFumigacionForm()

    context = {'form': form}
    return render(request, 'servicios/crear_servicio_fumigacion.html', context)

@login_required  # Agrega el decorador para asegurarte de que el usuario esté autenticado
def crear_servicio(request):
    if request.method == 'POST':
        form = ServicioForm(request.POST)
        if form.is_valid():
            servicio = form.save(commit=False)  # Crea una instancia del servicio sin guardarla en la base de datos todavía
            servicio.usuario = request.user  # Asigna el usuario actual al servicio
            servicio.save()  # Ahora guarda el servicio con el usuario asignado
            return redirect('lista_servicios')  # Redirige a la lista de servicios después de crear uno nuevo
    else:
        form = ServicioForm()

    return render(request, 'servicios/crear_servicio.html', {'form': form})

def asignar_servicio(request):
    if request.method == 'POST':
        form = AsignacionServicioForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_servicios')  # Redirige a la lista de servicios después de asignar uno nuevo
    else:
        form = AsignacionServicioForm()

    return render(request, 'servicios/asignar_servicio.html', {'form': form})

def ver_servicios_tecnico(request):
    tecnico = request.user.tecnico
    servicios_asignados = AsignacionServicio.objects.filter(tecnico=tecnico)

    if request.method == 'POST':
        # Procesar el formulario de marcado como completado
        servicio_id = request.POST.get('servicio_id')
        if servicio_id:
            servicio = Servicio.objects.get(pk=servicio_id)
            servicio.estado_servicio = EstadoServicio.objects.get(nombre='Completado')
            servicio.save()
            return redirect('ver_servicios_tecnico')

    return render(request, 'servicios/ver_servicios_tecnico.html', {'servicios_asignados': servicios_asignados})

def lista_servicios(request):
    servicios = Servicio.objects.all()
    return render(request, 'servicios/lista_servicios.html', {'servicios': servicios})


def llenar_formulario_fumigacion(request, servicio_id):
    servicio = ServicioFumigacion.objects.get(pk=servicio_id)
    if request.method == 'POST':
        form = ServicioFumigacionForm(request.POST, instance=servicio)
        if form.is_valid():
            form.save()
            return redirect('lista_servicios')
    else:
        form = ServicioFumigacionForm(instance=servicio)
    return render(request, 'servicios/llenar_formulario.html', {'form': form})

def llenar_formulario_lavado_tanque(request, servicio_id):
    servicio = ServicioLavadoTanque.objects.get(pk=servicio_id)
    if request.method == 'POST':
        form = ServicioLavadoTanqueForm(request.POST, instance=servicio)
        if form.is_valid():
            form.save()
            return redirect('lista_servicios')
    else:
        form = ServicioLavadoTanqueForm(instance=servicio)
    return render(request, 'servicios/llenar_formulario.html', {'form': form})

def llenar_formulario(request, servicio_id):
    servicio = get_object_or_404(Servicio, pk=servicio_id)

    if servicio.tipo_servicio.nombre == 'Fumigacion':
        form_class = ServicioFumigacionForm
    elif servicio.tipo_servicio.nombre == 'Lavado de Tanques':
        form_class = ServicioLavadoTanqueForm
    else:
        return HttpResponse('Tipo de servicio desconocido')

    EvidenciaMedidaFormSet = formset_factory(EvidenciaMedidaForm, extra=1, can_delete=True)
    ProductoUtilizadoFormSet = formset_factory(ProductoUtilizadoForm, extra=1, can_delete=True)

    if request.method == 'POST':
        form = form_class(request.POST, instance=servicio)
        evidencia_medida_formset = EvidenciaMedidaFormSet(request.POST, prefix='evidencias', instance=servicio)
        producto_utilizado_formset = ProductoUtilizadoFormSet(request.POST, prefix='productos', instance=servicio)

        if form.is_valid() and evidencia_medida_formset.is_valid() and producto_utilizado_formset.is_valid():
            servicio = form.save()

            for evidencia_medida_form in evidencia_medida_formset:
                evidencia_medida = evidencia_medida_form.save(commit=False)
                evidencia_medida.servicio = servicio
                evidencia_medida.save()

            for producto_utilizado_form in producto_utilizado_formset:
                producto_utilizado = producto_utilizado_form.save(commit=False)
                producto_utilizado.servicio = servicio
                producto_utilizado.save()

            return redirect('lista_servicios')
    else:
        form = form_class(instance=servicio)
        evidencia_medida_formset = EvidenciaMedidaFormSet(prefix='evidencias')
        producto_utilizado_formset = ProductoUtilizadoFormSet(prefix='productos')

    return render(request, 'servicios/llenar_formulario.html', {
    'form': form,
    'evidencia_medida_formset': evidencia_medida_formset,
    'producto_utilizado_formset': producto_utilizado_formset,
    })
