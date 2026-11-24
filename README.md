# catalogo-nocturno

Carga nocturna de un catálogo de productos. Lee el export de Open Food Facts (TSV comprimido con gzip), se queda con España, valida cada fila y carga las válidas en Postgres. Si el mismo fichero se procesa otra vez, no duplica productos ni pisa una versión vieja sobre una más nueva. Las filas malas no se tiran: van a un JSONL de cuarentena, con el motivo.

Python 3.12 o superior. En ejecución hace falta `psycopg`. Para desarrollar, `pytest` y `ruff`.

## Qué hace una pasada

```text
TSV.gz
  → leer sin cargar el fichero entero
  → quedarse con countries_tags que contiene en:spain
  → validar
       ├─ rechazada → cuarentena.jsonl
       └─ válida → lotes → upsert en productos
```

La tabla `productos` tiene `code` (clave primaria), `product_name`, `brands`, `last_modified_t` y `nutriscore_grade`. El upsert actualiza solo cuando `last_modified_t` de la fila nueva es estrictamente mayor. Por eso la segunda pasada del mismo fichero escribe 0 filas.

`validar` rechaza un `code` vacío, un `product_name` vacío y una fecha que no sea un entero. `last_modified_t` se guarda como número.

## Qué está hecho

- `src/catalogo/extraer.py`: lectura del TSV.gz en streaming.
- `src/catalogo/validar.py`: reglas de arriba.
- `src/catalogo/cuarentena.py`: JSONL con la fila y el motivo.
- `src/catalogo/cargar.py`: upsert por lotes, una transacción por lote.
- `src/catalogo/pipeline.py`: une las piezas y devuelve métricas (`leidas`, `filtradas`, `validas`, `rechazadas`, `escritas`, `lotes`).
- `sql/001_crear_productos.sql` y Postgres 16 en `infra/docker-compose.yml`.
- Tests de extracción, validación, carga, idempotencia del pipeline y los ejercicios de `src/practica/`.

## Qué falta

El arranque (`python -m catalogo.pipeline`) todavía lleva el DSN escrito en el código. No hay comando `catalogo run`, ni logs al ejecutar, ni integración continua. La muestra real del export no se sube a Git: hay que colocarla en `data/raw/`.

## Cómo ejecutarlo

Desde la raíz del repositorio:

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -e ".[dev]"
docker compose -f infra/docker-compose.yml up -d
```

Hace falta un `data/raw/muestra.tsv.gz`. El bloque `__main__` de `src/catalogo/pipeline.py` llama a:

```text
pipeline("data/raw/muestra.tsv.gz", conn, "data/cuarentena.jsonl", 10)
```

La base local es `postgresql://aulanorte:aulanorte@localhost:5432/aulanorte`, usuario y base `aulanorte`, puerto 5432.

```bash
pytest
ruff check src tests
```

Los tests que hablan con Postgres se saltan si el contenedor no está encendido. El resto corre igual.
