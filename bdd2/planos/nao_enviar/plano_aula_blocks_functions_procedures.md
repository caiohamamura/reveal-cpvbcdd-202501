# Plano de Aula: Blocks, Functions e Procedures em PostgreSQL

**Disciplina:** Banco de Dados II — ADS 3º semestre, IFSP Capivari  
**Duração:** 4 aulas (≈ 200 min)  
**Pré-requisitos:** views, triggers de auditoria, importação CSV  
**SGBD:** PostgreSQL 12+

---

## 1. Objetivo da Aula

Ao final das 4 aulas, o aluno será capaz de:

- **Compreender** a diferença entre DO blocks, Functions e Procedures no PostgreSQL
- **Escrever** funções (functions) com parâmetros IN, OUT, INOUT e variadic
- **Criar** stored procedures usando `CREATE PROCEDURE`
- **Utilizar** DO blocks para scripts ad-hoc de administração
- **Implementar** lógica de negócio no nível do banco de dados usando PL/pgSQL
- **Decidir** quando usar cada construct com base no cenário prático

---

## 2. Estrutura de Tempo

| Aula | Tempo | Tópico |
|------|-------|--------|
| 1 | 50 min | DO Blocks + Introdução a Functions |
| 2 | 50 min | Functions — sintaxe, parâmetros, retorno |
| 3 | 50 min | Stored Procedures + Trigger Functions |
| 4 | 50 min | Hands-on integrado + Exercícios |

---

## 3. Conteúdo Teórico com Exemplos Práticos

### Bloco 1 — DO Blocks (Aula 1)

#### O que é um DO Block?
Um bloco anônimo de código PL/pgSQL que **não é armazenado como objeto** no banco. Útil para tarefas administrativas pontuais ou testes rápidos.

```sql
DO $$
DECLARE
  -- variáveis
  msg TEXT := 'Olá, PostgreSQL!';
BEGIN
  -- lógica
  RAISE NOTICE '%', msg;
END $$;
```

**Quando usar DO blocks:**
- Script de migração único
- Atualização massiva de dados sem reaproveitamento
- Teste rápido de lógica PL/pgSQL
- Automação de tarefas admin (criação de roles, schemas temporários)

#### Exemplo prático: Migrar emails para minúsculo

```sql
DO $$
DECLARE
  count_updated INTEGER;
BEGIN
  UPDATE usuarios
  SET email = LOWER(email)
  WHERE email != LOWER(email);

  GET DIAGNOSTICS count_updated = ROW_COUNT;
  RAISE NOTICE 'E-mails atualizados: %', count_updated;
END $$;
```

**Diferença-chave:** DO block = execução imediata, sem reuso, sem parâmetros de saída.

---

### Bloco 2 — Functions (Aula 2)

#### O que é uma Function?
Um **objeto armazenado no banco** que recebe parâmetros, executa lógica e **retorna** um valor (escalar ou conjunto de linhas). Pode ser usada em SELECT, WHERE, expressions.

#### Tipos de retorno

| Tipo | Exemplo de uso |
|------|---------------|
| `RETURNS tipo` | Retorna escalar (INTEGER, TEXT, BOOLEAN) |
| `RETURNS SETOF tabela%ROWTYPE` | Retorna conjunto de linhas |
| `RETURNS TABLE(colunas)` | Retorna tabela virtual |
| `RETURNS_trigger` | Usada em triggers (ver Trigger Functions) |

#### Parâmetros

```sql
-- Modo padrão: IN (recebe valor)
CREATE FUNCTION somar(a INTEGER, b INTEGER) RETURNS INTEGER AS $$
BEGIN
  RETURN a + b;
END;
$$ LANGUAGE plpgsql;

-- OUT: retorna valor sem ser no retorno principal
CREATE FUNCTION dividir(a NUMERIC, b NUMERIC, OUT resultado NUMERIC, OUT resto NUMERIC) AS $$
BEGIN
  resultado := a / b;
  resto := a % b;
END;
$$ LANGUAGE plpgsql;

-- INOUT: entrada e saída
CREATE FUNCTION swap(INOUT a INTEGER, INOUT b INTEGER) AS $$
DECLARE
  temp INTEGER;
BEGIN
  temp := a;
  a := b;
  b := temp;
END;
$$ LANGUAGE plpgsql;

-- VARIADIC: número variável de argumentos
CREATE FUNCTION sum_all(VARIADIC arr INTEGER[]) RETURNS INTEGER AS $$
DECLARE
  total INTEGER := 0;
BEGIN
  FOREACH total IN ARRAY arr LOOP
    total := total + total; -- simplificado
  END LOOP;
  RETURN total;
END;
$$ LANGUAGE plpgsql;
```

