from practica.limpieza import limpiar_clientes


def test_payload_roto_devuelve_lista_vacia():
    assert limpiar_clientes(None) == []
    assert limpiar_clientes({"data": "roto"}) == []


def test_payload_correcto_devuelve_clientes_limpios():
    payload = {
        "page": 1,
        "data": [
            {
                "id": 7,
                "nombre": "  Ana ",
                "email": " ANA@Correo.es ",
                "etiquetas": [" vip ", "", 3, "nuevo"],
            },
            {"id": True, "nombre": "Bot"},
            {"id": 0, "nombre": "Cero"},
            {"id": "8", "nombre": "Texto"},
            {"id": 9, "nombre": "   "},
            {"id": 10, "nombre": "Leo", "email": "sin-arroba", "etiquetas": "vip"},
            "esto no es un registro",
            {"id": 11, "nombre": "Mar", "email": None},
        ],
    }
    assert limpiar_clientes(payload) == [
        {"id": 7, "nombre": "Ana", "email": "ana@correo.es", "etiquetas": ["vip", "nuevo"]},
        {"id": 10, "nombre": "Leo", "email": None, "etiquetas": []},
        {"id": 11, "nombre": "Mar", "email": None, "etiquetas": []},
    ]


def test_no_modifica_diccionario_original():
    original = {"id": 1, "nombre": " X "}
    limpiar_clientes({"data": [original]})
    assert original == {"id": 1, "nombre": " X "}
