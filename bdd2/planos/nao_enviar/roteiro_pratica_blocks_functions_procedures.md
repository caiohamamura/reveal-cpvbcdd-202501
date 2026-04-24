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

**Solução:**
```sql
DO $$
BEGIN
    RAISE NOTICE 'Olá, Banco de Dados II!';
END $$;
```

**Resultado esperado:**
```
NOTICE:  Olá, Banco de Dados II!
```

---

### Exercício 1.2: Variáveis e Concatenação

**Enunciado:** Declare uma variável `nome_aluno` com seu nome e outra `turma` com "ADS 3º". Use `RAISE NOTICE` para exibir: "Bem-vindo, [nome_aluno] da turma [turma]!".

**Solução:**
```sql
DO $$
DECLARE
    nome_aluno VARCHAR(50) := 'Seu Nome';
    turma VARCHAR(20) := 'ADS 3º';
BEGIN
    RAISE NOTICE 'Bem-vindo, % da turma %!', nome_aluno, turma;
END $$;
```

**Resultado esperado:**
```
NOTICE:  Bem-vindo, Seu Nome da turma ADS 3º!
```

---

### Exercício 1.3: Manipulação de Dados com Variáveis

**Enunciado:** Usando variáveis, atualize o limite de crédito do cliente "Ana Silva" para 7500 e exiba o novo valor.

**Solução:**
```sql
DO $$
DECLARE
    cliente_nome VARCHAR(100) := 'Ana Silva';
    novo_limite DECIMAL(10,2) := 7500.00;
    cliente_id_var INTEGER;
BEGIN
    -- Buscar ID do cliente
    SELECT id INTO cliente_id_var FROM clientes WHERE nome = cliente_nome;
    
    -- Atualizar limite
    UPDATE clientes SET limite_credito = novo_limite WHERE id = cliente_id_var;
    
    RAISE NOTICE 'Cliente % (ID: %) teve limite atualizado para R$ %', 
        cliente_nome, cliente_id_var, novo_limite;
END $$;
```

**Resultado esperado:**
```
NOTICE:  Cliente Ana Silva (ID: 1) teve limite atualizado para R$ 7500.00
```

---

### Exercício 1.4: Cálculo com Variáveis

**Enunciado:** Calcule o valor total de um pedido específico (pedido_id = 2) somando `quantidade * preco_unitario` dos itens. Use variáveis para armazenar e exibir o resultado.

**Solução:**
```sql
DO $$
DECLARE
    v_pedido_id INTEGER := 2;
    v_total DECIMAL(10,2) := 0;
    v_contagem INTEGER := 0;
BEGIN
    SELECT SUM(quantidade * preco_unitario), COUNT(*)
    INTO v_total, v_contagem
    FROM pedidos_itens
    WHERE pedido_id = v_pedido_id;
    
    RAISE NOTICE 'Pedido #% possui % itens - Total: R$ %', 
        v_pedido_id, v_contagem, v_total;
END $$;
```

**Resultado esperado:**
```
NOTICE:  Pedido #2 possui 3 itens - Total: R$ 225.00
```

---

### Exercício 1.5: Lógica Condicional (IF/THEN/ELSE)

**Enunciado:** Verifique o estoque do produto "Mouse" e exiba mensagem diferente conforme a quantidade:
- Estoque < 20: "Estoque baixo - reposição necessária"
- Estoque entre 20 e 50: "Estoque adequado"
- Estoque > 50: "Estoque alto"

**Solução:**
```sql
DO $$
DECLARE
    v_produto VARCHAR(100) := 'Mouse';
    v_estoque INTEGER;
BEGIN
    SELECT estoque INTO v_estoque FROM produtos WHERE nome = v_produto;
    
    IF v_estoque < 20 THEN
        RAISE NOTICE 'Estoque baixo - reposição necessária (atual: %)', v_estoque;
    ELSIF v_estoque <= 50 THEN
        RAISE NOTICE 'Estoque adequado (atual: %)', v_estoque;
    ELSE
        RAISE NOTICE 'Estoque alto (atual: %)', v_estoque;
    END IF;
END $$;
```

