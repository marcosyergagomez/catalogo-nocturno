-- ¿Cuál es el último pedido pagado de cada cliente?
with ordenados as (
select c.id, p.id as pedido_id, p.creado_en,
    row_number() over(partition by c.id order by p.creado_en desc, p.id desc) as orden
from clientes c
join pedidos p on p.cliente_id = c.id
where p.estado = 'pagado'
order by c.id
)
select o.id, o.pedido_id, o.creado_en
from ordenados o
where orden = 1
order by o.id