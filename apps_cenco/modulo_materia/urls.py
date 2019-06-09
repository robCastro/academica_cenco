from django.conf.urls import url
from apps_cenco.modulo_materia import views as matViews

urlpatterns = [
    url(r'^crear_materia/$', matViews.crear_materia, name='crear_materia'),
    url(r'^editar_materia/(?P<id_materia>\d+)$', matViews.editar_materia, name='modificar_materia'),
    url(r'^subir_documento/$', matViews.subir_documentos, name='subir_doc'),
    url(r'^descargar_documento/$', matViews.descargar_documentos, name='descargar_doc'),
    url(r'^consultar_material/$', matViews.consultar_material, name='consultar_material'),
]
