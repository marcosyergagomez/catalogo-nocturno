import json
from typing import Iterable, Mapping, Any
from pathlib import Path

def escribir_cuarentena(rechazados: Iterable[tuple[Mapping[str, Any], str]], ruta: Path) -> int:
    with open(ruta, "a", encoding="utf-8") as f:
        cont = 0
        for rechazo in rechazados:
            f.write(json.dumps({"motivo": rechazo[1], "fila": rechazo[0]}, ensure_ascii=False,)+ "\n")
            cont += 1
    return cont