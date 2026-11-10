from catalogo.validar import validar

BASE = {
    "sku": "A1",
    "nombre": "Taza",
    "precio_cents": "1200",
    "actualizado_en": "2026-05-01",
}

def test_fila_valida():
    assert validar({**BASE, "sku": " a1 ", "nombre": " Taza "}) == (
        {"sku": "A1", "nombre": "Taza", "precio_cents": 1200, "actualizado_en": "2026-05-01"},
        None,
    )

def test_sku_vacio():
    assert validar({**BASE, "sku": "  "}) == (None, "sku vacío")

def test_precio_malo():
    assert validar({**BASE, "precio_cents": "9.99"}) == (None, "precio no entero")