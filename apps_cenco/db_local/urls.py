from django.conf.urls import url

from apps_cenco.db_local import views

urlpatterns = [
    url(r'^editar/$', views.editar_configuracion, name="editarConfig"),
    url(r'^editar_footer/$', views.editar_footer, name="editarFooter"),

]
