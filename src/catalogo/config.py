from typing import Mapping
from pathlib import Path
from dataclasses import dataclass,field

@dataclass(frozen=True)
class Config:
    dsn: str
    tamano_lote: int = 500
    carpeta_cuarentena: Path = field(default_factory=lambda: Path("cuarentena"))
    nivel_log: str = "INFO"

def cargar_config(entorno: Mapping[str, str]) -> Config:
    dsn = entorno.get("CATALOGO_DSN", "").strip()
    if not dsn:
        raise ValueError("Falta CATALOGO_DSN")
    texto_lote = entorno.get("CATALOGO_TAMANO_LOTE", "500").strip()
    if not texto_lote.isdigit() or int(texto_lote) <= 0:
        raise ValueError("CATALOGO_TAMANO_LOTE tiene que ser un entero positivo")
    carpeta = entorno.get("CATALOGO_CUARENTENA", "cuarentena").strip()
    niveles = {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}
    nivel_log = entorno.get("CATALOGO_LOG_NIVEL", "INFO").strip().upper()
    if nivel_log not in niveles:
        raise ValueError("CATALOGO_LOG_NIVEL no es un nivel de log")
    return Config(
        dsn=dsn,
        tamano_lote=int(texto_lote),
        carpeta_cuarentena=Path(carpeta),
        nivel_log=nivel_log,
    )

