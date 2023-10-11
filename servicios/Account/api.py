
from django.conf import settings  # add this
from django.conf.urls.static import static  # add this
from django.contrib import admin
from django.urls import path
from . import views as accountView
# urls via api REST
urlpatterns = [

      ]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)