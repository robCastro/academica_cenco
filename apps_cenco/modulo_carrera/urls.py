from django.conf.urls import url
from apps_cenco.modulo_carrera import views as carrViews

urlpatterns = [
    url(r'^crear_carrera/$', carrViews.crear_carrera),
    url(r'^editar_carrera/(?P<id_carrera>\d+)$', carrViews.editar_carrera),
]
