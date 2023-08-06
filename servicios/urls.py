from django.urls import path
from . import views

urlpatterns = [
    path('', views.servicios_list, name='servicios_list'),
    path('servicioLavadoTanque/nuevo/', views.crear_servicio_lavado_tanque, name='servicioLavadoTanque'),
    path('servicio/editar/<int:pk>/', views.servicio_edit, name='servicio_edit'),
    path('servicioFumigacion/nuevo/', views.crear_servicio_fumigacion, name='servicioFumigacion_nuevo'),
    path('crear_servicio/', views.crear_servicio, name='crear_servicio'),
    path('asignar_servicio/', views.asignar_servicio, name='asignar_servicio'),
    path('ver_servicios_tecnico/', views.ver_servicios_tecnico, name='ver_servicios_tecnico'),
    path('lista_servicios/', views.lista_servicios, name='lista_servicios'),
    path('llenar_formulario_fumigacion/<int:servicio_id>/', views.llenar_formulario_fumigacion, name='llenar_formulario_fumigacion'),
    path('llenar_formulario_lavado_tanque/<int:servicio_id>/', views.llenar_formulario_lavado_tanque, name='llenar_formulario_lavado_tanque'),
    path('llenar_formulario/<int:servicio_id>/', views.llenar_formulario, name='llenar_formulario'),







]