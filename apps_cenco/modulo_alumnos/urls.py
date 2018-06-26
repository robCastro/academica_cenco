from django.conf.urls import url
from apps_cenco.modulo_alumnos import views

urlpatterns = [
    url(r'^insertar/$', views.registro_alumno, name="InsertarAlumno"),
    url(r'^insertarEncargado/$',views.registrar_encargado, name="InsertarEncargado"),
    url(r'^(?P<id_alumno>\d+)$', views.modificar_alumno, name="modificar_alumno"),
    url(r'^misdatos/$', views.ver_alumno_propio, name="ver_alumno_propio"),
]