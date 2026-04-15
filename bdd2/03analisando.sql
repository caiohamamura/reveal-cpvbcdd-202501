SET max_parallel_workers_per_gather = 0;
SET jit = off;
DROP INDEX IF EXISTS idx_od_orderid;
DROP INDEX IF EXISTS idx_od_productid;
DROP INDEX IF EXISTS idx_o_employeeid;
DROP INDEX IF EXISTS idx_o_customerid;
-- Limpar o cache do PostgreSQL para um teste limpo (requer superuser)
-- DISCARD ALL;

-- Query complexa (Faturamento por Categoria e Ano)
-- ⚠️ Peça para os alunos observarem o "Execution Time" no final do resultado
EXPLAIN ANALYZE
SELECT 
    c.category_name,
    EXTRACT(YEAR FROM o.order_date)::int AS ano,
    SUM(od.quantity * od.unit_price * (1 - COALESCE(od.discount, 0))) AS receita_liquida,
    SUM(od.quantity) AS total_unidades,
    COUNT(DISTINCT o.order_id) AS qtd_pedidos
FROM order_details od
JOIN orders o ON od.order_id = o.order_id
JOIN products p ON od.product_id = p.product_id
JOIN categories c ON p.category_id = c.category_id
GROUP BY c.category_name, EXTRACT(YEAR FROM o.order_date)
ORDER BY ano DESC, receita_liquida DESC;


-- ============================================
-- PARTE 6: CENÁRIO 2 - O ALÍVIO (COM ÍNDICES)
-- ============================================
-- Criando índices nas chaves estrangeiras (Boa prática)
CREATE INDEX idx_od_orderid ON order_details(order_id);
CREATE INDEX idx_od_productid ON order_details(product_id);
CREATE INDEX idx_o_employeeid ON orders(employee_id);
CREATE INDEX idx_o_customerid ON orders(customer_id);

-- Rodar a MESMA query. 
-- ⚠️ Mostre que caiu significativamente, mas AINDA calcula as agregações (SUM, COUNT) em tempo real
EXPLAIN ANALYZE
SELECT 
    c.category_name,
    EXTRACT(YEAR FROM o.order_date)::int AS ano,
    SUM(od.quantity * od.unit_price * (1 - COALESCE(od.discount, 0))) AS receita_liquida,
    SUM(od.quantity) AS total_unidades,
    COUNT(DISTINCT o.order_id) AS qtd_pedidos
FROM order_details od
JOIN orders o ON od.order_id = o.order_id
JOIN products p ON od.product_id = p.product_id
JOIN categories c ON p.category_id = c.category_id
GROUP BY c.category_name, EXTRACT(YEAR FROM o.order_date)
ORDER BY ano DESC, receita_liquida DESC;


-- ============================================
-- PARTE 7: CENÁRIO 3 - A MÁGICA (MATERIALIZED VIEW)
-- ============================================
-- A View materializa o resultado em disco. Não há cálculo em tempo de execução!
DROP MATERIALIZED VIEW IF EXISTS mv_vendas_por_categoria_ano;

CREATE MATERIALIZED VIEW mv_vendas_por_categoria_ano AS
SELECT 
    c.category_id,
    c.category_name,
    EXTRACT(YEAR FROM o.order_date)::int AS ano,
    SUM(od.quantity * od.unit_price * (1 - COALESCE(od.discount, 0))) AS receita_liquida,
    SUM(od.quantity) AS total_unidades,
    COUNT(DISTINCT o.order_id) AS qtd_pedidos
FROM order_details od
JOIN orders o ON od.order_id = o.order_id
JOIN products p ON od.product_id = p.product_id
JOIN categories c ON p.category_id = c.category_id
GROUP BY c.category_id, c.category_name, EXTRACT(YEAR FROM o.order_date);

-- Opcional: Índice dentro da própria MV para filtros ultra-rápidos
CREATE INDEX idx_mv_ano ON mv_vendas_por_categoria_ano(ano);

-- ⚠️ A Query agora cai para perto de 0 milissegundos!
EXPLAIN ANALYZE
SELECT * FROM mv_vendas_por_categoria_ano 
ORDER BY ano DESC, receita_liquida DESC;

-- Bônus: Filtrando apenas 1 ano na MV (Use o índice que criamos na MV)
EXPLAIN ANALYZE
SELECT * FROM mv_vendas_por_categoria_ano WHERE ano = 2023;


-- ============================================
-- PARTE 8: A REALIDADE (O PROBLEMA DO REFRESH)
-- ============================================
-- Mostre aos alunos que MV não é "mágica de verdade", é "câmera fotográfica". 
-- Se os dados mudarem, a foto fica velha.

-- 1. Inserir 1 pedido novo na mão
INSERT INTO order_details (order_id, product_id, unit_price, quantity, discount)
VALUES (
    (SELECT MAX(order_id) FROM orders), 
    1, 
    100.00, 
    1000, 
    0
);

-- 2. Perguntar aos alunos: "Se eu rodar a MV agora, o novo pedido de 100k aparece?"
-- Resposta: NÃO.
SELECT * FROM mv_vendas_por_categoria_ano WHERE ano = EXTRACT(YEAR FROM CURRENT_DATE);

-- 3. Mostrar a tabela real para provar que o pedido existe (usando os índices que criamos)
SELECT 
    c.category_name,
    EXTRACT(YEAR FROM o.order_date)::int AS ano,
    SUM(od.quantity * od.unit_price * (1 - COALESCE(od.discount, 0))) AS receita_liquida
FROM order_details od
JOIN orders o ON od.order_id = o.order_id
JOIN products p ON od.product_id = p.product_id
JOIN categories c ON p.category_id = c.category_id
WHERE EXTRACT(YEAR FROM o.order_date) = EXTRACT(YEAR FROM CURRENT_DATE)
GROUP BY c.category_name, EXTRACT(YEAR FROM o.order_date);

-- 4. "Tirar uma nova foto" (REFRESH)
REFRESH MATERIALIZED VIEW mv_vendas_por_categoria_ano;

-- 5. Agora sim, a MV está atualizada e o valor de 100k aparece instantaneamente
SELECT * FROM mv_vendas_por_categoria_ano WHERE ano = EXTRACT(YEAR FROM CURRENT_DATE);