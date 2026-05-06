-- ============================================
-- SCRIPT: GERAÇÃO DE DADOS SINTÉTICOS (ESCALA GRANDE)
-- Banco: Northwind (PostgreSQL)
-- Objetivo: Criar volume para demonstrar a dor
--           de consultas lentas e a "mágica" 
--           de ÍNDICES e MATERIALIZED VIEWS
-- ============================================

-- ============================================
-- PARTE 0: PREPARAÇÃO E LIMPEZA
-- ============================================
-- Alterar tipo de order_id para suportar volume
ALTER TABLE order_details ALTER COLUMN order_id TYPE integer USING order_id::integer;
ALTER TABLE orders ALTER COLUMN order_id TYPE integer USING order_id::integer;
-- Alterar tipo de customer_id para suportar prefixo SYN
ALTER TABLE customers ALTER COLUMN customer_id TYPE varchar(8);
ALTER TABLE orders ALTER COLUMN customer_id TYPE varchar(8);

-- Limpar dados sintéticos antigos (seguro para rodar várias vezes)
DELETE FROM order_details WHERE order_id IN (SELECT order_id FROM orders WHERE ship_name LIKE 'Cliente Sintético%' OR ship_name LIKE 'Cliente %');
DELETE FROM orders WHERE ship_name LIKE 'Cliente Sintético%' OR ship_name LIKE 'Cliente %';
DELETE FROM customers WHERE customer_id LIKE 'SYN%';

-- ============================================
-- PARTE 1: GERAR CLIENTES SINTÉTICOS (10.000)
-- ============================================
INSERT INTO customers (customer_id, company_name, contact_name, contact_title, address, city, region, postal_code, country, phone, fax)
SELECT
  'SYN' || LPAD(i::text, 5, '0'), -- Ajustado para 'SYN' para bater com o filtro
  'Empresa Sintética ' || i,
  'Contato ' || i,
  'Owner',
  'Rua Exemplo ' || i || ', ' || (i % 200),
  CASE i % 10
    WHEN 0 THEN 'São Paulo' WHEN 1 THEN 'Rio de Janeiro' WHEN 2 THEN 'Belo Horizonte'
    WHEN 3 THEN 'Curitiba' WHEN 4 THEN 'Porto Alegre' WHEN 5 THEN 'Salvador'
    WHEN 6 THEN 'Brasília' WHEN 7 THEN 'Recife' WHEN 8 THEN 'Fortaleza' WHEN 9 THEN 'Campinas'
  END,
  CASE i % 5
    WHEN 0 THEN 'SP' WHEN 1 THEN 'RJ' WHEN 2 THEN 'MG' WHEN 3 THEN 'PR' WHEN 4 THEN 'RS'
  END,
  LPAD((i * 7 % 99999)::text, 5, '0') || '-' || LPAD((i * 3 % 999)::text, 3, '0'),
  'Brazil',
  '(11) ' || LPAD((1000 + i)::text, 4, '0') || '-' || LPAD((i * 7 % 9999)::text, 4, '0'),
  NULL
FROM generate_series(1, 10000) AS i;

-- ============================================
-- PARTE 2: GERAR PEDIDOS SINTÉTICOS (200.000)
-- ============================================
-- Meta: 200.000 pedidos divididos em 4 lotes rápidos de 50.000
-- Técnica: Usar array_agg para sortear chaves estrangeiras de forma ultrarrápida

-- Lote 1
INSERT INTO orders (order_id, customer_id, employee_id, order_date, required_date, shipped_date, ship_via, freight, ship_name, ship_address, ship_city, ship_region, ship_postal_code, ship_country)
SELECT
  (SELECT COALESCE(MAX(order_id), 0) FROM orders) + i,
  c_arr[1 + floor(random() * array_length(c_arr, 1))],
  e_arr[1 + floor(random() * array_length(e_arr, 1))],
  TIMESTAMP '2015-01-01' + (random() * (TIMESTAMP '2024-12-31' - TIMESTAMP '2015-01-01')),
  TIMESTAMP '2015-01-01' + (random() * (TIMESTAMP '2024-12-31' - TIMESTAMP '2015-01-01')) + INTERVAL '7 days',
  TIMESTAMP '2015-01-01' + (random() * (TIMESTAMP '2024-12-31' - TIMESTAMP '2015-01-01')) + INTERVAL '3 days',
  s_arr[1 + floor(random() * array_length(s_arr, 1))],
  ROUND((random() * 500 + 5)::numeric, 2),
  'Cliente Sintético ' || i, 'Endereço Genérico', 'Cidade', 'UF', '00000-000', 'Brazil'
FROM generate_series(1, 50000) AS i
CROSS JOIN (SELECT array_agg(customer_id) AS c_arr FROM customers) AS c
CROSS JOIN (SELECT array_agg(employee_id) AS e_arr FROM employees) AS e
CROSS JOIN (SELECT array_agg(shipper_id) AS s_arr FROM shippers) AS s;

