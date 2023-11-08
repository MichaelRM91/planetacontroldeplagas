from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.forms import formset_factory
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.views.generic.edit import (
    CreateView, UpdateView
)
from django.views.generic.detail import DetailView
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Servicio, ServicioFumigacion, ServicioLavadoTanque
from .forms import EvidenciaMedidaForm, ProductoUtilizadoForm

from .models import *

from .forms import (
    AsignacionServicioForm,
    ServicioForm,
    ServicioFumigacionEvidenciaMedidaFormSet,
    ServicioFumigacionForm,
    ServicioFumigacionProductoUtilizadoFormSet,
    ServicioLavadoTanqueForm,
    ServicioFumigacionRecomendacionesFormSet,
    ServicioFumigacionPrecaucionesFormSet
)

# Create your views here.

@login_required  # Agrega el decorador para asegurarte de que el usuario esté autenticado
def servicios_list(request):
    servicios = Servicio.objects.exclude(estado_servicio=2).order_by('-id')
    print(servicios)
    form = AsignacionServicioForm(request.POST)
    return render(request, "servicios/servicios_list.html", {"servicios": servicios, "form": form})

@login_required  # Agrega el decorador para asegurarte de que el usuario esté autenticado
def servicio_nuevo(request):
    if request.method == "POST":
        form = ServicioForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "El servicio se ha creado exitosamente.")
            return redirect("servicios_list")
        else:
            messages.error(
                request,
                "Ha ocurrido un error al crear el servicio. Por favor, revise los campos e inténtelo nuevamente.",
            )
    else:
        form = ServicioForm()
    return render(request, "servicios/servicio_form.html", {"form": form})

@login_required  # Agrega el decorador para asegurarte de que el usuario esté autenticado
def servicio_edit(request, pk):
    servicio = Servicio.objects.get(pk=pk)
    if request.method == "POST":
        form = ServicioForm(request.POST, instance=servicio)
        if form.is_valid():
            servicio = form.save()
            return redirect("servicios_list")
    else:
        form = ServicioForm(instance=servicio)
    return render(
        request, "servicios/servicio_form.html", {"form": form, "servicio": servicio}
    )


# servicios/views.py

@login_required  # Agrega el decorador para asegurarte de que el usuario esté autenticado
def crear_servicio_fumigacion(request):
    if request.method == "POST":
        form = ServicioFumigacionForm(request.POST)
        if form.is_valid():
            servicio = form.save()
            # Realizar acciones adicionales o redireccionar
    else:
        form = ServicioFumigacionForm()

    context = {"form": form}
    return render(request, "servicios/crear_servicio_fumigacion.html", context)

@login_required  # Agrega el decorador para asegurarte de que el usuario esté autenticado
def crear_servicio_lavado_tanque(request):
    if request.method == "POST":
        form = ServicioFumigacionForm(request.POST)
        if form.is_valid():
            servicio = form.save()
            # Realizar acciones adicionales o redireccionar
    else:
        form = ServicioFumigacionForm()

    context = {"form": form}
    return render(request, "servicios/crear_servicio_fumigacion.html", context)


@login_required  # Agrega el decorador para asegurarte de que el usuario esté autenticado
def crear_servicio(request):
    if request.method == "POST":
        form = ServicioForm(request.POST)
        if form.is_valid():
            servicio = form.save(
                commit=False
            )  # Crea una instancia del servicio sin guardarla en la base de datos todavía
            servicio.usuario = request.user  # Asigna el usuario actual al servicio
            servicio.save()  # Ahora guarda el servicio con el usuario asignado
            return redirect(
                "servicios_list"
            )  # Redirige a la lista de servicios después de crear uno nuevo
    else:
        form = ServicioForm()

    return render(request, "servicios/crear_servicio.html", {"form": form})

@login_required  # Agrega el decorador para asegurarte de que el usuario esté autenticado
def asignar_servicio(request, servicio_id):
    servicio = Servicio.objects.get(id=servicio_id)

    if request.method == "POST":
        form = AsignacionServicioForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("servicios_list")
    else:
        form = AsignacionServicioForm()

    return render(request, "servicios/servicios_list.html", {"form": form})

