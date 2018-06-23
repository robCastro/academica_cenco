
from django.conf.urls import url
from apps_cenco.modulo_grupos import views

urlpatterns = [
    url(r'^consultar/$', views.consultar_grupos, name="consultar_grupos"),
    url(r'^consultar/(?P<id_grupo>\d+)$', views.detalle_grupo, name="detalle_grupo"),
    url(r'^eliminar/(?P<id_grupo>\d+)$', views.eliminarGrupo, name="eliminar_grupo")
]

