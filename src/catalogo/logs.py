import logging

from catalogo.config import Config


def configurar_logs(config: Config) -> None:
    logging.basicConfig(level=config.nivel_log, force=True)