@login_required  # Agrega el decorador para asegurarte de que el usuario esté autenticado
def reasignar_servicio(request, servicio_id):
    nuevo_estado = get_object_or_404(EstadoServicio, pk=3)
    servicio = Servicio.objects.get(id=servicio_id)
    servicio.estado_servicio = nuevo_estado
    servicio.save()
    print(servicio.estado_servicio.nombre)
    return redirect('servicios_list')


@login_required  # Agrega el decorador para asegurarte de que el usuario esté autenticado
def ver_servicios_tecnico(request):
    tecnico = request.user.tecnico
    servicios_asignados = AsignacionServicio.objects.filter(
    Q(tecnico=tecnico) & Q(servicio__estado_servicio__nombre="Asignado")
).order_by('-id')


    if request.method == "POST":
        # Procesar el formulario de marcado como completado
        servicio_id = request.POST.get("servicio_id")
        if servicio_id:
            servicio = Servicio.objects.get(pk=servicio_id)
            servicio.estado_servicio = EstadoServicio.objects.get(nombre="Completado")
            servicio.save()
            return redirect("ver_servicios_tecnico")

    return render(
        request,
        "servicios/ver_servicios_tecnico.html",
        {"servicios_asignados": servicios_asignados},
    )

@login_required  # Agrega el decorador para asegurarte de que el usuario esté autenticado
def ver_servicios_completados(request):
    tecnico = request.user.tecnico
    servicios_asignados = AsignacionServicio.objects.filter(Q(tecnico=tecnico) & Q(servicio__estado_servicio__nombre = "Completado"))
    return render(
        request,
        "servicios/ver_servicios_tecnico_completados.html",
        {"servicios_asignados": servicios_asignados},
    )

@login_required  # Agrega el decorador para asegurarte de que el usuario esté autenticado
def lista_servicios(request):
    servicios = Servicio.objects.all()
    return render(request, "servicios/lista_servicios.html", {"servicios": servicios})

@login_required  # Agrega el decorador para asegurarte de que el usuario esté autenticado
def llenar_formulario_fumigacion(request, servicio_id):
    servicio = ServicioFumigacion.objects.get(pk=servicio_id)
    if request.method == "POST":
        form = ServicioFumigacionForm(request.POST, instance=servicio)
        if form.is_valid():
            form.save()
            return redirect("lista_servicios")
    else:
        form = ServicioFumigacionForm(instance=servicio)
    return render(request, "servicios/llenar_formulario.html", {"form": form})

@login_required  # Agrega el decorador para asegurarte de que el usuario esté autenticado
def llenar_formulario_lavado_tanque(request, servicio_id):
    servicio = ServicioLavadoTanque.objects.get(pk=servicio_id)
    if request.method == "POST":
        form = ServicioLavadoTanqueForm(request.POST, instance=servicio)
        if form.is_valid():
            form.save()
            return redirect("lista_servicios")
    else:
        form = ServicioLavadoTanqueForm(instance=servicio)
    return render(request, "servicios/llenar_formulario.html", {"form": form})


