# Roteiro de Prática: Blocks, Functions e Procedures em PostgreSQL

**Disciplina:** Banco de Dados II — ADS 3º Semestre — IFSP Capivari
**Professor:** Caio Hamamura
**Duração estimada:** 3 horas (com pausa)

---

## Pré-requisitos

- SQL básico (SELECT, INSERT, UPDATE, DELETE)
- Conceito de views
- Conhecimento do banco de dados chosen (Northwind ou schema próprio)

## Banco de Dados de Apoio

Usaremos um schema próprio para garantir consistência nos exercícios. Execute o script de setup abaixo antes de começar.

---

## Setup: Schema E-commerce Simplificado

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

## PARTE 1: DO Blocks (Blocos Anônimos)

### 🎯 Objetivo
Compreender a estrutura básica de blocos PL/pgSQL e sua utilidade para operações avulsas.

### Conceito-Chave
`DO` executa um bloco de código anônimo (sem nome, sem parâmetros, sem reutilização). Ideal para tarefas únicas ou testes rápidos.

### Sintaxe Básica
```sql
DO $$
DECLARE
    -- declarações
BEGIN
    -- código
END $$;
```

---

### Exercício 1.1: Olá, Mundo! (Familiarização)

**Enunciado:** Execute um DO block que imprimia "Olá, Banco de Dados II!" usando `RAISE NOTICE`.

---

### Exercício 1.2: Variáveis e Concatenação

**Enunciado:** Declare uma variável `nome_aluno` com seu nome e outra `turma` com "ADS 3º". Use `RAISE NOTICE` para exibir: "Bem-vindo, [nome_aluno] da turma [turma]!".

---

### Exercício 1.3: Manipulação de Dados com Variáveis

**Enunciado:** Usando variáveis, atualize o limite de crédito do cliente "Ana Silva" para 7500 e exiba o novo valor.

---

### Exercício 1.4: Cálculo com Variáveis

**Enunciado:** Calcule o valor total de um pedido específico (pedido_id = 2) somando `quantidade * preco_unitario` dos itens. Use variáveis para armazenar e exibir o resultado.

---

### Exercício 1.5: Lógica Condicional (IF/THEN/ELSE)

**Enunciado:** Verifique o estoque do produto "Mouse" e exiba mensagem diferente conforme a quantidade:
- Estoque < 20: "Estoque baixo - reposição necessária"
- Estoque entre 20 e 50: "Estoque adequado"
- Estoque > 50: "Estoque alto"

---

### Exercício 1.6: LOOP Básico

**Enunciado:** Use um LOOP para exibir os números de 1 a 5, um por linha.

---

## PARTE 2: Functions (Funções)

### 🎯 Objetivo
Criar funções reutilizáveis que retornam valores escalares ou tabelas.

### Conceito-Chave
Funções em PostgreSQL são objetos nomeados que podem receber parâmetros e retornar valores. Podem ser usadas em SELECT, WHERE, e outras expressões SQL.

### Sintaxe Básica
```sql
CREATE OR REPLACE FUNCTION nome_funcao(param1 tipo1, param2 tipo2)
RETURNS tipo_retorno AS $$
DECLARE
    -- variáveis
BEGIN
    -- lógica
    RETURN valor;
END;
$$ LANGUAGE plpgsql;
```

---

### Exercício 2.1: Função Escalar Simples

**Enunciado:** Crie uma função `fn_total_pedido` que recebe o ID de um pedido e retorna o valor total (soma de quantidade × preço unitário dos itens).

**Teste:**
```sql
SELECT fn_total_pedido(2);
```

---

### Exercício 2.2: Função com Validação

**Enunciado:** Crie uma função `fn_desconto` que recebe um valor e um percentual de desconto. Se o percentual for negativo ou maior que 50, retorne NULL (desconto inválido). Caso contrário, retorne o valor com desconto aplicado.

