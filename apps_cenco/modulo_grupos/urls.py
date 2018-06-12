
from django.conf.urls import url
from apps_cenco.modulo_grupos import views

urlpatterns = [
    url(r'^consultar/$', views.consultar_grupos),
    url(r'^(?P<id_grupo>\d+)$', views.detalle_grupo, name="detalle_grupo")

]

