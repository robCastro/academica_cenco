from django.conf.urls import url
from apps_cenco.login import views

urlpatterns = [
    url(r'^director/$', views.directorCredencialesPropias, name='credenciales_director'),
    url(r'^asistente/$', views.homeAsistente, name='home_asistente'),
    url(r'^alumno/$', views.homeAlumno, name='home_alumno'),

]