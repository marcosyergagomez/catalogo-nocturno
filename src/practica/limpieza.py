def _es_entero(numero) -> bool:
    if isinstance(numero, int) and not isinstance(numero, bool) and numero > 0:
        return True
    return False


def _texto_limpio(texto) -> str:
    return texto.lower().strip()


def limpiar_clientes(payload) -> list:
    """
    Esta función limpia los datos de los clientes.
    Args:
        payload: dict
    Returns:
        list: lista de clientes limpios
    """
    clientes_limpios = []

    if not isinstance(payload, dict) or not isinstance(payload.get("data"), list):
        return clientes_limpios

    datos = payload.get("data")
    for dato in datos:
        if not isinstance(dato, dict):
            continue
        if not _es_entero(dato.get("id")):
            continue
        nombre = dato.get("nombre")
        if not isinstance(nombre, str) or not nombre.strip():
            continue
        else:
            nombre_limpio = nombre.strip()

        email = dato.get("email")
        email_limpio = None
        if isinstance(email, str):
            if "@" in _texto_limpio(email):
                email_limpio = _texto_limpio(email)
        etiquetas_limpias = []
        if isinstance(dato.get("etiquetas"), list):
            for etiqueta in dato.get("etiquetas"):
                if isinstance(etiqueta, str) and etiqueta.strip():
                    etiquetas_limpias.append(_texto_limpio(etiqueta))
        ficha = {
            "id": dato.get("id"),
            "nombre": nombre_limpio,
            "email": email_limpio,
            "etiquetas": etiquetas_limpias,
        }
        clientes_limpios.append(ficha)
    return clientes_limpios
