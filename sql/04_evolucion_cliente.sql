-- ¿Cuál ha sido la evolución de los pedidos pagados de un cliente?
select id, total_cents,
    sum(total_cents) over w as acumulado,
    total_cents - lag(total_cents) over w as diferencia
from pedidos
where estado = 'pagado' and cliente_id = $1
window w as (order by creado_en asc, id)