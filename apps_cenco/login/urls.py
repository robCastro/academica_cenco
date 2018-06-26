from django.conf.urls import url
from apps_cenco.login import views

urlpatterns = [
    url(r'^asistente/$', views.asistenteCredencialesPropias,name='asistenteCredencialesPropias'),
    url(r'^alumno/$', views.alumnoCredencialesPropias,name='alumnoCredencialesPropias')
]