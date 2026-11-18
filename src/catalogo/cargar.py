import psycopg
from collections.abc import Iterable, Iterator, Mapping
from contextlib import contextmanager
from datetime import UTC, datetime, timedelta
from typing import Any

def cargar_lote(conn,lote):
    sql="""
    insert into productos values (%(code)s, %(product_name)s, %(brands)s, %(last_modified_t)s, %(nutriscore_grade)s) on conflict (code) do update set product_name = excluded.product_name,
    brands = excluded.brands,
    last_modified_t = excluded.last_modified_t,
    nutriscore_grade = excluded.nutriscore_grade
    where excluded.last_modified_t > productos.last_modified_t
    """
    with conn.transaction(), conn.cursor() as cur:
        cur.executemany(sql,lote)
        return cur.rowcount
    
