
from django.conf.urls import url
import views

urlpatterns = [
    url(r'^ver_estados/$', views.ver_reporte_estados),
]