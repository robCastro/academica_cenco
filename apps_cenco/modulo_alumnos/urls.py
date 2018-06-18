from django.conf.urls import url
from apps_cenco.modulo_alumnos import views

urlpatterns = [
    url(r'^insertar/$', views.RegistroAlumno, name="InsertarAlumno"),
    url(r'^insertarEncargado/$',views.RegistrEncargado, name="InsertarEncargado")



]