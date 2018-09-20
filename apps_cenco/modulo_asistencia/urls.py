
from django.conf.urls import url
import views

#/asistencia/blabla
urlpatterns = [
    url(r'^ver_estados/$', views.ver_reporte_estados, name="director_ver_estados"),
    url(r'^filtrar_estados/$', views.filtrar_estado_por_periodo),
    url(r'^ingresar_asistencia/(?P<id_grupo>\d+)$', views.asistencia_a_clases, name="asistencia_grupo"), #para mostrar pantalla
    url(r'^guardar_asistencia/(?P<id_grupo>\d+)$', views.guardarAsistencia, name="guardar_asistencia_grupo"), #para guardar datos
]