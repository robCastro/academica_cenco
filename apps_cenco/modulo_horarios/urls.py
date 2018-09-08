from django.conf.urls import url
from apps_cenco.modulo_horarios import views


urlpatterns = [
    url(r'^consultar/$', views.consultar_horario, name='crud_horario'),
    url(r'^eliminar/$', views.eliminar_horario),
    url(r'^crear/$', views.crear_nuevo_horario),
    url(r'^editar/$', views.editar_horario),

    ]