**Teste:**
```sql
SELECT fn_desconto(1000.00, 10);    -- Válido: 900.00
SELECT fn_desconto(1000.00, 60);    -- Inválido: NULL
SELECT fn_desconto(1000.00, -5);    -- Inválido: NULL
```

---

### Exercício 2.3: Função que Retorna uma Tabela (TABLE)

**Enunciado:** Crie uma função `fn_produtos_por_categoria` que recebe o nome de uma categoria e retorna todos os produtos daquela categoria (id, nome, preco).

**Teste:**
```sql
SELECT * FROM fn_produtos_por_categoria('Eletrônicos');
```

---

### Exercício 2.4: Função para Atualizar e Retornar

**Enunciado:** Crie uma função `fn_atualizar_estoque` que recebe um ID de produto e uma quantidade (pode ser negativa para reduzir). A função deve atualizar o estoque e retornar o novo valor.

**Teste:**
```sql
SELECT fn_atualizar_estoque(2, 10);  -- Adiciona 10 mouses
SELECT fn_atualizar_estoque(2, -5);  -- Remove 5 mouses
SELECT * FROM produtos WHERE id = 2;
```

---

### Exercício 2.5: Função com IF e Retorno Múltiplo

**Enunciado:** Crie uma função `fn_classifica_cliente` que recebe o ID de um cliente e retorna um texto:
- "VIP" se limite_credito > 5000
- "Regular" se limite_credito entre 2000 e 5000
- "Básico" se limite_credito < 2000

**Teste:**
```sql
SELECT nome, limite_credito, fn_classifica_cliente(id) AS classificacao FROM clientes;
```

---

### Exercício 2.6: Função que Retorna Múltiplas Colunas com OUT Parameters

**Enunciado:** Crie uma função `fn_estatisticas_cliente` que recebe o ID do cliente e retorna (via OUT parameters): total de pedidos, valor total gasto, e quantidade de itens comprados.

**Teste:**
```sql
SELECT * FROM fn_estatisticas_cliente(1);
```

---

### Exercício 2.7: Função que Retorna SETOF (Row Type)

**Enunciado:** Crie uma função `fn_info_pedido` que recebe o ID do pedido e retorna uma linha do tipo `pedidos%ROWTYPE` com todas as informações do pedido.

**Teste:**
```sql
SELECT (fn_info_pedido(1)).*;
```

---

## PARTE 3: Procedures (Procedimentos)

### 🎯 Objetivo
Diferenciar procedures de functions e entender quando usar cada uma. Procedures são chamadas com `CALL` e não retornam valor diretamente.

### Conceito-Chave
A partir do PostgreSQL 11, procedures suportam transação própria (podem fazer COMMIT/ROLLBACK internos). Functions devem ser atômicas e não podem controlar transações.

### Sintaxe Básica
```sql
CREATE OR REPLACE PROCEDURE nome_procedure(param1 tipo1, param2 tipo2)
AS $$
DECLARE
    -- variáveis
BEGIN
    -- lógica
END;
$$ LANGUAGE plpgsql;
```

---

### Exercício 3.1: Procedure para Inserir Dados

**Enunciado:** Crie uma procedure `sp_novo_cliente` que recebe nome, email, cidade e limite_credito, e insere um novo cliente na tabela. Use `CALL` para testar.

**Teste:**
```sql
CALL sp_novo_cliente('Eduardo Lima', 'eduardo@email.com', 'São Paulo', 4500);
SELECT * FROM clientes WHERE nome = 'Eduardo Lima';
```

---

### Exercício 3.2: Procedure com Validação e Exceção

**Enunciado:** Crie uma procedure `sp_atualizar_pedido_status` que recebe o ID do pedido e o novo status. Se o pedido não existir, lance uma exceção.

**Teste:**
```sql
CALL sp_atualizar_pedido_status(2, 'ENVIADO');       -- Válido
CALL sp_atualizar_pedido_status(999, 'ENVIADO');    -- Erro
```

---

### Exercício 3.3: Procedure com TRANSACTION

