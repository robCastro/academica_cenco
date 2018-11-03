from django.conf.urls import url
from apps_cenco.modulo_materia import views as matViews

urlpatterns = [
    url(r'^crear_materia/$', matViews.crear_materia),
    url(r'^editar_materia/(?P<id_materia>\d+)$', matViews.editar_materia),
]
