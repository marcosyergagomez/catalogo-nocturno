"""Códigos de salida de `catalogo run`: 0 métricas, 1 config, 2 argparse."""

import gzip
import json
import os
from pathlib import Path

import psycopg
import pytest

from catalogo.cli import main

DSN = os.environ.get(
    "CATALOGO_TEST_DSN",
    "postgresql://aulanorte:aulanorte@localhost:5432/aulanorte",
)
SQL_CREAR = Path(__file__).resolve().parents[1] / "sql" / "001_crear_productos.sql"

CABECERA = (
    "code\tproduct_name\tbrands\tcountries_tags\tlast_modified_t\tnutriscore_grade\n"
)
MUESTRA = CABECERA + (
    "8410000000001\tLeche entera\tGranja\ten:spain\t1774000000\tb\n"
    "8410000000002\tYogur\tLácteos\ten:spain,en:france\t1774000001\ta\n"
    "8410000000003\tGalletas\tDulces\ten:france\t1774000002\tc\n"
    "8410000000004\t\tSin Nombre\ten:spain\t1774000003\tb\n"
)


def _tabla_lista():
    try:
        conexion = psycopg.connect(DSN, autocommit=True)
    except psycopg.OperationalError as error:
        pytest.skip(f"Postgres no está disponible ({error}). ¿docker start aulanorte-pg?")
    conexion.execute("drop table if exists productos")
    conexion.execute(SQL_CREAR.read_text(encoding="utf-8"))
    conexion.close()


@pytest.fixture
def muestra_gz(tmp_path):
    ruta = tmp_path / "muestra.tsv.gz"
    with gzip.open(ruta, mode="wt", encoding="utf-8", newline="") as fichero:
        fichero.write(MUESTRA)
    return ruta


def test_run_imprime_metricas_json_y_la_segunda_vez_escribe_cero(
    monkeypatch, capsys, tmp_path, muestra_gz
):
    _tabla_lista()
    monkeypatch.setenv("CATALOGO_DSN", DSN)
    monkeypatch.setenv("CATALOGO_TAMANO_LOTE", "2")
    monkeypatch.setenv("CATALOGO_CUARENTENA", str(tmp_path / "q"))
    argv = ["run", "--fichero", str(muestra_gz), "--fecha", "2026-11-27"]

    assert main(argv) == 0
    primera = json.loads(capsys.readouterr().out)
    assert primera["leidas"] == 4
    assert primera["validas"] == 2
    assert primera["rechazadas"] == 1
    assert primera["filtradas"] == 1
    assert primera["escritas"] == 2
    assert primera["lotes"] == 1
    assert primera["duracion_s"] > 0

    assert main(argv) == 0
    capturado = capsys.readouterr()
    segunda = json.loads(capturado.out)
    assert segunda["escritas"] == 0
    assert segunda["leidas"] == 4
    assert "carga_terminada" in capturado.err
    assert "carga_terminada" not in capturado.out


def test_sin_dsn_falla_al_arrancar_con_codigo_1(monkeypatch, capsys):
    monkeypatch.delenv("CATALOGO_DSN", raising=False)

    def no_conectar(*args, **kwargs):
        raise AssertionError("Sin DSN no tenía que abrir la conexión.")

    monkeypatch.setattr(psycopg, "connect", no_conectar)
    codigo = main(["run", "--fichero", "no-existe.tsv.gz", "--fecha", "2026-11-27"])
    capturado = capsys.readouterr()

    assert codigo == 1
    assert capturado.out.strip() == ""
    assert "CATALOGO_DSN" in capturado.err


def test_sin_fecha_argparse_sale_con_codigo_2(capsys):
    with pytest.raises(SystemExit) as exc:
        main(["run", "--fichero", "x.tsv.gz"])
    capturado = capsys.readouterr()
    assert exc.value.code == 2
    assert "--fecha" in capturado.err
