
from django.conf.urls import url
import views

urlpatterns = [
    url(r'^ver_estados/$', views.ver_reporte_estados),
    url(r'^filtrar_estados/$', views.filtrar_estado_por_periodo),
]