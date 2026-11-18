import pytest
from pathlib import Path
from catalogo.extraer import leer_tsv_gz
import gzip

def test_leer_tsv_gz(tmp_path):
    ruta = tmp_path / "catalogo.tsv.gz"
    with gzip.open(ruta, mode="wt", encoding="utf-8", newline="") as f:
        f.write(
            "code\tproduct_name\tbrands\tlast_modified_t\tnutriscore_grade\n"
            "6549841\tTaza\tTazas Matias\t20260501\tB\n"
        )
    filas = list(leer_tsv_gz(ruta))
    assert len(filas) == 1
    assert filas[0]["code"] == "6549841"
    assert filas[0]["product_name"] == "Taza"
    assert filas[0]["brands"] == "Tazas Matias"
    assert filas[0]["last_modified_t"] == "20260501"
    assert filas[0]["nutriscore_grade"] == "B"