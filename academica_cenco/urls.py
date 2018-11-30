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
from django.conf.urls.static import static
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
    url(r'^configuracion/', include('apps_cenco.db_local.urls')),
    url(r'^asistencia/', include('apps_cenco.modulo_asistencia.urls')),
    url(r'^empleados/', include('apps_cenco.modulo_empleados.urls')),
    url(r'^carrera/', include('apps_cenco.modulo_carrera.urls')),
    url(r'^materia/', include('apps_cenco.modulo_materia.urls')),
    url(r'^notas/',  include('apps_cenco.modulo_notas.urls')),
    url(r'^pagos/',  include('apps_cenco.modulo_pagos.urls')),

    # for reset passwords
    url(r'^password_reset/$', auth_views.password_reset, {'template_name': 'sesiones/password_reset_form.html',
                                                          'html_email_template_name': 'sesiones/password_reset_email.html',
                                                          'subject_template_name': 'sesiones/password_reset_subject.txt'
                                                          }, name='password_reset'),
    url(r'^password_reset/done/$', auth_views.password_reset_done, {'template_name': 'sesiones/password_reset_done.html'}, name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        auth_views.password_reset_confirm, {'template_name': 'sesiones/password_reset_confirm.html'}, name='password_reset_confirm'),
    url(r'^reset/done/$', auth_views.password_reset_complete, {'template_name': 'sesiones/password_reset_complete.html'}, name='password_reset_complete'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

