import os
import logging
from catalogo.extraer import leer_tsv_gz
from catalogo.validar import validar
from catalogo.cuarentena import escribir_cuarentena
from catalogo.cargar import cargar_lote
from practica.lotes import lotes
from dataclasses import dataclass
from catalogo.config import cargar_config
from catalogo.logs import configurar_logs
import time
import psycopg


@dataclass
class Metricas:
    leidas: int = 0
    validas: int = 0
    rechazadas: int = 0
    escritas: int = 0
    lotes: int = 0
    filtradas: int = 0
    duracion_s: float = 0


def pipeline(ruta,conn,ruta_cuarentena, tamano_lote):
    metricas = Metricas()
    inicio = time.perf_counter()
    filas = leer_tsv_gz(ruta)
    validas = []
    rechazadas = []

    for fila in filas:
        metricas.leidas += 1
        if not "en:spain" in fila["countries_tags"].split(","):
            metricas.filtradas += 1
            continue
        fila_validada = validar(fila)
        if fila_validada[1] is not None:
            rechazadas.append((fila, fila_validada[1]))
            metricas.rechazadas += 1
        else:
            metricas.validas += 1
            validas.append(fila_validada[0])
    lotes_validos = lotes(validas,tamano_lote)
    escribir_cuarentena(rechazadas, ruta_cuarentena)
    for lote in lotes_validos:
        metricas.lotes += 1
        cargados = cargar_lote(conn, lote)
        metricas.escritas += cargados

    segundos = time.perf_counter() - inicio
    metricas.duracion_s = segundos
    return metricas

if __name__ == "__main__":
    config = cargar_config(os.environ)
    configurar_logs(config)
    with psycopg.connect(config.dsn) as conn:
        pipeline("data/raw/muestra.tsv.gz", conn, config.carpeta_cuarentena / "cuarentena.jsonl", config.tamano_lote)