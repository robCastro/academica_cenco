from django.conf.urls import url
from apps_cenco.modulo_pagos import views

urlpatterns = [
    url(r'^detalle_pagos/(?P<idAlumno>\d+)$', views.detalle_pago, name='detalle_pagos'),
    url(r'^detalle_pagos/(?P<idAlumno>\d+)/(?P<cod_mensaje>\d+)$', views.detalle_pago, name='detalle_pagos_mensaje'),
    url(r'^modificar_pago/(?P<idAlumno>\d+)/(?P<idPago>\d+)$', views.modificar_pago, name='modificar_pago'),
    url(r'^eliminar_pago/(?P<idAlumno>\d+)/(?P<idPago>\d+)$', views.eliminar_pago, name='eliminar_pago'),
    url(r'^cola_pagos/$', views.ver_cola_impresion, name='cola_pagos'),
    url(r'^imprimir_cola/$', views.imprimir_cola, name='imprimir_cola_pagos'),
    url(r'^ver_alumnos/$', views.ver_alumnos, name='ver_alumnos'),
    url(r'^ingresar_pago/$', views.ingresar_pago, name='ingresar_pago'),
    url(r'^filtrar_alumnos/$', views.filtrarAlumnos, name='filtrar_alumnos'),
    url(r'^pagos_pdf/(?P<codigos>[\w\-]+)/$',views.pdf_pagos, name="pagos_pdf"),
    url(r'^recibo_pdf/(?P<codigo>\d+)$',views.pdf_recibo, name="recibo_pdf"),
]