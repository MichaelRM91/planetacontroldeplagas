from django.urls import include, path
from django.conf.urls.static import static  # add this
from .Account import views as Accountviews
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from django.conf import settings  # add this
from django.views.generic.edit import UpdateView

from . import views
from django.contrib.auth.views import LogoutView
from .views import *

urlpatterns = [
    path('', views.servicios_list, name='servicios_list'),
    path('servicioLavadoTanque/<int:servicio_id>/', views.llenar_formulario_lavado_tanque, name='servicioLavadoTanque'),
    path('servicio/editar/<int:pk>/', views.servicio_edit, name='servicio_edit'),
    path('crear_servicio/', views.crear_servicio, name='crear_servicio'),
    path('asignar_servicio/<int:servicio_id>/', views.asignar_servicio, name='asignar_servicio'),
    path('reasignar_servicio/<int:servicio_id>/', views.reasignar_servicio, name='reasignar_servicio'),
    path('ver_servicios_tecnico/', views.ver_servicios_tecnico, name='ver_servicios_tecnico'),
    path('ver_servicios_completados/', views.ver_servicios_completados, name='ver_servicios_completados'),
    path('lista_servicios/', views.lista_servicios, name='lista_servicios'),
    path('create_lavado/<int:servicio_id>/', LavadoCreate.as_view(), name='create_lavado'),
    path('update_lavado/<int:servicio_id>/', LavadoUpdate.as_view(), name='update_lavado'),
    path('details_lavado/<int:servicio_id>/', LavadoDetail.as_view(), name='details_lavado'),
    path('create/<int:servicio_id>/', ProductCreate.as_view(), name='create_product'),
    path('update/<int:servicio_id>/', ProductUpdate.as_view(), name='update_product'),
    path('details/<int:servicio_id>/', ProductDetail.as_view(), name='details_product'),
    path('login/', views.user_login, name = "login.html"),
    path('logout/', views.user_logout, name = "logout"),
    path('account/', include('servicios.Account.urls')),
    path('bienvenida/', welcome_view, name='welcome'),
    path('password-change/', auth_views.PasswordChangeView.as_view(success_url=reverse_lazy('account:password_change_done')), name='password_change'),
    path('servicios_cliente/', views.cliente_servicios, name='cliente_servicios'),
    path('delete_servicio/<int:servicio_id>/', views.eliminar_servicio, name='delete_servicio'),
    path('guardar_firma_lavado/<int:servicio_id>/', views.guardar_firma_lavado, name='guardar_firma_lavado'),
    path('guardar_firma_fumigacion/<int:servicio_id>/', views.guardar_firma_fumigacion, name='guardar_firma_fumigacion'),
    path('cliente_list/', views.cliente_list, name='cliente_list'),
    path('crear_cliente/', views.crear_cliente, name='crear_cliente'),
    path('clientes/editar/<int:pk>/', views.cliente_edit, name='cliente_edit'),
    path('delete_cliente/<int:cliente_id>/', views.eliminar_cliente, name='delete_cliente'),
    path('iniciar_servicio/<int:servicio_id>/', views.iniciar_servicio, name='iniciar_servicio'),
    path('servicios/servicios_all/', views.ver_servicios_all, name='ver_servicios_all'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)