-- Lote 2
INSERT INTO orders (order_id, customer_id, employee_id, order_date, required_date, shipped_date, ship_via, freight, ship_name, ship_address, ship_city, ship_region, ship_postal_code, ship_country)
SELECT
  (SELECT COALESCE(MAX(order_id), 0) FROM orders) + i,
  c_arr[1 + floor(random() * array_length(c_arr, 1))],
  e_arr[1 + floor(random() * array_length(e_arr, 1))],
  TIMESTAMP '2016-01-01' + (random() * (TIMESTAMP '2024-12-31' - TIMESTAMP '2016-01-01')),
  TIMESTAMP '2016-01-01' + (random() * (TIMESTAMP '2024-12-31' - TIMESTAMP '2016-01-01')) + INTERVAL '7 days',
  TIMESTAMP '2016-01-01' + (random() * (TIMESTAMP '2024-12-31' - TIMESTAMP '2016-01-01')) + INTERVAL '3 days',
  s_arr[1 + floor(random() * array_length(s_arr, 1))],
  ROUND((random() * 500 + 5)::numeric, 2),
  'Cliente Sintético ' || i, 'Endereço Genérico', 'Cidade', 'UF', '00000-000', 'Brazil'
FROM generate_series(1, 50000) AS i
CROSS JOIN (SELECT array_agg(customer_id) AS c_arr FROM customers) AS c
CROSS JOIN (SELECT array_agg(employee_id) AS e_arr FROM employees) AS e
CROSS JOIN (SELECT array_agg(shipper_id) AS s_arr FROM shippers) AS s;

-- Lote 3
INSERT INTO orders (order_id, customer_id, employee_id, order_date, required_date, shipped_date, ship_via, freight, ship_name, ship_address, ship_city, ship_region, ship_postal_code, ship_country)
SELECT
  (SELECT COALESCE(MAX(order_id), 0) FROM orders) + i,
  c_arr[1 + floor(random() * array_length(c_arr, 1))],
  e_arr[1 + floor(random() * array_length(e_arr, 1))],
  TIMESTAMP '2017-01-01' + (random() * (TIMESTAMP '2024-12-31' - TIMESTAMP '2017-01-01')),
  TIMESTAMP '2017-01-01' + (random() * (TIMESTAMP '2024-12-31' - TIMESTAMP '2017-01-01')) + INTERVAL '7 days',
  TIMESTAMP '2017-01-01' + (random() * (TIMESTAMP '2024-12-31' - TIMESTAMP '2017-01-01')) + INTERVAL '3 days',
  s_arr[1 + floor(random() * array_length(s_arr, 1))],
  ROUND((random() * 500 + 5)::numeric, 2),
  'Cliente Sintético ' || i, 'Endereço Genérico', 'Cidade', 'UF', '00000-000', 'Brazil'
FROM generate_series(1, 50000) AS i
CROSS JOIN (SELECT array_agg(customer_id) AS c_arr FROM customers) AS c
CROSS JOIN (SELECT array_agg(employee_id) AS e_arr FROM employees) AS e
CROSS JOIN (SELECT array_agg(shipper_id) AS s_arr FROM shippers) AS s;

-- Lote 4
INSERT INTO orders (order_id, customer_id, employee_id, order_date, required_date, shipped_date, ship_via, freight, ship_name, ship_address, ship_city, ship_region, ship_postal_code, ship_country)
SELECT
  (SELECT COALESCE(MAX(order_id), 0) FROM orders) + i,
  c_arr[1 + floor(random() * array_length(c_arr, 1))],
  e_arr[1 + floor(random() * array_length(e_arr, 1))],
  TIMESTAMP '2018-01-01' + (random() * (TIMESTAMP '2024-12-31' - TIMESTAMP '2018-01-01')),
  TIMESTAMP '2018-01-01' + (random() * (TIMESTAMP '2024-12-31' - TIMESTAMP '2018-01-01')) + INTERVAL '7 days',
  TIMESTAMP '2018-01-01' + (random() * (TIMESTAMP '2024-12-31' - TIMESTAMP '2018-01-01')) + INTERVAL '3 days',
  s_arr[1 + floor(random() * array_length(s_arr, 1))],
  ROUND((random() * 500 + 5)::numeric, 2),
  'Cliente Sintético ' || i, 'Endereço Genérico', 'Cidade', 'UF', '00000-000', 'Brazil'
FROM generate_series(1, 50000) AS i
CROSS JOIN (SELECT array_agg(customer_id) AS c_arr FROM customers) AS c
CROSS JOIN (SELECT array_agg(employee_id) AS e_arr FROM employees) AS e
CROSS JOIN (SELECT array_agg(shipper_id) AS s_arr FROM shippers) AS s;


-- ============================================
-- PARTE 3: GERAR ITENS DE PEDIDO (~1.000.000)
-- ============================================
-- Meta: ~5 itens por pedido. 
-- Técnica: Usar unnest de array embaralhado para garantir 
-- que NÃO haja duplicidade de (order_id, product_id) que quebre a PK.

-- Lote 1: 40.000 pedidos (Gera ~200.000 linhas)
INSERT INTO order_details (order_id, product_id, unit_price, quantity, discount)
SELECT
    o.order_id,
    unnested.product_id,
    p.unit_price * (1 + random() * 0.3),
    (random() * 80 + 5)::int,
    CASE WHEN random() < 0.15 THEN ROUND((random() * 0.20)::numeric, 2) ELSE 0 END
