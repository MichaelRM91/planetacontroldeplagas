from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.forms import formset_factory
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Q
from django.views.generic.edit import (
    CreateView, UpdateView
)
from django.views.generic.detail import DetailView
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Servicio, ServicioFumigacion, ServicioLavadoTanque
from .forms import EvidenciaMedidaForm, ProductoUtilizadoForm
from datetime import date, timedelta
from .models import *

from .forms import (
    AsignacionServicioForm,
    ServicioForm,
    ServicioFumigacionEvidenciaMedidaFormSet,
    ServicioFumigacionForm,
    ServicioFumigacionProductoUtilizadoFormSet,
    ServicioLavadoTanqueForm,
    ServicioFumigacionRecomendacionesFormSet,
    ServicioFumigacionPrecaucionesFormSet,
    ServicioLavadoTanqueAnexosFormset,
    FirmaLavadoForm, FirmaFumigacionForm, ServicioLavadoTanqueFormset,
    ClienteForm

)

from django.views import View
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.http import JsonResponse

# Create your views here.

@login_required  # Agrega el decorador para asegurarte de que el usuario esté autenticado
@user_passes_test(lambda user: user.is_superuser)
def servicios_list(request):
    today_date = date.today()
    five_days_later = today_date + timedelta(days=5)
    servicios = Servicio.objects.exclude(estado_servicio__in=[2, 4]).order_by('fecha_ejecucion')
    form = AsignacionServicioForm(request.POST)
    return render(request, "servicios/servicios_list.html", {"servicios": servicios, "form": form, "today_date": today_date,"five_days_later": five_days_later})

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
        ctx['infoEmpresas'] = infoEmpresa.objects.get(id=1)
        ctx['firma'] = firmas_servicio_fumigacion.objects.filter(servicio_fumigacion=servicioFumigacion) if servicio_id else None
        
        return ctx

    def get_named_formsets(self):
        return {
            'envidencias': ServicioFumigacionEvidenciaMedidaFormSet(self.request.POST or None, self.request.FILES or None, instance=self.object, prefix='envidencias'),
            'productos': ServicioFumigacionProductoUtilizadoFormSet(self.request.POST or None, self.request.FILES or None, instance=self.object, prefix='productos'),
            'precauciones': ServicioFumigacionPrecaucionesFormSet(self.request.POST or None, self.request.FILES or None, prefix='precauciones'),
            'recomendaciones': ServicioFumigacionRecomendacionesFormSet(self.request.POST or None, self.request.FILES or None, prefix='recomendaciones'),
        }

class LavadoInline():
    form_class = ServicioLavadoTanqueForm
    model = ServicioLavadoTanque
    template_name = "servicios/lavado_create_or_update.html"

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
    
    def formset_anexos_valid(self, formset):
        anexos = formset.save(commit=False)  
        
        for obj in formset.deleted_objects:
            obj.delete()
        for anexo in anexos:
            anexo.servicio_lavado= self.object
            anexo.save()
            
    def formset_tanques_valid(self, formset):
        tanques = formset.save(commit=False)  
        
        for obj in formset.deleted_objects:
            obj.delete()
        for tanque in tanques:
            tanque.servicio_lavado= self.object
            tanque.save()
            
class LavadoCreate(LavadoInline, CreateView):

    def get_context_data(self, **kwargs):
        ctx = super(LavadoCreate, self).get_context_data(**kwargs)
        ctx['named_formsets'] = self.get_named_formsets()
        servicio_id = self.kwargs.get('servicio_id')
        ctx['servicio'] = Servicio.objects.get(id=servicio_id) if servicio_id else None

        return ctx
 
    def get_named_formsets(self):
        if self.request.method == "GET":
            return {
                'anexos': ServicioLavadoTanqueAnexosFormset(prefix='anexos'), 
                'tanques': ServicioLavadoTanqueFormset(prefix='tanques') 
            }
        else:
            return {
                'anexos': ServicioLavadoTanqueAnexosFormset(self.request.POST or None, self.request.FILES or None, prefix='anexos'),
                'tanques': ServicioLavadoTanqueFormset(self.request.POST or None, self.request.FILES or None, prefix='tanques')
            }  
            
class LavadoUpdate(LavadoInline, UpdateView):
    def get_object(self, queryset=None):
        # Recupera el atributo único de la URL en lugar de usar la pk
        servicio_id = self.kwargs.get('servicio_id')
        
        # Realiza una consulta para obtener el objeto utilizando el atributo único
        # Asegúrate de importar el modelo correcto y ajustar el nombre del campo
        return ServicioLavadoTanque.objects.get(servicio_id=servicio_id)
    def get_context_data(self, **kwargs):
        ctx = super(LavadoUpdate, self).get_context_data(**kwargs)
        ctx['named_formsets'] = self.get_named_formsets()
        servicio_id = self.kwargs.get('servicio_id')
        ctx['servicio'] = Servicio.objects.get(id=servicio_id) if servicio_id else None
        return ctx

    def get_named_formsets(self):
        return {
            'anexos': ServicioLavadoTanqueAnexosFormset(self.request.POST or None, self.request.FILES or None, instance=self.object, prefix='anexos'),
            'tanques': ServicioLavadoTanqueFormset(self.request.POST or None, self.request.FILES or None, instance=self.object, prefix='tanques')
        }    
        
