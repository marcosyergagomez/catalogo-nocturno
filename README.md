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
- `src/catalogo/pipeline.py`: une las piezas y devuelve métricas (`leidas`, `filtradas`, `validas`, `rechazadas`, `escritas`, `lotes`, `duracion_s`).
- `src/catalogo/config.py`: `Config` y `cargar_config` leen el entorno y fallan al arrancar si falta el DSN.
- `src/catalogo/logs.py`: nivel de log desde la configuración.
- `src/catalogo/cli.py`: `catalogo run --fichero ... --fecha ...`. Métricas en JSON por stdout, logs por stderr.
- `sql/001_crear_productos.sql` y Postgres 16 en `infra/docker-compose.yml`.
- Tests de extracción, validación, carga, idempotencia del pipeline, configuración, logs, la CLI y los ejercicios de `src/practica/`.

## Qué falta

Integración continua. La muestra real del export no se sube a Git: hay que colocarla en `data/raw/`. `--fecha` se valida y queda en el log; todavía no filtra filas.

## Cómo ejecutarlo

Desde la raíz del repositorio:

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -e ".[dev]"
docker compose -f infra/docker-compose.yml up -d
```

Hace falta un `data/raw/muestra.tsv.gz`. La base local es `postgresql://aulanorte:aulanorte@localhost:5432/aulanorte`, usuario y base `aulanorte`, puerto 5432. Copia `.env.example` a `.env` (no se sube a Git) o exporta las variables en la shell:

```powershell
$env:CATALOGO_DSN = "postgresql://aulanorte:aulanorte@localhost:5432/aulanorte"
catalogo run --fichero data/raw/muestra.tsv.gz --fecha 2026-11-27
```

La salida estándar es un JSON con las métricas. Los logs van a la salida de error. Sin `CATALOGO_DSN` el proceso sale con código 1. Si falta `--fecha`, argparse sale con código 2. La segunda pasada del mismo fichero deja `escritas` en 0.

```bash
pytest
ruff check src tests
```

Los tests que hablan con Postgres se saltan si el contenedor no está encendido. El resto corre igual.
