from django.conf import settings  # add this
from django.conf.urls.static import static  # add this
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path
from django.urls import re_path
from . import views as accountView
# urls
urlpatterns = [
            re_path('password/', accountView.change_password, name='change_password'),
      ]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)