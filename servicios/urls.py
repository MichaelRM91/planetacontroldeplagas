from django.urls import path
from . import views

urlpatterns = [
    path('', views.servicios_list, name='servicios_list'),
    path('servicio/nuevo/', views.servicio_nuevo, name='servicio_nuevo'),
    path('servicio/editar/<int:pk>/', views.servicio_edit, name='servicio_edit'),
    path('categoria/nueva/', views.categoria_nueva, name='categoria_nueva'),

]