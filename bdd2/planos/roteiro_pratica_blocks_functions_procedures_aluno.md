# Roteiro de Prática: Blocks, Functions e Procedures em PostgreSQL

**Disciplina:** Banco de Dados II — ADS 3º Semestre — IFSP Capivari  
**Professor:** Caio Hamamura  
**Duração estimada:** 3 horas (com pausa)

---

## Pré-requisitos

- SQL básico (SELECT, INSERT, UPDATE, DELETE)
- Conceito de views

---

## Setup: Schema E-commerce Simplificado

Execute o script abaixo antes de começar os exercícios.

```sql
-- =============================================
-- SETUP: Schema e-commerce simplificado
-- Execute este script antes da prática
-- =============================================

DROP TABLE IF EXISTS pedidos_itens CASCADE;
DROP TABLE IF EXISTS pedidos CASCADE;
DROP TABLE IF EXISTS produtos CASCADE;
DROP TABLE IF EXISTS clientes CASCADE;

CREATE TABLE clientes (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE,
    cidade VARCHAR(80),
    limite_credito DECIMAL(10,2) DEFAULT 0
);

CREATE TABLE produtos (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    categoria VARCHAR(50),
    preco DECIMAL(10,2) NOT NULL,
    estoque INTEGER DEFAULT 0
);

CREATE TABLE pedidos (
    id SERIAL PRIMARY KEY,
    cliente_id INTEGER REFERENCES clientes(id),
    data_pedido DATE DEFAULT CURRENT_DATE,
    status VARCHAR(20) DEFAULT 'PENDENTE',
    valor_total DECIMAL(10,2) DEFAULT 0
);

CREATE TABLE pedidos_itens (
    id SERIAL PRIMARY KEY,
    pedido_id INTEGER REFERENCES pedidos(id),
    produto_id INTEGER REFERENCES produtos(id),
    quantidade INTEGER NOT NULL,
    preco_unitario DECIMAL(10,2) NOT NULL
);

-- Dados de exemplo
INSERT INTO clientes (nome, email, cidade, limite_credito) VALUES
('Ana Silva', 'ana@email.com', 'São Paulo', 5000),
('Bruno Costa', 'bruno@email.com', 'Campinas', 3000),
('Carla Mendes', 'carla@email.com', 'Santos', 8000),
('Daniel Ferreira', 'daniel@email.com', 'São Paulo', 2000);

INSERT INTO produtos (nome, categoria, preco, estoque) VALUES
('Notebook', 'Eletrônicos', 3500.00, 10),
('Mouse', 'Periféricos', 80.00, 50),
('Teclado', 'Periféricos', 150.00, 30),
('Monitor', 'Eletrônicos', 1200.00, 15),
('Cabo USB', 'Acessórios', 25.00, 100),
('Webcam', 'Eletrônicos', 300.00, 20),
('Pendrive 32GB', 'Armazenamento', 45.00, 80),
('HD Externo', 'Armazenamento', 350.00, 25);

INSERT INTO pedidos (cliente_id, data_pedido, status, valor_total) VALUES
(1, '2026-04-20', 'ENTREGUE', 3680.00),
(2, '2026-04-21', 'PENDENTE', 225.00),
(1, '2026-04-22', 'PROCESSANDO', 1545.00),
(3, '2026-04-23', 'ENTREGUE', 3500.00);

INSERT INTO pedidos_itens (pedido_id, produto_id, quantidade, preco_unitario) VALUES
(1, 1, 1, 3500.00),  -- Notebook
(1, 2, 2, 80.00),    -- 2 Mouses
(1, 5, 4, 25.00),    -- 4 Cabos USB
(2, 2, 1, 80.00),    -- Mouse
(2, 7, 1, 45.00),    -- Pendrive
(2, 5, 4, 25.00),    -- 4 Cabos USB
(3, 4, 1, 1200.00),  -- Monitor
(3, 2, 5, 80.00),    -- 5 Mouses
(3, 3, 5, 150.00),   -- 5 Teclados
(4, 1, 1, 3500.00);  -- Notebook
```

---

## Exercício 1 — DO Block

**Objetivo:** Crie um DO block que:

1. Conte quantos produtos existem na tabela `produtos`
2. Calcule a média de preços
3. Exiba mensagem formatada com `RAISE NOTICE`

---

## Exercício 2 — Function com OUT

**Objetivo:** Crie `fn_estatisticas_categoria(p_categoria_id)` que retorna:

- `total_produtos` — count de produtos
- `preco_medio` — preço médio
- `preco_max` — maior preço

**Dica:** Use parâmetros `OUT` para retornar múltiplos valores.

---

## Exercício 3 — Procedure com Transação

**Objetivo:** Crie `sp_transferir_estoque(origem, destino, qtd)` que:

1. Verifique se ambos os produtos existem
2. Verifique estoque suficiente na origem
3. Reduza da origem e aumente no destino
4. Levante exceção se não for possível

**Teste:**
```sql
-- Verificar estoques antes
SELECT id, nome, estoque FROM produtos WHERE id IN (2, 7);

CALL sp_transferir_estoque(2, 7, 10);

-- Verificar estoques depois
SELECT id, nome, estoque FROM produtos WHERE id IN (2, 7);
```

---

## Desafio Extra

**Objetivo:** Crie `fn_produtos_por_faixa(p_min, p_max)` que:

1. Use `RETURNS TABLE` para retornar id, nome, preço
2. Valide que `p_min <= p_max`
3. Levante exceção se inválido

---

## Material de Apoio

### Links Úteis
- [PostgreSQL Documentation: PL/pgSQL](https://www.postgresql.org/docs/current/plpgsql.html)
- [PostgreSQL Functions](https://www.postgresql.org/docs/current/sql-createfunction.html)
- [PostgreSQL Procedures](https://www.postgresql.org/docs/current/sql-createprocedure.html)

### Dica para Debug
```sql
-- Para ver mensagens de RAISE NOTICE, configure:
SET client_min_messages = 'notice';
```

---

*Criado em: 2026-04-24*  
*Banco de Dados II - ADS 3º Semestre - IFSP Capivari*
