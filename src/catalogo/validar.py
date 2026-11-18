from typing import Mapping, Any

def validar(fila: Mapping[str, Any]) -> tuple[dict | None, str | None]:
    code = (fila.get("code") or "").strip()
    if not code:
        return (None,"code vacío")
    product_name = (fila.get("product_name") or "").strip()
    if not product_name:
        return(None, "product_name vacío")
    brands = (fila.get("brands") or "").strip()
    last_modified_t = fila.get("last_modified_t")
    if last_modified_t is None:
        return (None, "La fecha esta vacia")
    if not last_modified_t.strip().isdigit():
        return (None, "La fecha no es entera")
    nutriscore_grade = (fila.get("nutriscore_grade") or "").strip()
    limpio = {
        "code": code,
        "product_name": product_name,
        "brands": brands,
        "last_modified_t": int(fila.get("last_modified_t").strip()),
        "nutriscore_grade": nutriscore_grade
    }
    return (limpio,None)

    