-- ¿Cuántos clientes no han hecho ningún pedido pagado?
select c.id, c.nombre
from clientes c
left join pedidos p on p.cliente_id = c.id and p.estado = 'pagado'
where p.id is null
order by c.id