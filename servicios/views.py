from django.contrib import messages
from django.shortcuts import render, redirect
from .models import Categoria, Servicio
from .forms import ServicioForm, CategoriaForm
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


def categoria_nueva(request):
    if request.method == "POST":
        form = CategoriaForm(request.POST)
        if form.is_valid():
            categoria = form.save()
            return redirect('servicio_nuevo')
    else:
        form = CategoriaForm()
    return render(request, 'servicios/categoria_edit.html', {'form': form})
