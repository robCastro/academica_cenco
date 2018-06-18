from django.conf.urls import url
from apps_cenco.modulo_alumnos import views

urlpatterns = [
    url(r'^insertar/$', views.registro_alumno, name="InsertarAlumno"),
    url(r'^insertarEncargado/$',views.registrar_encargado, name="InsertarEncargado")



]