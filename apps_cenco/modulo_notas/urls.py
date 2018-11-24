from django.conf.urls import url

from apps_cenco.modulo_notas import views

urlpatterns = [
    url(r'^ingresar_notas/(?P<id_grupo>\d+)$', views.ingresar_nota),
]
