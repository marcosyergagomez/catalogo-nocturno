import argparse
import json
import logging
import os
import sys
from dataclasses import asdict
from datetime import date
from pathlib import Path

import psycopg

from catalogo.config import cargar_config
from catalogo.logs import configurar_logs
from catalogo.pipeline import pipeline

log = logging.getLogger("catalogo")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="catalogo")
    sub = parser.add_subparsers(dest="comando", required=True)
    run = sub.add_parser("run", help="carga un fichero del proveedor")
    run.add_argument("--fichero", required=True)
    run.add_argument("--fecha", required=True, type=date.fromisoformat)
    args = parser.parse_args(argv)

    try:
        config = cargar_config(os.environ)
    except ValueError as error:
        logging.basicConfig(level=logging.ERROR, force=True)
        log.error("%s", error)
        return 1

    configurar_logs(config)
    ruta = Path(args.fichero)
    if not ruta.is_file():
        log.error("No existe el fichero %s", ruta)
        return 1

    ruta_cuarentena = config.carpeta_cuarentena / "cuarentena.jsonl"
    try:
        ruta_cuarentena.parent.mkdir(parents=True, exist_ok=True)
        with psycopg.connect(config.dsn, autocommit=True) as conn:
            metricas = pipeline(ruta, conn, ruta_cuarentena, config.tamano_lote)
    except (OSError, psycopg.Error) as error:
        log.error("%s", error)
        return 1

    print(json.dumps(asdict(metricas), ensure_ascii=False), flush=True)
    log.info(
        "%s",
        json.dumps(
            {
                "evento": "carga_terminada",
                "fichero": str(ruta),
                "fecha": args.fecha.isoformat(),
                **asdict(metricas),
            },
            ensure_ascii=False,
        ),
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