class LavadoDetail(DetailView):
    model = ServicioLavadoTanque

    def get_object(self, queryset=None):
        # Recupera el atributo único de la URL en lugar de usar la pk
        servicio_id = self.kwargs.get('servicio_id')
        
        # Realiza una consulta para obtener el objeto utilizando el atributo único
        # Asegúrate de importar el modelo correcto y ajustar el nombre del campo
        return ServicioLavadoTanque.objects.get(servicio_id=servicio_id)
    def get_context_data(self, **kwargs):
        ctx = super(LavadoDetail, self).get_context_data(**kwargs)
        servicio_id = self.kwargs.get('servicio_id')
        ctx['servicio'] = Servicio.objects.get(id=servicio_id) if servicio_id else None
        ctx['servicio_lavado_list'] = ServicioLavadoTanque.objects.filter(servicio=servicio_id) if servicio_id else None
        asignacion = AsignacionServicio.objects.get(servicio_id=servicio_id)
        servicio_lavado = ServicioLavadoTanque.objects.get(servicio=servicio_id)
        ctx['anexos'] = AnexoImagen.objects.filter(servicio_lavado=servicio_lavado) if servicio_id else None
        ctx['tanques'] = Tanque.objects.filter(servicio_lavado=servicio_lavado) if servicio_id else None
        tecnico_asignado = asignacion.tecnico
        ctx['tecnico'] = tecnico_asignado
        ctx['infoEmpresas'] = infoEmpresa.objects.get(id=1)
        ctx['firma'] = firmas_servicio_Lavado.objects.filter(servicio_Lavado=servicio_lavado) if servicio_id else None
        anexo = AnexoImagen.objects.filter(servicio_lavado=servicio_lavado)
        tanque = Tanque .objects.filter(servicio_lavado=servicio_lavado)
        
        
        
        # Primero, obtén el objeto ServicioLavadoTanque deseado (puedes reemplazar 'id_del_servicio' con el ID real):
        servicio_lavado_tanque = ServicioLavadoTanque.objects.get(servicio=servicio_id)

        # Luego, puedes obtener los anexos asociados a este servicio:
        anexos_del_servicio = AnexoImagen.objects.filter(servicio_lavado=servicio_lavado_tanque)
        
        return ctx

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
            return redirect('welcome')


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

@login_required
def cliente_list(request):
    clientes = Cliente.objects.filter(estado='activo').order_by('-id')
    return render(request, 'clientes/cliente_list.html', {'clientes': clientes})
   
@login_required
def crear_cliente(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            cliente = form.save(commit=False)
            cliente.created_by = request.user  # Asignar el usuario en sesión al campo 'created_by'
            cliente.estado = 'activo'
            cliente.save()
            messages.success(request, "El cliente se ha creado exitosamente.")
            return redirect('cliente_list')
        else:
            messages.error(
                request,
                "Ha ocurrido un error al crear el cliente. Por favor, revise los campos e inténtelo nuevamente.",
            )
    else:
        form = ClienteForm()

    return render(request, 'clientes/crear_cliente.html', {'form': form})

@user_passes_test(lambda user: user.is_staff)
@login_required  # Agrega el decorador para asegurarte de que el usuario esté autenticado
def cliente_edit(request, pk):
    clientes = Cliente.objects.get(pk=pk)
    if request.method == "POST":
        form = ClienteForm(request.POST, instance=clientes)
        if form.is_valid():
            cliente = form.save(commit=False)
            cliente.created_by = request.user  
            clientes = form.save()
            return redirect("cliente_list")
    else:
        form = ClienteForm(instance=clientes)
    return render(
        request, "clientes/cliente_form.html", {"form": form, "clientes": clientes}
    )

@user_passes_test(lambda user: user.is_staff)
def eliminar_cliente(request, cliente_id):
    cliente = Cliente.objects.get(id=cliente_id)
    cliente.estado = 'no_activo'
    cliente.save()
    messages.success(request, "El cliente se ha marcado como inactivo.")
    return redirect('cliente_list')

@login_required
def welcome_view(request):
    return render(request, 'home.html')

@user_passes_test(lambda user: user.is_staff)
def eliminar_servicio(request, servicio_id):
    servicio = Servicio.objects.get(id=servicio_id)
    servicio.estado_servicio_id = 4
    servicio.save()
    return redirect('servicios_list')

def guardar_firma_lavado(request, servicio_id):
    if request.method == 'POST':
        form = FirmaLavadoForm(request.POST, request.FILES)
        if form.is_valid():
            firma = form.save(commit=False)
            firma.servicio_Lavado = ServicioLavadoTanque.objects.get(servicio=servicio_id)
            firma.save()
            return redirect('details_lavado', servicio_id=servicio_id)
        else:
            return JsonResponse({'success': False, 'errors': form.errors})
    else:
        form = FirmaLavadoForm()
    return redirect('details_lavado', servicio_id=servicio_id)

def guardar_firma_fumigacion(request, servicio_id):
    if request.method == 'POST':
        form = FirmaFumigacionForm(request.POST, request.FILES)
        if form.is_valid():
            firma = form.save(commit=False)
            firma.servicio_fumigacion = ServicioFumigacion.objects.get(servicio=servicio_id)
            firma.save()
            return redirect('details_product', servicio_id=servicio_id)
        else:
            return JsonResponse({'success': False, 'errors': form.errors})
    else:
        form = FirmaFumigacionForm()
    return redirect('details_product', servicio_id=servicio_id)


def iniciar_servicio(request, servicio_id):
    servicio = get_object_or_404(Servicio, pk=servicio_id)

    # Verifica que el servicio aún no haya sido iniciado
    if not servicio.fecha_inicio:
        servicio.fecha_inicio = timezone.now()
        servicio.save()
    return redirect('ver_servicios_tecnico')