**Resultado esperado:**
```
NOTICE:  Estoque adequado (atual: 50)
```

---

### Exercício 1.6: LOOP Básico

**Enunciado:** Use um LOOP para exibir os números de 1 a 5, um por linha.

**Solução:**
```sql
DO $$
DECLARE
    contador INTEGER := 1;
BEGIN
    LOOP
        EXIT WHEN contador > 5;
        RAISE NOTICE 'Número: %', contador;
        contador := contador + 1;
    END LOOP;
END $$;
```

**Resultado esperado:**
```
NOTICE:  Número: 1
NOTICE:  Número: 2
NOTICE:  Número: 3
NOTICE:  Número: 4
NOTICE:  Número: 5
```

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

**Solução:**
```sql
CREATE OR REPLACE FUNCTION fn_total_pedido(p_pedido_id INTEGER)
RETURNS DECIMAL(10,2) AS $$
DECLARE
    v_total DECIMAL(10,2);
BEGIN
    SELECT COALESCE(SUM(quantidade * preco_unitario), 0)
    INTO v_total
    FROM pedidos_itens
    WHERE pedido_id = p_pedido_id;
    
    RETURN v_total;
END;
$$ LANGUAGE plpgsql;
```

**Teste:**
```sql
SELECT fn_total_pedido(2);
```

**Resultado esperado:**
```
 fn_total_pedido 
-----------------
          225.00
```

---

### Exercício 2.2: Função com Validação

**Enunciado:** Crie uma função `fn_desconto` que recebe um valor e um percentual de desconto. Se o percentual for negativo ou maior que 50, retorne NULL (desconto inválido). Caso contrário, retorne o valor com desconto aplicado.

**Solução:**
```sql
CREATE OR REPLACE FUNCTION fn_desconto(p_valor DECIMAL(10,2), p_percentual DECIMAL(5,2))
RETURNS DECIMAL(10,2) AS $$
BEGIN
    IF p_percentual < 0 OR p_percentual > 50 THEN
        RETURN NULL;
    END IF;
    
    RETURN p_valor * (1 - p_percentual / 100);
END;
$$ LANGUAGE plpgsql IMMUTABLE;
```

**Teste:**
```sql
SELECT fn_desconto(1000.00, 10);    -- Válido: 900.00
SELECT fn_desconto(1000.00, 60);    -- Inválido: NULL
SELECT fn_desconto(1000.00, -5);    -- Inválido: NULL
```

**Resultado esperado:**
```
 fn_desconto 
-------------
     900.00

 fn_desconto 
-------------
     

 fn_desconto 
-------------
     
```

---

### Exercício 2.3: Função que Retorna uma Tabela (TABLE)

**Enunciado:** Crie uma função `fn_produtos_por_categoria` que recebe o nome de uma categoria e retorna todos os produtos daquela categoria (id, nome, preco).

**Solução:**
```sql
CREATE OR REPLACE FUNCTION fn_produtos_por_categoria(p_categoria VARCHAR)
RETURNS TABLE(id INTEGER, nome VARCHAR, preco DECIMAL(10,2)) AS $$
BEGIN
    RETURN QUERY
    SELECT pro.id, pro.nome, pro.preco
    FROM produtos pro
    WHERE pro.categoria = p_categoria;
END;
$$ LANGUAGE plpgsql;
```

**Teste:**
```sql
SELECT * FROM fn_produtos_por_categoria('Eletrônicos');
```

**Resultado esperado:**
```
 id |   nome    |   preco   
----+-----------+-----------
  1 | Notebook  |  3500.00
  4 | Monitor   |  1200.00
  6 | Webcam    |   300.00
```

---

### Exercício 2.4: Função para Atualizar e Retornar

**Enunciado:** Crie uma função `fn_atualizar_estoque` que recebe um ID de produto e uma quantidade (pode ser negativa para reduzir). A função deve atualizar o estoque e retornar o novo valor.

