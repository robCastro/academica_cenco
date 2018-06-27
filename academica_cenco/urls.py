"""academica_cenco URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.conf.urls import include

from apps_cenco.login.views import *
from apps_cenco.modulo_grupos.views import *
from apps_cenco.modulo_alumnos.views import *
from django.contrib.auth import views as auth_views

#  {'next_page': '/login'}

urlpatterns = [
    url(r'^$', principal, name="inicio"),  # Valida que sucede cuando se entra al localhost:8000/
    url(r'^accounts/login/$', auth_views.login, {'template_name': 'sesiones/login.html'}, name='login'),
    url(r'^logout/$', auth_views.logout, {'template_name': 'sesiones/logout.html'}, name='logout'),
    url(r'^admin/', admin.site.urls),
    url(r'^grupos/', include('apps_cenco.modulo_grupos.urls')),
    url(r'^credenciales/', include('apps_cenco.login.urls')),
    url(r'^alumnos/', include('apps_cenco.modulo_alumnos.urls')),
    url(r'^horarios/', include('apps_cenco.modulo_horarios.urls')),
]
