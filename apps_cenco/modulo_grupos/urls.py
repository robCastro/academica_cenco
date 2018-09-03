from django.conf.urls import url
from apps_cenco.modulo_grupos import views

urlpatterns = [
    url(r'^consultar/$', views.consultar_grupos, name="consultar_grupos"),
    url(r'^consultar/(?P<id_grupo>\d+)$', views.detalle_grupo, name="detalle_grupo"),
    url(r'^eliminar/(?P<id_grupo>\d+)$', views.eliminarGrupo, name="eliminar_grupo"),
    url(r'^asist_consultar/$', views.asist_consultar_grupos, name="asistente_consultar_grupos"),
    url(r'^asist_consultar/(?P<id_grupo>\d+)$', views.asist_detalle_grupo, name="asist_detalle_grupo"),
    url(r'^prof_consultar/$', views.prof_consultar_grupos, name="profesor_consultar_grupos"),
]