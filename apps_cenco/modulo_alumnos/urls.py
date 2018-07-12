from django.conf.urls import url
from apps_cenco.modulo_alumnos import views

urlpatterns = [
    url(r'^consultar/$', views.consultar_alumnos, name="asistenteConsultarAlumnos"),
    url(r'^(?P<id_alumno>\d+)$', views.detalle_alumno, name="detalle_alumno"),
    url(r'^modificar/(?P<id_alumno>\d+)$', views.modificar_alumno, name="modificar_alumno"),
    url(r'^misdatos/$', views.ver_alumno_propio, name="ver_alumno_propio"),
    url(r'^insertarAlum/$', views.inscribirAlumno, name="InsertarAlumnoV2"),
    url(r'^registrarEncargado/$',views.registrarEncargado, name="RegistrarEncargado"),
    url(r'^modificarAlum/(?P<id_alumno>\d+)$', views.modificar_alumno2, name="modificar_alumnoV2"),
]