from django.conf.urls import url

from apps_cenco.modulo_notas import views

urlpatterns = [
    url(r'^ingresar_notas/(?P<id_grupo>\d+)$', views.ingresar_nota, name='ingresar_notas'),
    url(r'^consultar_evaluaciones/$', views.consultar_evaluaciones, name='consultar_evaluaciones'),
    url(r'^finalizar_materia/(?P<id_alumno>\d+)$', views.finalizar_materia),
    url(r'^record_notas/$', views.ver_record_notas, name='ver_record_notas'),
    url(r'^ingresar_evaluaciones/$', views.ingresar_evaluaciones, name='ingresar_evaluaciones'),

]
