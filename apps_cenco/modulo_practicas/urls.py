from django.conf.urls import url

from apps_cenco.modulo_practicas import views

urlpatterns = [
    url(r'^reservar_practica/$', views.reservar_practica,name="reservarPractica"),
]