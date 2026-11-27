import logging

from catalogo.config import Config, cargar_config
from catalogo.logs import configurar_logs


def test_sin_variable_el_nivel_es_info():
    config = cargar_config({"CATALOGO_DSN": "postgresql://x"})
    assert config.nivel_log == "INFO"


def test_lee_el_nivel_del_entorno():
    config = cargar_config({
        "CATALOGO_DSN": "postgresql://x",
        "CATALOGO_LOG_NIVEL": "warning",
    })
    assert config.nivel_log == "WARNING"


def test_configurar_logs_cambia_el_nivel():
    configurar_logs(Config(dsn="x", nivel_log="WARNING"))
    assert logging.getLogger().level == logging.WARNING

    configurar_logs(Config(dsn="x", nivel_log="INFO"))
    assert logging.getLogger().level == logging.INFO