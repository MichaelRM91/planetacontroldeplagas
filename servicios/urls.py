from django.urls import path
from . import views
from .views import (
    ProductCreate, ProductUpdate, 
)

urlpatterns = [
    path('', views.servicios_list, name='servicios_list'),
    path('servicioLavadoTanque/<int:servicio_id>/', views.llenar_formulario_lavado_tanque, name='servicioLavadoTanque'),
    path('servicio/editar/<int:pk>/', views.servicio_edit, name='servicio_edit'),
    path('crear_servicio/', views.crear_servicio, name='crear_servicio'),
    path('asignar_servicio/', views.asignar_servicio, name='asignar_servicio'),
    path('ver_servicios_tecnico/', views.ver_servicios_tecnico, name='ver_servicios_tecnico'),
    path('ver_servicios_completados/', views.ver_servicios_completados, name='ver_servicios_completados'),
    path('lista_servicios/', views.lista_servicios, name='lista_servicios'),
    path('llenar_formulario/<int:servicio_id>/', views.llenar_formulario, name='llenar_formulario'),
    path('create/<int:servicio_id>/', ProductCreate.as_view(), name='create_product'),
    path('update/<int:servicio_id>/', ProductUpdate.as_view(), name='update_product'),
    #path('delete-producto/<int:pk>/', delete_producto, name='delete_producto'),
    #path('delete-evidencia/<int:pk>/', delete_evidencia, name='delete_evidencia'),


 




]