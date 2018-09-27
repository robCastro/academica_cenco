
from django.conf.urls import url
import views

#/asistencia/blabla
urlpatterns = [
    url(r'^ver_estados/$', views.ver_reporte_estados, name="director_ver_estados"),
    url(r'^ver_metricas_estado/$', views.ver_metricas_estado, name="director_ver_metricas_estado"),
    url(r'^filtrar_metricas_estados/$', views.filtrar_metricas),
    url(r'^filtrar_estados/$', views.filtrar_estado_por_periodo),
    url(r'^ingresar_asistencia/(?P<id_grupo>\d+)$', views.asistencia_a_clases, name="asistencia_grupo"), #para mostrar pantalla
    url(r'^guardar_asistencia/(?P<id_grupo>\d+)$', views.guardarAsistencia, name="guardar_asistencia_grupo"), #para guardar datos
    url(r'^prof_consultar/(?P<id_grupo>\d+)$', views.prof_detalle_grupo, name="prof_detalle_grupo"),
    url(r'^listado_asistencia/(?P<id_grupo>\d+)$',views.prof_listado_grupo, name="listado_asistencia_pdf"),
    url(r'^detalle_asistencia/(?P<id_alumno>\d+)$',views.detalle_asistencia, name="detalle_asistencia"),
]