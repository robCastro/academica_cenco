# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from django.http import HttpResponseForbidden, HttpResponse, HttpResponseServerError

# Create your views here.
from apps_cenco.db_local.forms import DetalleFooterForm
from apps_cenco.db_local.models import FooterINFO

import sys

reload(sys)
sys.setdefaultencoding('utf-8')


@login_required
def editar_configuracion(request):
    if request.user.groups.filter(name="Director").exists():
        try:
            footer = FooterINFO.objects.get(codigo=1)
        except ObjectDoesNotExist:
            return HttpResponseServerError('Error al consultar la base de datos')
        form_footer = DetalleFooterForm(instance=footer)
        context = {
            'form_footer': form_footer,
        }
        return render(request, 'settings/director_configuracion.html', context)
    else:
        return HttpResponseForbidden('No tiene permiso para ver este contenido')


@login_required
def editar_footer(request):
    if request.user.groups.filter(name="Director").exists() and request.method == 'POST':
        try:
            footer = FooterINFO.objects.get(codigo=1)
            tel = footer.telefono
            mail = footer.correo
            dire = footer.direccion

            form = DetalleFooterForm(request.POST, instance=footer)
            if form.is_valid():
                footer_aux = form.save(commit=False)
                if tel == footer_aux.telefono and \
                        mail == footer_aux.correo and \
                        dire == footer_aux.direccion:
                    return HttpResponse('No se ingresaron cambios', status=500)
                form.save()
                return HttpResponse('Datos del footer Guardados correctamente.', status=200)
            else:
                return HttpResponse('Datos del footer ingresados de forma incorrecta', status=500)
        except ObjectDoesNotExist:
            return HttpResponse('Error interno del servidor. No se encuentran datos del footer', status=500)
    else:
        return HttpResponseForbidden('No tiene permiso para ver este contenido')
