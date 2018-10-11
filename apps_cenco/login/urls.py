from django.conf.urls import url
from apps_cenco.login import views

urlpatterns = [
    url(r'^director/$', views.directorCredencialesPropias, name="director_credenciales_propias"),
    url(r'^cerrar_sesion/$', views.log_out, name="cerrar_sesion"),
    url(r'^empleado/$', views.empleadoCredencialesPropias,name='empleadoCredencialesPropias'),
    url(r'^alumno/$', views.alumnoCredencialesPropias,name='alumnoCredencialesPropias'),
    url(r'^director_home/$', views.directorCredencialesPropias, name='credenciales_director'),
    url(r'^asistente_home/$', views.homeAsistente, name='home_asistente'),
    url(r'^alumno_home/$', views.homeAlumno, name='home_alumno'),
    url(r'^alumnos/$', views.consultar_alumnos,name='credenciales_alumno'),
    url(r'^asistentes/$', views.consultar_asistentes,name='credenciales_asistente'),
    url(r'^profesores/$', views.consultar_profesores,name='credenciales_profesores'),
    url(r'^tecnicos/$', views.consultar_tecnicos,name='credenciales_tecnicos'),
    url(r'^encargados/$', views.consultar_encargados,name='credenciales_encargados'),
]