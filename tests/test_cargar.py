"""Tests de cargar_lote contra el Postgres del compose (aulanorte)."""

import os
from pathlib import Path

import psycopg
import pytest

from catalogo.cargar import cargar_lote

# Mismo usuario/base/password que infra/docker-compose.yml
DSN = os.environ.get(
    "CATALOGO_TEST_DSN",
    "postgresql://aulanorte:aulanorte@localhost:5432/aulanorte",
)
SQL_CREAR = Path(__file__).resolve().parents[1] / "sql" / "001_crear_productos.sql"

PRODUCTO = {
    "code": "8410000000001",
    "product_name": "Leche entera",
    "brands": "Granja",
    "last_modified_t": 1_774_000_000,
    "nutriscore_grade": "b",
}


@pytest.fixture
def conn():
    """Conexión limpia: borra y crea productos, luego cierra al acabar el test."""
    try:
        connection = psycopg.connect(DSN, autocommit=True)
    except psycopg.OperationalError as error:
        pytest.skip(f"Postgres no está disponible ({error}). ¿docker start aulanorte-pg?")

    connection.execute("drop table if exists productos")
    connection.execute(SQL_CREAR.read_text(encoding="utf-8"))
    yield connection
    connection.close()


def test_primera_carga_escribe_una_fila(conn):
    escritas = cargar_lote(conn, [PRODUCTO])
    assert escritas == 1

    fila = conn.execute(
        "select code, product_name, brands, last_modified_t, nutriscore_grade "
        "from productos where code = %s",
        (PRODUCTO["code"],),
    ).fetchone()
    assert fila == (
        PRODUCTO["code"],
        PRODUCTO["product_name"],
        PRODUCTO["brands"],
        PRODUCTO["last_modified_t"],
        PRODUCTO["nutriscore_grade"],
    )


def test_segunda_carga_del_mismo_lote_escribe_cero(conn):
    assert cargar_lote(conn, [PRODUCTO]) == 1
    # Misma fila otra vez: el WHERE de versión no actualiza → 0 escritas
    assert cargar_lote(conn, [PRODUCTO]) == 0


def test_version_vieja_no_pisa_y_nueva_si(conn):
    assert cargar_lote(conn, [PRODUCTO]) == 1

    viejo = {**PRODUCTO, "product_name": "Leche vieja", "last_modified_t": 1_770_000_000}
    assert cargar_lote(conn, [viejo]) == 0
    nombre = conn.execute(
        "select product_name from productos where code = %s",
        (PRODUCTO["code"],),
    ).fetchone()[0]
    assert nombre == "Leche entera"

    nuevo = {**PRODUCTO, "product_name": "Leche nueva", "last_modified_t": 1_780_000_000}
    assert cargar_lote(conn, [nuevo]) == 1
    nombre = conn.execute(
        "select product_name from productos where code = %s",
        (PRODUCTO["code"],),
    ).fetchone()[0]
    assert nombre == "Leche nueva"