**Solução:**
```sql
CREATE OR REPLACE FUNCTION fn_atualizar_estoque(p_produto_id INTEGER, p_quantidade INTEGER)
RETURNS INTEGER AS $$
DECLARE
    v_novo_estoque INTEGER;
BEGIN
    UPDATE produtos
    SET estoque = estoque + p_quantidade
    WHERE id = p_produto_id
    RETURNING estoque INTO v_novo_estoque;
    
    RETURN v_novo_estoque;
END;
$$ LANGUAGE plpgsql;
```

**Teste:**
```sql
SELECT fn_atualizar_estoque(2, 10);  -- Adiciona 10 mouses
SELECT fn_atualizar_estoque(2, -5);  -- Remove 5 mouses
SELECT * FROM produtos WHERE id = 2;
```

**Resultado esperado:**
```
 fn_atualizar_estoque 
---------------------
                   60
(1 row)

 fn_atualizar_estoque 
---------------------
                   55
(1 row)

 id |  nome  | categoria    | preco | estoque 
----+--------+--------------+-------+---------
  2 | Mouse  | Periféricos  | 80.00 |      55
```

---

### Exercício 2.5: Função com IF e Retorno Múltiplo

**Enunciado:** Crie uma função `fn_classifica_cliente` que recebe o ID de um cliente e retorna um texto:
- "VIP" se limite_credito > 5000
- "Regular" se limite_credito entre 2000 e 5000
- "Básico" se limite_credito < 2000

**Solução:**
```sql
CREATE OR REPLACE FUNCTION fn_classifica_cliente(p_cliente_id INTEGER)
RETURNS VARCHAR(20) AS $$
DECLARE
    v_limite DECIMAL(10,2);
BEGIN
    SELECT limite_credito INTO v_limite FROM clientes WHERE id = p_cliente_id;
    
    IF v_limite > 5000 THEN
        RETURN 'VIP';
    ELSIF v_limite >= 2000 THEN
        RETURN 'Regular';
    ELSE
        RETURN 'Básico';
    END IF;
END;
$$ LANGUAGE plpgsql;
```

**Teste:**
```sql
SELECT nome, limite_credito, fn_classifica_cliente(id) AS classificacao FROM clientes;
```

**Resultado esperado:**
```
   nome    | limite_credito | classificacao 
-----------+-----------------+----------------
 Ana Silva |        7500.00 | VIP
 Bruno Costa|        3000.00 | Regular
 Carla Mendes|       8000.00 | VIP
 Daniel Ferreira|     2000.00 | Regular
```

---

### Exercício 2.6: Função que Retorna Múltiplas Colunas com OUT Parameters

**Enunciado:** Crie uma função `fn_estatisticas_cliente` que recebe o ID do cliente e retorna (via OUT parameters): total de pedidos, valor total gasto, e quantidade de itens comprados.

**Solução:**
```sql
CREATE OR REPLACE FUNCTION fn_estatisticas_cliente(
    p_cliente_id INTEGER,
    OUT total_pedidos INTEGER,
    OUT valor_gasto DECIMAL(10,2),
    OUT total_itens INTEGER
) AS $$
BEGIN
    SELECT COUNT(*), COALESCE(SUM(valor_total), 0)
    INTO total_pedidos, valor_gasto
    FROM pedidos
    WHERE cliente_id = p_cliente_id;
    
    SELECT COALESCE(SUM(pi.quantidade), 0)
    INTO total_itens
    FROM pedidos p
    JOIN pedidos_itens pi ON p.id = pi.pedido_id
    WHERE p.cliente_id = p_cliente_id;
END;
$$ LANGUAGE plpgsql;
```

**Teste:**
```sql
SELECT * FROM fn_estatisticas_cliente(1);
```

**Resultado esperado:**
```
 total_pedidos | valor_gasto | total_itens 
---------------+-------------+-------------
             2 |     5225.00 |          12
```

---

### Exercício 2.7: Função que Retorna SETOF (Row Type)

**Enunciado:** Crie uma função `fn_info_pedido` que recebe o ID do pedido e retorna uma linha do tipo `pedidos%ROWTYPE` com todas as informações do pedido.

**Solução:**
```sql
CREATE OR REPLACE FUNCTION fn_info_pedido(p_pedido_id INTEGER)
RETURNS pedidos AS $$
DECLARE
    v_pedido pedidos%ROWTYPE;
BEGIN
    SELECT * INTO v_pedido FROM pedidos WHERE id = p_pedido_id;
    RETURN v_pedido;
END;
$$ LANGUAGE plpgsql;
```