class FumigacionInline():
    form_class = ServicioFumigacionForm
    model = ServicioFumigacion
    template_name = "servicios/fumigacion_create_or_update.html"

    def form_valid(self, form):
        # Paso 1: Obtén el objeto del servicio usando el ID proporcionado en la URL
        servicio_id = self.kwargs.get('servicio_id')
        servicio = None
        if servicio_id:
            servicio = Servicio.objects.get(id=servicio_id)

        # Paso 2: Asigna el objeto del servicio al campo relevante en el formulario
        if servicio:
            form.instance.servicio = servicio

        named_formsets = self.get_named_formsets()
        if not all((x.is_valid() for x in named_formsets.values())):
            return self.render_to_response(self.get_context_data(form=form))

        # Save the main object first
        self.object = form.save()

        # Now that the main object is saved, you can save the related objects
        for name, formset in named_formsets.items():
            formset_save_func = getattr(self, 'formset_{0}_valid'.format(name), None)
            if formset_save_func is not None:
                formset_save_func(formset)
            else:
                formset.save()

        return redirect('ver_servicios_tecnico')

    def formset_envidencias_valid(self, formset):
        """
        Hook for custom formset saving.Useful if you have multiple formsets
        """
        envidencias = formset.save(commit=False)  # self.save_formset(formset, contact)
        # add this 2 lines, if you have can_delete=True parameter 
        # set in inlineformset_factory func
        for obj in formset.deleted_objects:
            obj.delete()
        for EvidenciaMedida in envidencias:
            EvidenciaMedida.servicio_fumigacion = self.object
            EvidenciaMedida.save()
    def formset_productos_valid(self, formset):
        """
        Hook for custom formset saving.Useful if you have multiple formsets
        """
        productos = formset.save(commit=False)  # self.save_formset(formset, contact)
        # add this 2 lines, if you have can_delete=True parameter 
        # set in inlineformset_factory func
        for obj in formset.deleted_objects:
            obj.delete()
        for ProductoUtilizado in productos:
            ProductoUtilizado.servicio_fumigacion = self.object
            ProductoUtilizado.save()
            
    def formset_precauciones_valid(self, formset):
        """
        Hook for custom formset saving.Useful if you have multiple formsets
        """
        precaucion = formset.save(commit=False)  # self.save_formset(formset, contact)
        # add this 2 lines, if you have can_delete=True parameter 
        # set in inlineformset_factory func
        for obj in formset.deleted_objects:
            obj.delete()
        for precauciones in precaucion:
            precauciones.servicio_fumigacion = self.object
            precauciones.save()
            
    def formset_recomendaciones_valid(self, formset):
        """
        Hook for custom formset saving.Useful if you have multiple formsets
        """
        recomendacion = formset.save(commit=False)  # self.save_formset(formset, contact)
        # add this 2 lines, if you have can_delete=True parameter 
        # set in inlineformset_factory func
        for obj in formset.deleted_objects:
            obj.delete()
        for recomendaciones in recomendacion:
            recomendaciones.servicio_fumigacion = self.object
            recomendaciones.save()

class ProductCreate(FumigacionInline, CreateView):

    def get_context_data(self, **kwargs):
        ctx = super(ProductCreate, self).get_context_data(**kwargs)
        ctx['named_formsets'] = self.get_named_formsets()
        servicio_id = self.kwargs.get('servicio_id')
        ctx['servicio'] = Servicio.objects.get(id=servicio_id) if servicio_id else None

        return ctx
 
    def get_named_formsets(self):
        if self.request.method == "GET":
            return {
                'envidencias': ServicioFumigacionEvidenciaMedidaFormSet(prefix='envidencias'),
                'productos': ServicioFumigacionProductoUtilizadoFormSet(prefix='productos'),
                'precauciones': ServicioFumigacionPrecaucionesFormSet(prefix='precauciones'),
                'recomendaciones': ServicioFumigacionRecomendacionesFormSet(prefix='recomendaciones'),
                
            }
        else:
            return {
                'envidencias': ServicioFumigacionEvidenciaMedidaFormSet(self.request.POST or None, self.request.FILES or None, prefix='envidencias'),
                'productos': ServicioFumigacionProductoUtilizadoFormSet(self.request.POST or None, self.request.FILES or None, prefix='productos'),
                'precauciones': ServicioFumigacionPrecaucionesFormSet(self.request.POST or None, self.request.FILES or None, prefix='precauciones'),
                'recomendaciones': ServicioFumigacionRecomendacionesFormSet(self.request.POST or None, self.request.FILES or None, prefix='recomendaciones'),
            }


