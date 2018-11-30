from django.conf.urls import url
from apps_cenco.modulo_pagos import views

urlpatterns = [
    url(r'^detalle_pagos/(?P<idAlumno>\d+)$', views.detalle_pago, name='detalle_pagos'),
    url(r'^detalle_pagos/(?P<idAlumno>\d+)/(?P<cod_mensaje>\d+)$', views.detalle_pago, name='detalle_pagos_mensaje'),
    url(r'^modificar_pago/(?P<idAlumno>\d+)/(?P<idPago>\d+)$', views.modificar_pago, name='modificar_pago'),
    url(r'^eliminar_pago/(?P<idAlumno>\d+)/(?P<idPago>\d+)$', views.eliminar_pago, name='eliminar_pago'),
]