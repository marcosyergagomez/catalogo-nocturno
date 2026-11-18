from catalogo.validar import validar

BASE = {
    "code": "549841",
    "product_name": "Taza",
    "brands": "Tazas Matias",
    "last_modified_t": "20260501",
    "nutriscore_grade": "B",
}

def test_fila_valida():
    assert validar({**BASE, "code": "549841", "product_name": "Taza", "brands": "Tazas Matias", "last_modified_t": "20260501", "nutriscore_grade": "B"}) == (
        {"code": "549841", "product_name": "Taza", "brands": "Tazas Matias", "last_modified_t": 20260501, "nutriscore_grade": "B"},
        None,
    )

def test_code_vacio():
    assert validar({**BASE, "code": "  "}) == (None, "code vacío")

def test_last_modified_t_malo():
    assert validar({**BASE, "last_modified_t": "9.99"}) == (None, "La fecha no es entera")