FROM (
    SELECT order_id FROM orders 
    WHERE NOT EXISTS (SELECT 1 FROM order_details od WHERE od.order_id = orders.order_id)
    LIMIT 40000
) o
CROSS JOIN (SELECT array_agg(product_id ORDER BY random()) AS p_arr FROM products) AS prod
CROSS JOIN LATERAL unnest(prod.p_arr[1 : (1 + floor(random() * 6))]) AS unnested(product_id)
JOIN products p ON unnested.product_id = p.product_id;

-- Lote 2: 40.000 pedidos
INSERT INTO order_details (order_id, product_id, unit_price, quantity, discount)
SELECT o.order_id, unnested.product_id, p.unit_price * (1 + random() * 0.3), (random() * 80 + 5)::int, CASE WHEN random() < 0.15 THEN ROUND((random() * 0.20)::numeric, 2) ELSE 0 END
FROM (SELECT order_id FROM orders WHERE NOT EXISTS (SELECT 1 FROM order_details od WHERE od.order_id = orders.order_id) LIMIT 40000) o
CROSS JOIN (SELECT array_agg(product_id ORDER BY random()) AS p_arr FROM products) AS prod
CROSS JOIN LATERAL unnest(prod.p_arr[1 : (1 + floor(random() * 6))]) AS unnested(product_id)
JOIN products p ON unnested.product_id = p.product_id;

-- Lote 3: 40.000 pedidos
INSERT INTO order_details (order_id, product_id, unit_price, quantity, discount)
SELECT o.order_id, unnested.product_id, p.unit_price * (1 + random() * 0.3), (random() * 80 + 5)::int, CASE WHEN random() < 0.15 THEN ROUND((random() * 0.20)::numeric, 2) ELSE 0 END
FROM (SELECT order_id FROM orders WHERE NOT EXISTS (SELECT 1 FROM order_details od WHERE od.order_id = orders.order_id) LIMIT 40000) o
CROSS JOIN (SELECT array_agg(product_id ORDER BY random()) AS p_arr FROM products) AS prod
CROSS JOIN LATERAL unnest(prod.p_arr[1 : (1 + floor(random() * 6))]) AS unnested(product_id)
JOIN products p ON unnested.product_id = p.product_id;

-- Lote 4: 40.000 pedidos
INSERT INTO order_details (order_id, product_id, unit_price, quantity, discount)
SELECT o.order_id, unnested.product_id, p.unit_price * (1 + random() * 0.3), (random() * 80 + 5)::int, CASE WHEN random() < 0.15 THEN ROUND((random() * 0.20)::numeric, 2) ELSE 0 END
FROM (SELECT order_id FROM orders WHERE NOT EXISTS (SELECT 1 FROM order_details od WHERE od.order_id = orders.order_id) LIMIT 40000) o
CROSS JOIN (SELECT array_agg(product_id ORDER BY random()) AS p_arr FROM products) AS prod
CROSS JOIN LATERAL unnest(prod.p_arr[1 : (1 + floor(random() * 6))]) AS unnested(product_id)
JOIN products p ON unnested.product_id = p.product_id;

-- Lote 5: Restante
INSERT INTO order_details (order_id, product_id, unit_price, quantity, discount)
SELECT o.order_id, unnested.product_id, p.unit_price * (1 + random() * 0.3), (random() * 80 + 5)::int, CASE WHEN random() < 0.15 THEN ROUND((random() * 0.20)::numeric, 2) ELSE 0 END
FROM (SELECT order_id FROM orders WHERE NOT EXISTS (SELECT 1 FROM order_details od WHERE od.order_id = orders.order_id)) o
CROSS JOIN (SELECT array_agg(product_id ORDER BY random()) AS p_arr FROM products) AS prod
CROSS JOIN LATERAL unnest(prod.p_arr[1 : (1 + floor(random() * 6))]) AS unnested(product_id)
JOIN products p ON unnested.product_id = p.product_id;


-- ============================================
-- PARTE 4: VERIFICAÇÃO FINAL
-- ============================================
SELECT 'orders' AS tabela, COUNT(*) AS registros FROM orders
UNION ALL
SELECT 'order_details', COUNT(*) FROM order_details
UNION ALL
SELECT 'customers', COUNT(*) FROM customers;


-- ********************************************************************************
-- >>> INÍCIO DA AULA PRÁTICA: DEMONSTRANDO ÍNDICES E MATERIALIZED VIEWS <<<
-- ********************************************************************************

-- ============================================
-- PARTE 5: CENÁRIO 1 - A DOR (SEM ÍNDICES)
-- ============================================
-- Vamos dropar os índices para simular um banco mal configurado
DROP INDEX IF EXISTS idx_order_details_orderid;
DROP INDEX IF EXISTS idx_order_details_productid;
DROP INDEX IF EXISTS idx_orders_customerid;
DROP INDEX IF EXISTS idx_orders_employeeid;

