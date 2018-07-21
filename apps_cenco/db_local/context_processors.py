from apps_cenco.db_local.models import FooterINFO


def agregar_a_context(request):
    contenido_footer = FooterINFO.objects.get(codigo=1)
    return {'contenido_footer': contenido_footer}
