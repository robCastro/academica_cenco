from django.conf.urls import url
from apps_cenco.modulo_pagos import views

urlpatterns = [
    url(r'^detalle_pagos/(?P<idAlumno>\d+)$', views.detalle_pago, name='detalle_pagos'),
]