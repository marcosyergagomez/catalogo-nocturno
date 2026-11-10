from typing import Mapping, Any

def validar(fila: Mapping[str, Any]) -> tuple[dict | None, str | None]:
    sku = (fila.get("sku") or "").strip()
    if not sku:
        return (None,"sku vacío")
    nombre = (fila.get("nombre") or "").strip()
    if not nombre:
        return(None, "nombre vacío")
    precio_cents = fila.get("precio_cents")
    if precio_cents is None:
        return (None, "precio no entero")
    if not precio_cents.strip().isdigit():
        return (None, "precio no entero")
    actualizado_en = (fila.get("actualizado_en") or "").strip()
    if not actualizado_en:
        return(None, "fecha vacía")
    limpio = {
        "sku": fila.get("sku").strip().upper(),
        "nombre": fila.get("nombre").strip(),
        "precio_cents": int(fila.get("precio_cents").strip()),
        "actualizado_en": fila.get("actualizado_en").strip()
    }
    return (limpio,None)

    