**Teste:**
```sql
SELECT (fn_info_pedido(1)).*;
```

**Resultado esperado:**
```
 id | cliente_id | data_pedido |    status     | valor_total 
----+------------+-------------+---------------+-------------
  1 |          1 | 2026-04-20  | ENTREGUE      |     3680.00
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

**Solução:**
```sql
CREATE OR REPLACE PROCEDURE sp_novo_cliente(
    p_nome VARCHAR,
    p_email VARCHAR,
    p_cidade VARCHAR,
    p_limite DECIMAL(10,2)
) AS $$
BEGIN
    INSERT INTO clientes (nome, email, cidade, limite_credito)
    VALUES (p_nome, p_email, p_cidade, p_limite);
    
    RAISE NOTICE 'Cliente % inserido com sucesso!', p_nome;
END;
$$ LANGUAGE plpgsql;
```

**Teste:**
```sql
CALL sp_novo_cliente('Eduardo Lima', 'eduardo@email.com', 'São Paulo', 4500);
SELECT * FROM clientes WHERE nome = 'Eduardo Lima';
```

**Resultado esperado:**
```
NOTICE:  Cliente Eduardo Lima inserido com sucesso!

 id |    nome     |        email         |   cidade   | limite_credito 
----+-------------+----------------------+------------+----------------
  5 | Eduardo Lima| eduardo@email.com    | São Paulo  |        4500.00
```

---

### Exercício 3.2: Procedure com Validação e Exceção

**Enunciado:** Crie uma procedure `sp_atualizar_pedido_status` que recebe o ID do pedido e o novo status. Se o pedido não existir, lance uma exceção.

**Solução:**
```sql
CREATE OR REPLACE PROCEDURE sp_atualizar_pedido_status(
    p_pedido_id INTEGER,
    p_novo_status VARCHAR
)
AS $$
DECLARE
    v_existe INTEGER;
BEGIN
    -- Verificar se pedido existe
    SELECT COUNT(*) INTO v_existe FROM pedidos WHERE id = p_pedido_id;
    
    IF v_existe = 0 THEN
        RAISE EXCEPTION 'Pedido #% não encontrado!', p_pedido_id;
    END IF;
    
    -- Atualizar status
    UPDATE pedidos SET status = p_novo_status WHERE id = p_pedido_id;
    
    RAISE NOTICE 'Pedido #% atualizado para status: %', p_pedido_id, p_novo_status;
END;
$$ LANGUAGE plpgsql;
```

**Teste:**
```sql
CALL sp_atualizar_pedido_status(2, 'ENVIADO');       -- Válido
CALL sp_atualizar_pedido_status(999, 'ENVIADO');    -- Erro
```

**Resultado esperado:**
```
NOTICE:  Pedido #2 atualizado para status: ENVIADO
ERROR:  Pedido #999 não encontrado!
CONTEXT:  PL/pgSQL function sp_atualizar_pedido_status(...) line 11 at RAISE
```

---

### Exercício 3.3: Procedure com TRANSACTION

**Enunciado:** Crie uma procedure `sp_transferir_estoque` que recebe dois IDs de produto e uma quantidade. A procedure deve:
1. Verificar se ambos os produtos existem
2. Verificar se há estoque suficiente no produto origem
3. Reduzir do origem e aumentar no destino
4. Fazer tudo em uma transação (ou reverter tudo)

**Solução:**
```sql
CREATE OR REPLACE PROCEDURE sp_transferir_estoque(
    p_produto_origem INTEGER,
    p_produto_destino INTEGER,
    p_quantidade INTEGER
)
AS $$
DECLARE
    v_estoque_origem INTEGER;