class ProductUpdate(FumigacionInline, UpdateView):
    def get_object(self, queryset=None):
        # Recupera el atributo único de la URL en lugar de usar la pk
        servicio_id = self.kwargs.get('servicio_id')
        
        # Realiza una consulta para obtener el objeto utilizando el atributo único
        # Asegúrate de importar el modelo correcto y ajustar el nombre del campo
        return ServicioFumigacion.objects.get(servicio_id=servicio_id)
    def get_context_data(self, **kwargs):
        ctx = super(ProductUpdate, self).get_context_data(**kwargs)
        ctx['named_formsets'] = self.get_named_formsets()
        servicio_id = self.kwargs.get('servicio_id')
        ctx['servicio'] = Servicio.objects.get(id=servicio_id) if servicio_id else None
        return ctx

    def get_named_formsets(self):
        return {
            'envidencias': ServicioFumigacionEvidenciaMedidaFormSet(self.request.POST or None, self.request.FILES or None, instance=self.object, prefix='envidencias'),
            'productos': ServicioFumigacionProductoUtilizadoFormSet(self.request.POST or None, self.request.FILES or None, instance=self.object, prefix='productos'),
            'precauciones': ServicioFumigacionPrecaucionesFormSet(self.request.POST or None, self.request.FILES or None, instance=self.object, prefix='precauciones'),
            'recomendaciones': ServicioFumigacionRecomendacionesFormSet(self.request.POST or None, self.request.FILES or None, instance=self.object, prefix='recomendaciones'),
        }

class ProductDetail(DetailView):
    model = ServicioFumigacion

    
    def get_object(self, queryset=None):
        # Recupera el atributo único de la URL en lugar de usar la pk
        servicio_id = self.kwargs.get('servicio_id')
        
        # Realiza una consulta para obtener el objeto utilizando el atributo único
        # Asegúrate de importar el modelo correcto y ajustar el nombre del campo
        return ServicioFumigacion.objects.get(servicio_id=servicio_id)
    def get_context_data(self, **kwargs):
        ctx = super(ProductDetail, self).get_context_data(**kwargs)
        ctx['named_formsets'] = self.get_named_formsets()
        servicio_id = self.kwargs.get('servicio_id')
        ctx['servicio'] = Servicio.objects.get(id=servicio_id) if servicio_id else None
        ctx['servicio_fumigacion_list'] = ServicioFumigacion.objects.filter(servicio=servicio_id) if servicio_id else None
        servicioFumigacion = ServicioFumigacion.objects.filter(servicio=servicio_id).first() if servicio_id else None
        ctx['evidencia_medida'] = EvidenciaMedida.objects.filter(servicio_fumigacion=servicioFumigacion) if servicioFumigacion else None
        ctx['productos_utilizados'] = ProductoUtilizado.objects.filter(servicio_fumigacion=servicioFumigacion) if servicioFumigacion else None
        ctx['precauciones'] = ServicioPrecaucion.objects.filter(servicio_fumigacion=servicioFumigacion) if servicioFumigacion else None
        ctx['recomendaciones'] = ServicioRecomendacion.objects.filter(servicio_fumigacion=servicioFumigacion) if servicioFumigacion else None
        asignacion = AsignacionServicio.objects.get(servicio_id=servicio_id)
        tecnico_asignado = asignacion.tecnico
        ctx['tecnico'] = tecnico_asignado
        
        return ctx

    def get_named_formsets(self):
        return {
            'envidencias': ServicioFumigacionEvidenciaMedidaFormSet(self.request.POST or None, self.request.FILES or None, instance=self.object, prefix='envidencias'),
            'productos': ServicioFumigacionProductoUtilizadoFormSet(self.request.POST or None, self.request.FILES or None, instance=self.object, prefix='productos'),
            'precauciones': ServicioFumigacionPrecaucionesFormSet(self.request.POST or None, self.request.FILES or None, prefix='precauciones'),
            'recomendaciones': ServicioFumigacionRecomendacionesFormSet(self.request.POST or None, self.request.FILES or None, prefix='recomendaciones'),
        }


def user_login(request):
    if request.method == 'GET':
        return render(request, 'login.html', {
            'form' : AuthenticationForm
        })
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'login.html', {
                'form': AuthenticationForm,
                'error': 'nombre de usuario o password incorrectos'
            })
        else:
            login(request, user)
            return redirect('/')


def user_logout(request):
    logout(request)
    return redirect('/')


@login_required
def cliente_servicios(request):
    cliente = Cliente.objects.get(user=request.user)
    servicios = Servicio.objects.filter(cliente=cliente, estado_servicio=2).order_by('-id')

    return render(request, 'servicios/servicios_client.html', {
        'servicios': servicios
    })