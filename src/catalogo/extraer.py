import csv
import gzip

def leer_tsv_gz(ruta):
    with gzip.open(ruta, mode="rt", encoding="utf-8", newline="") as f:
        for fila in csv.DictReader(f, delimiter="\t", quoting=csv.QUOTE_NONE):
            if not any((v or "").strip() for v in fila.values()):
                continue
            yield fila