BEGIN
    -- Verificar produto origem
    SELECT estoque INTO v_estoque_origem FROM produtos WHERE id = p_produto_origem;
    IF NOT FOUND THEN
        RAISE EXCEPTION 'Produto origem #% não encontrado!', p_produto_origem;
    END IF;
    
    -- Verificar produto destino
    IF NOT EXISTS (SELECT 1 FROM produtos WHERE id = p_produto_destino) THEN
        RAISE EXCEPTION 'Produto destino #% não encontrado!', p_produto_destino;
    END IF;
    
    -- Verificar estoque
    IF v_estoque_origem < p_quantidade THEN
        RAISE EXCEPTION 'Estoque insuficiente! Disponível: %', v_estoque_origem;
    END IF;
    
    -- Realizar transferência
    UPDATE produtos SET estoque = estoque - p_quantidade WHERE id = p_produto_origem;
    UPDATE produtos SET estoque = estoque + p_quantidade WHERE id = p_produto_destino;
    
    RAISE NOTICE 'Transferência concluída: % unidades de #% para #%', 
        p_quantidade, p_produto_origem, p_produto_destino;
    
EXCEPTION
    WHEN OTHERS THEN
        RAISE NOTICE 'Transferência cancelada: %', SQLERRM;
        RAISE;
END;
$$ LANGUAGE plpgsql;
```

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

**Resultado esperado:**
```
 id |   nome    | estoque 
----+-----------+---------
  2 | Mouse     |      55
  7 | Pendrive  |      80

NOTICE:  Transferência concluída: 10 unidades de #2 para #7

 id |   nome    | estoque 
----+-----------+---------
  2 | Mouse     |      45
  7 | Pendrive  |      90

ERROR:  Estoque insuficiente! Disponível: 45
```

---

### Exercício 3.4: Procedure com CURSOR e LOOP

**Enunciado:** Crie uma procedure `sp_listar_pedidos_por_status` que recebe um status e lista todos os pedidos com ese status, formatando a saída.

**Solução:**
```sql
CREATE OR REPLACE PROCEDURE sp_listar_pedidos_por_status(p_status VARCHAR)
AS $$
DECLARE
    v_pedido RECORD;
BEGIN
    RAISE NOTICE '=== Pedidos com status: % ===', p_status;
    RAISE NOTICE '----------------------------------------';
    
    FOR v_pedido IN 
        SELECT p.id, c.nome AS cliente, p.valor_total
        FROM pedidos p
        JOIN clientes c ON p.cliente_id = c.id
        WHERE p.status = p_status
        ORDER BY p.id
    LOOP
        RAISE NOTICE 'Pedido #% | Cliente: % | Valor: R$ %', 
            v_pedido.id, v_pedido.cliente, v_pedido.valor_total;
    END LOOP;
    
    RAISE NOTICE '----------------------------------------';
END;
$$ LANGUAGE plpgsql;
```

**Teste:**
```sql
CALL sp_listar_pedidos_por_status('ENTREGUE');
CALL sp_listar_pedidos_por_status('PENDENTE');
```

**Resultado esperado:**
```
NOTICE: === Pedidos com status: ENTREGUE ===
NOTICE: ----------------------------------------
NOTICE: Pedido #1 | Cliente: Ana Silva | Valor: R$ 3680.00
NOTICE: Pedido #4 | Cliente: Carla Mendes | Valor: R$ 3500.00
NOTICE: ----------------------------------------
NOTICE: === Pedidos com status: PENDENTE ===
NOTICE: ----------------------------------------
NOTICE: Pedido #2 | Cliente: Bruno Costa | Valor: R$ 225.00
NOTICE: ----------------------------------------
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

**Resolução:**
```sql
CREATE OR REPLACE FUNCTION fn_faturamento_periodo(p_data_inicio DATE, p_data_fim DATE)
RETURNS DECIMAL(10,2) AS $$
DECLARE
    v_faturamento DECIMAL(10,2);
BEGIN
    SELECT COALESCE(SUM(valor_total), 0)
    INTO v_faturamento
    FROM pedidos
    WHERE data_pedido BETWEEN p_data_inicio AND p_data_fim
      AND status IN ('ENTREGUE', 'PROCESSANDO');
    
    RETURN v_faturamento;
END;
$$ LANGUAGE plpgsql;

-- Teste
SELECT fn_faturamento_periodo('2026-04-01', '2026-04-30') AS faturamento_abril;
```

---

