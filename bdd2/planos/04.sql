SELECT e.employee_id,
       e.first_name || ' ' || e.last_name AS nome,
       e.title AS cargo,
       COUNT(DISTINCT o.order_id) AS total_pedidos,
       SUM(od.quantity * od.unit_price) AS valor_total_vendido,
       ROUND(AVG(od.quantity * od.unit_price)::numeric, 2) AS ticket_medio
FROM employees e
LEFT JOIN orders o ON e.employee_id = o.employee_id
LEFT JOIN order_details od ON o.order_id = od.order_id
GROUP BY e.employee_id, e.first_name, e.last_name, e.title;