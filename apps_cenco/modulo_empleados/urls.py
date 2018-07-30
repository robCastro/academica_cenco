from django.conf.urls import url
from apps_cenco.modulo_empleados import views

urlpatterns = [
    url(r'^modificar/(?P<id_empleado>\d+)$', views.modificar_empleado, name="modificar_empleado"),
    url(r'^director_datos/$', views.director_datos_propios, name="director_datos_propios"),
    url(r'^director_datos_usuario/$', views.director_datos_propios_usuario, name="director_datos_propios_usuario"),
    url(r'^director_datos_correo/$', views.director_datos_propios_correo, name="director_datos_propios_correo"),
    url(r'^director_datos_contrasenia/$', views.director_datos_propios_contrasenia, name="director_datos_propios_contrasenia"),
]