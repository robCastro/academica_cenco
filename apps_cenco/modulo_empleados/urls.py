from django.conf.urls import url
from apps_cenco.modulo_empleados import views

urlpatterns = [
    url(r'^consultar/$', views.consultar_empleados, name="consultar_empleados"),
    url(r'^crear/$', views.dir_crear_empleado, name="crear_empleado"),
    url(r'^(?P<id_empleado>\d+)$', views.detalle_de_empleado, name="detalle_empleado"),

]