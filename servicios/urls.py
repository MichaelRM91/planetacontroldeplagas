from django.urls import include, path
from django.conf.urls.static import static  # add this
from .Account import views as Accountviews
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from django.conf import settings  # add this


from . import views
from django.contrib.auth.views import LogoutView
from .views import (
    ProductCreate, ProductDetail, ProductUpdate, 
)

urlpatterns = [
    path('', views.servicios_list, name='servicios_list'),
    path('servicioLavadoTanque/<int:servicio_id>/', views.llenar_formulario_lavado_tanque, name='servicioLavadoTanque'),
    path('servicio/editar/<int:pk>/', views.servicio_edit, name='servicio_edit'),
    path('crear_servicio/', views.crear_servicio, name='crear_servicio'),
    path('asignar_servicio/<int:servicio_id>/', views.asignar_servicio, name='asignar_servicio'),
    path('ver_servicios_tecnico/', views.ver_servicios_tecnico, name='ver_servicios_tecnico'),
    path('ver_servicios_completados/', views.ver_servicios_completados, name='ver_servicios_completados'),
    path('lista_servicios/', views.lista_servicios, name='lista_servicios'),
    path('llenar_formulario/<int:servicio_id>/', views.llenar_formulario, name='llenar_formulario'),
    path('create/<int:servicio_id>/', ProductCreate.as_view(), name='create_product'),
    path('update/<int:servicio_id>/', ProductUpdate.as_view(), name='update_product'),
    path('details/<int:servicio_id>/', ProductDetail.as_view(), name='details_product'),
    path('login/', views.user_login, name = "login.html"),
    path('logout/', views.user_logout, name = "logout"),
    path('account/', include('servicios.Account.urls')),
    path('password-change/', auth_views.PasswordChangeView.as_view(success_url=reverse_lazy('account:password_change_done')), name='password_change'),
    #path('delete-producto/<int:pk>/', delete_producto, name='delete_producto'),
    #path('delete-evidencia/<int:pk>/', delete_evidencia, name='delete_evidencia'),


]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)