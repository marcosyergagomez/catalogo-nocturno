import pytest

from practica.colecciones import agrupar_por, contar_por, sin_duplicados


@pytest.mark.parametrize(
    "lista, resultado",
    [([3, 1, 3, 2, 1], [3, 1, 2]), ([], []), ([x % 3 for x in range(10)], [0, 1, 2])],
)
def test_lista_sin_repetidos(lista, resultado):
    assert sin_duplicados(lista) == resultado


def test_misma_clave_de_texto():
    emails = ["Ana@x.es", "ana@x.es", "leo@x.es", "ANA@X.ES"]
    assert sin_duplicados(emails, clave=str.lower) == ["Ana@x.es", "leo@x.es"]


def test_misma_clave_dentro_diccionario():
    pedidos = [{"id": 1, "v": "a"}, {"id": 2, "v": "b"}, {"id": 1, "v": "c"}]
    assert sin_duplicados(pedidos, clave=lambda p: p["id"]) == [
        {"id": 1, "v": "a"},
        {"id": 2, "v": "b"},
    ]


ventas = [
    {"ciudad": "Madrid", "importe": 10},
    {"ciudad": "Bilbao", "importe": 5},
    {"ciudad": "Madrid", "importe": 7},
]


@pytest.mark.parametrize(
    "entrada, clave, resultado",
    [
        (ventas, lambda v: v["ciudad"], {"Madrid": 2, "Bilbao": 1}),
        ([], len, {}),
        (["ab", "c", "de"], len, {2: 2, 1: 1}),
    ],
)
def test_contar_por(entrada, clave, resultado):
    assert contar_por(entrada, clave) == resultado


@pytest.mark.parametrize(
    "entrada, clave, resultado",
    [(ventas, lambda v: v["ciudad"], {"Madrid": [ventas[0], ventas[2]], "Bilbao": [ventas[1]]})],
)
def test_agrupar_por(entrada, clave, resultado):
    assert agrupar_por(entrada, clave) == resultado