#### Exemplo prático: Calculadora de comissão

```sql
CREATE OR REPLACE FUNCTION calcular_comissao(
  p_venda NUMERIC(10,2),
  p_taxa NUMERIC(3,2) DEFAULT 0.05
) RETURNS NUMERIC(10,2) AS $$
BEGIN
  IF p_venda < 0 THEN
    RAISE EXCEPTION 'Venda não pode ser negativa: %', p_venda;
  END IF;
  RETURN p_venda * p_taxa;
END;
$$ LANGUAGE plpgsql STRICT;
```

**Uso:** `SELECT calcular_comissao(1000.00);` → `50.00`

#### Exemplo prático: Função que retorna conjunto de linhas

```sql
CREATE OR REPLACE FUNCTION get_clientes_por_cidade(p_cidade TEXT)
RETURNS TABLE(
  id INTEGER,
  nome TEXT,
  email TEXT
) AS $$
BEGIN
  RETURN QUERY
  SELECT c.id, c.nome, c.email
  FROM clientes c
  WHERE c.cidade ILIKE p_cidade;
END;
$$ LANGUAGE plpgsql;
```

**Uso:** `SELECT * FROM get_clientes_por_cidade('São Paulo');`

**Quando usar Functions:**
- Reutilização em múltiplos lugares (SELECT, WHERE, CHECK constraints)
- Retorno de valores (tabela, escalar)
- Composable (podem ser usadas em queries)
- Validação de dados, cálculos recorrentes

---

### Bloco 3 — Procedures (Aula 3)

#### O que é uma Procedure?
Um **objeto armazenado** similar a function, mas **não retorna valor diretamente**. Usada para operações que modificam estado do banco (INSERT/UPDATE/DELETE em massa, transações explícitas). Suporta `CALL`.

```sql
CREATE PROCEDURE atualizar_preco_produto(
  p_produto_id INTEGER,
  p_novo_preco NUMERIC(10,2)
) AS $$
BEGIN
  UPDATE produtos
  SET preco = p_novo_preco, data_atualizacao = CURRENT_TIMESTAMP
  WHERE id = p_produto_id;
END;
$$ LANGUAGE plpgsql;
```

**Chamada:** `CALL atualizar_preco_produto(42, 199.90);`

#### Por que Procedures e não Functions para modificações?

1. **Sem retorno** — procedures são mais honestas sobre sua intenção (mutação vs. computação)
2. **Transações explícitas** — procedures podem fazer COMMIT/ROLLBACK interno
3. **Melhor performance** — chamadas com CALL não precisam processar retorno

#### Exemplo prático: Procedure com transação

```sql
CREATE OR REPLACE PROCEDURE transferir_fundos(
  p_conta_origem INTEGER,
  p_conta_destino INTEGER,
  p_valor NUMERIC(12,2)
) AS $$
BEGIN
  IF p_valor <= 0 THEN
    RAISE EXCEPTION 'Valor deve ser positivo';
  END IF;

  UPDATE contas
  SET saldo = saldo - p_valor
  WHERE id = p_conta_origem
    AND saldo >= p_valor;

  IF NOT FOUND THEN
    RAISE EXCEPTION 'Saldo insuficiente ou conta origem inválida';
  END IF;

  UPDATE contas
  SET saldo = saldo + p_valor
  WHERE id = p_conta_destino;

  RAISE NOTICE 'Transferência de R$ % de % para % concluída', p_valor, p_conta_origem, p_conta_destino;
END;
$$ LANGUAGE plpgsql;
```

#### Procedures vs Functions — Resumo

| Característica | Function | Procedure |
|---------------|----------|-----------|
| Retorno | ✅ Sim (obrigatório) | ❌ Não |
| CALL | ❌ SELECT ou `SELECT ... INTO` | ✅ CALL |
| Transação | Não pode fazer COMMIT/ROLLBACK | Pode fazer COMMIT/ROLLBACK |
| Uso em SQL | ✅ Sim (expressions) | ❌ Não |
| Melhor para | Cálculos, validações, queries | Operações de mutação, batch |

#### Trigger Functions (revisão rápida conectado ao já aprendido)

Como já viram triggers de auditoria, revisar que trigger functions são Functions com `RETURNS TRIGGER`:

