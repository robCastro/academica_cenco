from django.conf.urls import url
from apps_cenco.modulo_alumnos import views

urlpatterns = [
    url(r'^(?P<id_alumno>\d+)$', views.modificar_alumno, name="modificar_alumno"),
    url(r'^misdatos/$', views.ver_alumno_propio, name="ver_alumno_propio"),

]