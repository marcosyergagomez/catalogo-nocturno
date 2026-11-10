import json
from catalogo.cuarentena import escribir_cuarentena

def test_escribir_cuarentena(tmp_path):
    ruta = tmp_path / "cuarentena.jsonl"
    n = escribir_cuarentena(
        [({"sku": "C3", "nombre": ""}, "nombre vacío")],
        ruta,
    )
    n += escribir_cuarentena(
        [({"sku": "D4"}, "precio no entero")],
        ruta,
    )
    lineas = ruta.read_text(encoding="utf-8").splitlines()
    assert n == 2
    assert len(lineas) == 2  # la segunda llamada AÑADE
    assert json.loads(lineas[0]) == {
        "motivo": "nombre vacío",
        "fila": {"sku": "C3", "nombre": ""},
    }