```sql
CREATE OR REPLACE FUNCTION fn_audit_usuarios()
RETURNS TRIGGER AS $$
BEGIN
  IF TG_OP = 'DELETE' THEN
    INSERT INTO audit_log (tabela, operacao, dado_antigo, usuario, data)
    VALUES ('usuarios', 'DELETE', row_to_json(OLD), SESSION_USER, NOW());
    RETURN OLD;
  END IF;
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;
```

---

## 4. Atividade Prática — Hands-on (Aula 4)

### Dataset base

Usar o schema e-commerce simplificado (clientes, produtos, pedidos) — ver script de setup no roteiro de prática.

```sql
-- Schema e-commerce simplificado (ver roteiro_pratica_blocks_functions_procedures.md)
CREATE TABLE categorias (
  id SERIAL PRIMARY KEY,
  nome VARCHAR(100) NOT NULL,
  created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE produtos (
  id SERIAL PRIMARY KEY,
  titulo VARCHAR(255) NOT NULL,
  categoria_id INTEGER REFERENCES categorias(id),
  preco NUMERIC(10,2) DEFAULT 0.00,
  created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE log_transferencias (
  id SERIAL PRIMARY KEY,
  origem_id INTEGER,
  acao VARCHAR(20),
  dados JSONB,
  usuario VARCHAR(100),
  created_at TIMESTAMP DEFAULT NOW()
);

-- Dados de exemplo
INSERT INTO categorias (nome) VALUES ('Ação'), ('Comédia'), ('Drama');
INSERT INTO produtos (nome, categoria, preco)
VALUES ('Velozes e Furiosos', 1, 12.90),
       ('O Pill', 2, 9.90),
       ('O Senhor dos Anéis', 3, 14.90),
       ('Matrix', 1, 13.90),
       ('Todo Mundo em Pânico', 2, 8.90);
```

### Exercícios

**Exercício 1 — DO Block (10 min)**  
Crie um DO block que:
- Conte quantos produtos existem na tabela `produtos`
- Calcule a média de preços
- Exiba uma mensagem formatada com os valores

```sql
-- [Gabarito]
DO $$
DECLARE
  total_produtos INTEGER;
  media_preco NUMERIC(10,2);
BEGIN
  SELECT COUNT(*), COALESCE(AVG(preco), 0) INTO total_produtos, media_preco
  FROM produtos;

  RAISE NOTICE 'Total de produtos: % | Preço médio: R$ %', total_produtos, media_preco::TEXT;
END $$;
```

**Exercício 2 — Function com OUT (15 min)**  
Crie uma function `estatisticas_categoria(p_categoria_id INTEGER)` que retorna:
- `total_produtos`: count de produtos
- `preco_medio`: preço médio
- `preco_max`: maior preço

```sql
-- [Gabarito]
CREATE OR REPLACE FUNCTION estatisticas_categoria(
  p_categoria_id INTEGER,
  OUT total_produtos BIGINT,
  OUT preco_medio NUMERIC(10,2),
  OUT preco_max NUMERIC(10,2)
) AS $$
BEGIN
  SELECT COUNT(*), COALESCE(AVG(preco), 0), COALESCE(MAX(preco), 0)
  INTO total_produtos, preco_medio, preco_max
  FROM produtos
  WHERE categoria_id = p_categoria_id;
END;
$$ LANGUAGE plpgsql;

-- Uso: SELECT * FROM estatisticas_categoria(1);
```

**Exercício 3 — Procedure com lógica transacional (20 min)**  
Crie uma procedure `sp_transferir_estoque(p_origem INTEGER, p_destino INTEGER, p_qtd INTEGER)` que:
- Verifique se ambos os produtos existem
- Atualize a categoria
- Registre a mudança em uma tabela `log_transferencias`
- Se película não existir, levante exceção

```sql
-- [Gabarito]
CREATE OR REPLACE PROCEDURE reatribuir_categoria(
  p_origem INTEGER,
    p_destino INTEGER,
    p_qtd INTEGER,
  p_nova_categoria_id INTEGER
) AS $$
DECLARE
  v_estoque INTEGER;
BEGIN
  -- Verifica se produto existe
  SELECT estoque INTO v_estoque FROM produtos WHERE id = p_origem;
  IF NOT FOUND THEN
    RAISE EXCEPTION 'Estoque insuficiente! Disponível: %', v_estoque;
  END IF;

  -- Atualiza categoria
  UPDATE produtos
  SET categoria_id = p_nova_categoria_id, created_at = NOW()
  WHERE id = p_origem;

  -- Log da operação
  INSERT INTO log_transferencias (origem_id, destino_id, quantidade, usuario)
  VALUES (
    p_origem,
    'CATEGORIA_ATUALIZADA',
    jsonb_build_object('nova_categoria_id', p_nova_categoria_id),
    SESSION_USER
  );

  RAISE NOTICE 'Transferidos % itens: #% → #%', p_qtd, p_origem, p_destino;
END;
$$ LANGUAGE plpgsql;

-- Uso: CALL reatribuir_categoria(3, 2);
```

