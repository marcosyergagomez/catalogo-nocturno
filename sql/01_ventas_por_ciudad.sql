-- ¿Cuánto se ha cobrado por ciudad en un periodo, solo en ciudades
-- con al menos N pedidos pagados? Rango semiabierto [desde, hasta).
-- $1 desde, $2 hasta, $3 minimo_pedidos
select c.ciudad, count(*), coalesce(sum(p.total_cents), 0) as total
from clientes c
join pedidos p on p.cliente_id = c.id
where p.estado = 'pagado'
  and p.creado_en >= $1
  and p.creado_en < $2
group by c.ciudad
having count(*) >= $3
order by total desc, c.ciudad;