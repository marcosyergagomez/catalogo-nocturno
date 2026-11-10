import pytest
from pathlib import Path
from catalogo.extraer import leer_csv

def test_leer_csv(tmp_path):
    ruta = tmp_path / "catalogo.csv"
    ruta.write_text(
        "sku,nombre,precio_cents,actualizado_en\n"
        "A1,Taza,1200,2026-05-01\n"
        ",,,\n"  # fila vacía → leer_csv la salta
        "B2,\"Vaso, pack\",2400,2026-05-01\n",
        encoding="utf-8",
    )
    filas = list(leer_csv(ruta))
    assert len(filas) == 2
    assert filas[0]["sku"] == "A1"
    assert filas[1]["nombre"] == "Vaso, pack"  # todo sale como str