**Enunciado:** Crie uma procedure `sp_transferir_estoque` que recebe dois IDs de produto e uma quantidade. A procedure deve:
1. Verificar se ambos os produtos existem
2. Verificar se há estoque suficiente no produto origem
3. Reduzir do origem e aumentar no destino
4. Fazer tudo em uma transação (ou reverter tudo)

**Teste:**
```sql
-- Verificar estoques antes
SELECT id, nome, estoque FROM produtos WHERE id IN (2, 7);

CALL sp_transferir_estoque(2, 7, 10);  -- Transferir 10 mouses para pendrives

-- Verificar estoques depois
SELECT id, nome, estoque FROM produtos WHERE id IN (2, 7);

-- Testar erro (estoque insuficiente)
CALL sp_transferir_estoque(2, 7, 100);
```

---

### Exercício 3.4: Procedure com CURSOR e LOOP

**Enunciado:** Crie uma procedure `sp_listar_pedidos_por_status` que recebe um status e lista todos os pedidos com ese status, formatando a saída.

**Teste:**
```sql
CALL sp_listar_pedidos_por_status('ENTREGUE');
CALL sp_listar_pedidos_por_status('PENDENTE');
```

---

## PARTE 4: Desafio Integrador

### 🎯 Objetivo
Integrar todos os conceitos aprendidos: DO blocks, functions e procedures em um cenário realista.

### Cenário: Sistema de Faturamento

Você foi contratado para criar rotinas de apoio a um sistema de faturamento e-commerce.

---

### Desafio 4.1: Function de Faturamento (Médio)

**Enunciado:** Crie uma função `fn_faturamento_periodo` que recebe duas datas (início e fim) e retorna o faturamento total do período.

---

### Desafio 4.2: Procedure de Baixa de Pedido (Médio-Difícil)

**Enunciado:** Crie uma procedure `sp_finalizar_pedido` que:
1. Recebe o ID do pedido
2. Valida se o pedido existe e está em status válido para finalização
3. Calcula o valor total dos itens
4. Atualiza o valor_total na tabela pedidos
5. Atualiza o status para "FINALIZADO"

---

### Desafio 4.3: Function de Ranking de Clientes (Difícil)

**Enunciado:** Crie uma função `fn_ranking_clientes` que retorna os top N clientes por valor total de compras no período. A função deve receber:
- `p_limite` (INTEGER): quantos clientes retornar
- `p_data_inicio` (DATE): data inicial do período
- `p_data_fim` (DATE): data final do período

A função deve retornar uma tabela com: posição, nome do cliente, total de pedidos, valor total gasto.

---

### Desafio 4.4: Procedure de Cleanup (Avançado)

**Enunciado:** Crie uma procedure `sp_limpar_pedidos_cancelados` que:
1. Identifica pedidos com status "CANCELADO" com mais de 30 dias
2. Remove os itens desses pedidos (tabela pedidos_itens)
3. Remove os pedidos
4. Retorna o relatório do que foi excluído

---

### Desafio 4.5: VIEW com Function - Relatório Gerencial (Avançado)

**Enunciado:** Crie uma view `vw_resumo_financeiro` que usa a função `fn_faturamento_periodo` para mostrar o faturamento dos últimos 7, 30 e 90 dias.

---

## Critérios de Avaliação

| Nível | Requisitos |
|-------|-----------|
| **Básico** | Exercícios 1.1 a 1.6 |
| **Intermediário** | + Exercícios 2.1, 2.2, 2.4, 3.1 |
| **Avançado** | + Exercícios 2.3, 2.5, 3.2, 3.3, 4.1, 4.2 |
| **Expert** | + Exercícios 2.6, 3.4, 4.3, 4.4, 4.5 |

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

-- Para debug de functions, use:
SELECT fn_nome_funcao(...) AS debug;
```

---

*Criado em: 2026-04-24*  
*Banco de Dados II - ADS 3º Semestre - IFSP Capivari*
