from django.contrib import admin
from .models import Categoria, Cliente, Servicio

# Register your models here.
admin.site.register(Categoria)
admin.site.register(Servicio)
admin.site.register(Cliente)
