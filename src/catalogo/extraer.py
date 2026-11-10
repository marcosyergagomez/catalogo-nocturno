import csv

def leer_csv(ruta):
    with open(ruta, encoding="utf-8", newline="") as f:
        for fila in csv.DictReader(f):
            if not any((v or "").strip() for v in fila.values()):
                continue
            yield fila