### Desafio 4.2: Procedure de Baixa de Pedido (Médio-Difícil)

**Enunciado:** Crie uma procedure `sp_finalizar_pedido` que:
1. Recebe o ID do pedido
2. Valida se o pedido existe e está em status válido para finalização
3. Calcula o valor total dos itens
4. Atualiza o valor_total na tabela pedidos
5. Atualiza o status para "FINALIZADO"

**Resolução:**
```sql
CREATE OR REPLACE PROCEDURE sp_finalizar_pedido(p_pedido_id INTEGER)
AS $$
DECLARE
    v_status VARCHAR(20);
    v_total DECIMAL(10,2);
    v_cliente_id INTEGER;
BEGIN
    -- Verificar se pedido existe
    SELECT status, cliente_id INTO v_status, v_cliente_id FROM pedidos WHERE id = p_pedido_id;
    
    IF NOT FOUND THEN
        RAISE EXCEPTION 'Pedido #% não encontrado!', p_pedido_id;
    END IF;
    
    -- Validar status
    IF v_status NOT IN ('PENDENTE', 'PROCESSANDO') THEN
        RAISE EXCEPTION 'Pedido #% não pode ser finalizado (status atual: %)', p_pedido_id, v_status;
    END IF;
    
    -- Calcular valor total
    SELECT SUM(quantidade * preco_unitario)
    INTO v_total
    FROM pedidos_itens
    WHERE pedido_id = p_pedido_id;
    
    -- Atualizar pedido
    UPDATE pedidos 
    SET valor_total = COALESCE(v_total, 0),
        status = 'FINALIZADO'
    WHERE id = p_pedido_id;
    
    RAISE NOTICE 'Pedido #% finalizado! Valor: R$ %', p_pedido_id, COALESCE(v_total, 0);
END;
$$ LANGUAGE plpgsql;
```

---

### Desafio 4.3: Function de Ranking de Clientes (Difícil)

**Enunciado:** Crie uma função `fn_ranking_clientes` que retorna os top N clientes por valor total de compras no período. A função deve receber:
- `p_limite` (INTEGER): quantos clientes retornar
- `p_data_inicio` (DATE): data inicial do período
- `p_data_fim` (DATE): data final do período

A função deve retornar uma tabela com: posição, nome do cliente, total de pedidos, valor total gasto.

**Resolução:**
```sql
CREATE OR REPLACE FUNCTION fn_ranking_clientes(p_limite INTEGER, p_data_inicio DATE, p_data_fim DATE)
RETURNS TABLE(posicao INTEGER, cliente_nome VARCHAR, total_pedidos BIGINT, valor_total DECIMAL(10,2)) AS $$
BEGIN
    RETURN QUERY
    WITH ranking AS (
        SELECT 
            c.nome,
            COUNT(p.id) AS tot_pedidos,
            COALESCE(SUM(p.valor_total), 0) AS tot_valor
        FROM clientes c
        LEFT JOIN pedidos p ON c.id = p.cliente_id 
            AND p.data_pedido BETWEEN p_data_inicio AND p_data_fim
            AND p.status IN ('ENTREGUE', 'FINALIZADO', 'PROCESSANDO')
        GROUP BY c.id, c.nome
        ORDER BY tot_valor DESC
        LIMIT p_limite
    )
    SELECT 
        ROW_NUMBER() OVER (ORDER BY r.tot_valor DESC)::INTEGER,
        r.nome,
        r.tot_pedidos::BIGINT,
        r.tot_valor
    FROM ranking r;
END;
$$ LANGUAGE plpgsql;

-- Teste
SELECT * FROM fn_ranking_clientes(3, '2026-04-01', '2026-04-30');
```

---

### Desafio 4.4: Procedure de Cleanup (Avançado)

**Enunciado:** Crie uma procedure `sp_limpar_pedidos_cancelados` que:
1. Identifica pedidos com status "CANCELADO" com mais de 30 dias
2. Remove os itens desses pedidos (tabela pedidos_itens)
3. Remove os pedidos
4. Retorna o relatório do que foi excluído

