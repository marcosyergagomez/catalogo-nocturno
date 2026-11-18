"""Pipeline OFF de punta a punta: métricas e idempotencia contra Postgres."""

import gzip
import os
from pathlib import Path

import psycopg
import pytest

from catalogo.pipeline import Metricas, pipeline

DSN = os.environ.get(
    "CATALOGO_TEST_DSN",
    "postgresql://aulanorte:aulanorte@localhost:5432/aulanorte",
)
SQL_CREAR = Path(__file__).resolve().parents[1] / "sql" / "001_crear_productos.sql"

CABECERA = (
    "code\tproduct_name\tbrands\tcountries_tags\tlast_modified_t\tnutriscore_grade\n"
)
# 2 España válidas, 1 filtrada (no España), 1 rechazada (nombre vacío)
MUESTRA = CABECERA + (
    "8410000000001\tLeche entera\tGranja\ten:spain\t1774000000\tb\n"
    "8410000000002\tYogur\tLácteos\ten:spain,en:france\t1774000001\ta\n"
    "8410000000003\tGalletas\tDulces\ten:france\t1774000002\tc\n"
    "8410000000004\t\tSin Nombre\ten:spain\t1774000003\tb\n"
)


@pytest.fixture
def conn():
    try:
        connection = psycopg.connect(DSN, autocommit=True)
    except psycopg.OperationalError as error:
        pytest.skip(f"Postgres no está disponible ({error}). ¿docker start aulanorte-pg?")

    connection.execute("drop table if exists productos")
    connection.execute(SQL_CREAR.read_text(encoding="utf-8"))
    yield connection
    connection.close()


@pytest.fixture
def muestra_gz(tmp_path):
    ruta = tmp_path / "muestra.tsv.gz"
    with gzip.open(ruta, mode="wt", encoding="utf-8", newline="") as f:
        f.write(MUESTRA)
    return ruta


def test_pipeline_primera_carga_y_idempotencia(conn, muestra_gz, tmp_path):
    ruta_q = tmp_path / "cuarentena.jsonl"

    primera = pipeline(muestra_gz, conn, ruta_q, tamano_lote=2)
    assert primera == Metricas(
        leidas=4,
        validas=2,
        rechazadas=1,
        filtradas=1,
        escritas=2,
        lotes=1,
    )

    filas = conn.execute(
        "select code, product_name from productos order by code"
    ).fetchall()
    assert filas == [
        ("8410000000001", "Leche entera"),
        ("8410000000002", "Yogur"),
    ]

    motivos = [
        line
        for line in ruta_q.read_text(encoding="utf-8").splitlines()
        if line
    ]
    assert len(motivos) == 1
    assert "product_name vacío" in motivos[0]

    # Misma muestra otra vez: upsert con la misma versión → 0 escritas
    segunda = pipeline(muestra_gz, conn, ruta_q, tamano_lote=2)
    assert segunda.escritas == 0
    assert segunda.validas == 2
    assert segunda.leidas == 4
