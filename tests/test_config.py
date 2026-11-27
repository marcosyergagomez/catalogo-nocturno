import pytest
from catalogo.config import cargar_config, Config
from pathlib import Path

def test_cargar_config():
    assert cargar_config({"CATALOGO_DSN": "postgresql://x"}) == Config(dsn="postgresql://x", nivel_log="INFO")
    assert cargar_config({
        "CATALOGO_DSN": "postgresql://x", "CATALOGO_TAMANO_LOTE": "50", "CATALOGO_CUARENTENA": "/tmp/q",
    }) == Config(dsn="postgresql://x", tamano_lote=50, carpeta_cuarentena=Path("/tmp/q"), nivel_log="INFO")
    for malo in [{}, {"CATALOGO_DSN": "  "}, {"CATALOGO_DSN": "x", "CATALOGO_TAMANO_LOTE": "0"},
                 {"CATALOGO_DSN": "x", "CATALOGO_TAMANO_LOTE": "diez"}, {"CATALOGO_LOG_NIVEL": "INVALIDO"}]:
        try:
            cargar_config(malo)
        except ValueError:
            pass
        else:
            raise AssertionError(f"{malo} tenía que lanzar ValueError.")