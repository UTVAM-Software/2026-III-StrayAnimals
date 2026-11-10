from .security import es_solo_lectura


def tipo_acceso(request):
    usuario = request.user
    if not usuario.is_authenticated:
        etiqueta = None
        lectura = False
    elif usuario.is_superuser:
        etiqueta = "Superusuario"
        lectura = False
    elif es_solo_lectura(usuario):
        etiqueta = "Solo lectura"
        lectura = True
    else:
        etiqueta = "Usuario"
        lectura = False
    return {"tipo_acceso": etiqueta, "acceso_solo_lectura": lectura}