**Resolução:**
```sql
CREATE OR REPLACE PROCEDURE sp_limpar_pedidos_cancelados(p_dias_antiguidade INTEGER DEFAULT 30)
AS $$
DECLARE
    v_pedidos_excluidos INTEGER;
    v_itens_excluidos INTEGER;
    v_data_limite DATE;
BEGIN
    v_data_limite := CURRENT_DATE - p_dias_antiguidade;
    
    -- Contar antes de excluir
    SELECT COUNT(*), COALESCE(SUM(1), 0) 
    INTO v_pedidos_excluidos, v_itens_excluidos
    FROM pedidos 
    WHERE status = 'CANCELADO' AND data_pedido < v_data_limite;
    
    -- Excluir itens primeiro (integridade referencial)
    DELETE FROM pedidos_itens
    WHERE pedido_id IN (SELECT id FROM pedidos WHERE status = 'CANCELADO' AND data_pedido < v_data_limite);
    
    -- Excluir pedidos
    DELETE FROM pedidos
    WHERE status = 'CANCELADO' AND data_pedido < v_data_limite;
    
    GET DIAGNOSTICS v_pedidos_excluidos = ROW_COUNT;
    
    RAISE NOTICE '=== Limpeza Concluída ===';
    RAISE NOTICE 'Pedidos removidos: %', v_pedidos_excluidos;
    RAISE NOTICE 'Itens removidos: %', v_itens_excluidos;
    RAISE NOTICE 'Data limite: %', v_data_limite;
END;
$$ LANGUAGE plpgsql;
```

---

### Desafio 4.5: VIEW com Function - Relatório Gerencial (Avançado)

**Enunciado:** Crie uma view `vw_resumo_financeiro` que usa a função `fn_faturamento_periodo` para mostrar o faturamento dos últimos 7, 30 e 90 dias.

**Resolução:**
```sql
CREATE OR REPLACE VIEW vw_resumo_financeiro AS
SELECT 
    'Últimos 7 dias' AS periodo,
    fn_faturamento_periodo(CURRENT_DATE - 7, CURRENT_DATE) AS faturamento
UNION ALL
SELECT 
    'Últimos 30 dias' AS periodo,
    fn_faturamento_periodo(CURRENT_DATE - 30, CURRENT_DATE) AS faturamento
UNION ALL
SELECT 
    'Últimos 90 dias' AS periodo,
    fn_faturamento_periodo(CURRENT_DATE - 90, CURRENT_DATE) AS faturamento;

-- Teste
SELECT * FROM vw_resumo_financeiro;
```

---

## Gabarito Resumido (Para o Professor)

| Exercício | Conceito Principal |複雜度 |
|-----------|-------------------|-------|
| 1.1 | DO block básico | ⭐ |
| 1.2 | Variáveis e concatenação | ⭐ |
| 1.3 | Variáveis + UPDATE | ⭐⭐ |
| 1.4 | Aggregação em variável | ⭐⭐ |
| 1.5 | IF/THEN/ELSE | ⭐⭐ |
| 1.6 | LOOP básico | ⭐⭐ |
| 2.1 | Function escalar | ⭐⭐ |
| 2.2 | Function com validação | ⭐⭐ |
| 2.3 | Function retorna TABLE | ⭐⭐⭐ |
| 2.4 | Function com UPDATE+RETURNING | ⭐⭐ |
| 2.5 | Function com IF/ELSE | ⭐⭐ |
| 2.6 | OUT parameters | ⭐⭐⭐ |
| 2.7 | %ROWTYPE return | ⭐⭐⭐ |
| 3.1 | Procedure básica | ⭐⭐ |
| 3.2 | Procedure com exceção | ⭐⭐⭐ |
| 3.3 | Procedure com transação | ⭐⭐⭐ |
| 3.4 | Procedure com CURSOR/LOOP | ⭐⭐⭐ |
| 4.1 | Function de negócio | ⭐⭐ |
| 4.2 | Procedure de negócio | ⭐⭐⭐ |
| 4.3 | Function com ranking | ⭐⭐⭐ |
| 4.4 | Procedure de manutenção | ⭐⭐⭐ |
| 4.5 | VIEW + Function | ⭐⭐⭐⭐ |

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