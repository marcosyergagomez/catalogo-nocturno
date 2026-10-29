from collections.abc import Callable, Iterable
from typing import Any


def sin_duplicados(items: Iterable[Any], clave: Callable | None = None) -> list:
    """
    Esta función elimina duplicados de una lista.
    Args:
        items: list
        clave: function
    Returns:
        list: lista sin duplicados
    """
    vistos = set()
    deduplicados = []
    for item in items:
        identidad = item if clave is None else clave(item)
        if identidad in vistos:
            continue
        vistos.add(identidad)
        deduplicados.append(item)

    return deduplicados
