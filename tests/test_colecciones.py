from practica.colecciones import sin_duplicados


def test_lista_sin_repetidos():
    assert sin_duplicados([3, 1, 3, 2, 1]) == [3, 1, 2]


def test_lista_vacia():
    assert sin_duplicados([]) == []


def test_item_no_es_lista():
    assert sin_duplicados(x % 3 for x in range(10)) == [0, 1, 2]


def test_misma_clave_de_texto():
    emails = ["Ana@x.es", "ana@x.es", "leo@x.es", "ANA@X.ES"]
    assert sin_duplicados(emails, clave=str.lower) == ["Ana@x.es", "leo@x.es"]


def test_misma_clave_dentro_diccionario():
    pedidos = [{"id": 1, "v": "a"}, {"id": 2, "v": "b"}, {"id": 1, "v": "c"}]
    assert sin_duplicados(pedidos, clave=lambda p: p["id"]) == [
        {"id": 1, "v": "a"},
        {"id": 2, "v": "b"},
    ]
