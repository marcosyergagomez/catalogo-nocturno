from itertools import islice


def _generador_interno(items, tamano):
    iterador = iter(items)
    while lote := list(islice(iterador, tamano)):
        yield lote


def lotes(items, tamano):
    if not isinstance(tamano, int) or isinstance(tamano, bool) or tamano <= 0:
        raise ValueError("El tamaño debe ser un numero entero positivo")
    return _generador_interno(items, tamano)
