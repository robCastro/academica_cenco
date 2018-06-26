from django.conf.urls import url
from apps_cenco.login import views

urlpatterns = [
    url(r'^director/$', views.directorCredencialesPropias),
]