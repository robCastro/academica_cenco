from django.conf.urls import url
from apps_cenco.login import views

urlpatterns = [
    url(r'^director/$', views.directorCredencialesPropias, name="director_credenciales_propias"),
    url(r'^cerrar_sesion/$', views.log_out, name="cerrar_sesion"),
    url(r'^asistente/$', views.asistenteCredencialesPropias,name='asistenteCredencialesPropias'),
    url(r'^alumno/$', views.alumnoCredencialesPropias,name='alumnoCredencialesPropias'),
    url(r'^director/$', views.directorCredencialesPropias, name='credenciales_director'),
    url(r'^asistente/$', views.homeAsistente, name='home_asistente'),
    url(r'^alumno/$', views.homeAlumno, name='home_alumno'),

]