**Desafio Extra (10 min — para alunos rápidos)**  
Crie uma function `produtos_por_faixa_preco(p_min NUMERIC, p_max NUMERIC)` que:
- Use `RETURNS TABLE` para retornar id, título, preço
- Use exception handling para validar que p_min <= p_max

```sql
-- [Gabarito]
CREATE OR REPLACE FUNCTION produtos_por_faixa_preco(
  p_min NUMERIC(10,2),
  p_max NUMERIC(10,2)
) RETURNS TABLE(id INTEGER, titulo TEXT, preco NUMERIC(10,2)) AS $$
BEGIN
  IF p_min > p_max THEN
    RAISE EXCEPTION 'Preço mínimo (%) não pode ser maior que máximo (%)', p_min, p_max;
  END IF;

  RETURN QUERY
  SELECT f.id, f.titulo, f.preco
  FROM produtos p
  WHERE f.preco BETWEEN p_min AND p_max;
END;
$$ LANGUAGE plpgsql;

-- Uso: SELECT * FROM produtos_por_faixa_preco(10.00, 15.00);
```

---

## 5. Conexão com o Mercado de Trabalho

### Onde isso é usado em produção?

| Cenário real | Construct |
|--------------|-----------|
| Migrar dados legados (script único) | DO block |
| Cálculo de comissões, impostos,Frete | Function |
| ProcessarBatch diário (batch) de pedidos | Procedure |
| Validação de dados em constraints | Function (CHECK) |
| Geração de relatórios complexos | Function (RETURN TABLE) |
| Rotinas de ETL (Extract-Transform-Load) | Procedure |
|Microsserviços de dados: regras de negócio centralizadas | Function |

### Oportunidades profissionais que exigem esse conhecimento

- **DBA Jr/Pleno**: escrever functions para rotinas de manutenção
- **Backend Developer**: entender como APIs consomem functions (ORMs como Hibernate, SQLAlchemy convertem chamadas para functions)
- **Data Engineer**: procedures para pipelines de dados
- **Analista de BI**: functions para views materializadas e relatórios

### Frameworks e ORMs que usam isso

- **PostgreSQL + Node.js**: `pg` library, Prisma, Sequelize
- **PostgreSQL + Python**: SQLAlchemy, Django ORM
- **PostgreSQL + Java**: JPA/Hibernate ( JPQL suporta functions)
- **PostgreSQL + C#**: Entity Framework Core, Dapper

**Exemplo real:** Um ecommerce pode ter 50+ functions para cálculo de frete, impostos, pontos fidelidade, todas chamadas via API sem expor a lógica SQL para o frontend.

---

## 6. Roteiro Resumido para o Professor

| Aula | Tempo | Atividade |
|------|-------|-----------|
| 1 | 10 min | Introdução + diferenças DO/Function/Procedure (quadro) |
| 1 | 25 min | Demonstração DO blocks + exemplos ao vivo |
| 1 | 15 min | Exercício 1 (DO block) |
| 2 | 10 min | Revisão + sintaxe completa de Functions |
| 2 | 20 min | Demonstração com diferentes tipos de retorno e parâmetros |
| 2 | 20 min | Exercício 2 (Function com OUT) |
| 3 | 10 min | Procedures vs Functions (comparação) |
| 3 | 25 min | Demonstração Procedure com transação |
| 3 | 15 min | Exercício 3 (Procedure) |
| 4 | 10 min | Revisão geral + Tirar dúvidas |
| 4 | 30 min | Exercícios 1, 2 e 3 resolvidos na prática |
| 4 | 10 min | Desafio Extra |

---

## 7. Materiais de Apoio

- **Documentação oficial**: https://www.postgresql.org/docs/current/plpgsql.html
- **Schema E-commerce simplificado**: ver `roteiro_pratica_blocks_functions_procedures.md`
- **Ferramenta prática**: `psql` para execução direta dos scripts

---

*Plano elaborado para a disciplina de Banco de Dados II — ADS 3º semestre — IFSP Capivari*