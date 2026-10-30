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


def contar_por(items, clave) -> dict:
    """
    Esta función cuenta los elementos de una lista por una clave.
    Args:
        items: list
        clave: function
    Returns:
        dict: diccionario con el conteo de los elementos
    """
    conteo = {}
    for item in items:
        k = clave(item)
        conteo[k] = conteo.get(k, 0) + 1
    return conteo


def agrupar_por(items, clave) -> dict:
    """
    Esta función agrupa los elementos de una lista por una clave.
    Args:
        items: list
        clave: function
    Returns:
        dict: diccionario con los elementos agrupados
    """
    agrupar = {}
    for item in items:
        k = clave(item)
        agrupar.setdefault(k, []).append(item)
    return agrupar
