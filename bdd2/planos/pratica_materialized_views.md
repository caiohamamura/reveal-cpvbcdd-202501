# Prática: Materialized Views

**Banco de Dados 2 — IFSP Capivari**
**Dataset**: Northwind Traders

---

## Tarefa 1 — Investigação (individual)

Antes de escrever qualquer SQL, responda no seu caderno:

1. O que acontece quando você executa `SELECT * FROM uma_view`? O banco reexecuta a query inteira ou lê dados armazenados? **Justifique sua resposta.**

2. Imagine que você tem uma view que junta 5 tabelas e calcula médias. Ela é executada 200x por dia por diferentes setores da empresa. Qual é o problema? **Explique com suas palavras.**

3. Se uma view "salva" o resultado em disco, o que acontece quando os dados originais mudam? **Desenhe um diagrama simples mostrando a relação entre tabela base → materialized view → usuário.**

**Entrega**: Discussão com o professor.

---

## Tarefa 2 — Construção guiada

Usando o banco **Northwind**, crie uma view regular que mostre **vendas por produto** com as seguintes informações:

- Nome do produto
- Categoria
- Fornecedor
- Quantidade total vendida
- Valor total em reais
- Quantidade de pedidos únicos

**Requisitos**:
- Use pelo menos 4 tabelas (você descobre quais)
- Agrupe por produto, categoria e fornecedor
- Ordene pelo maior valor total

Depois de criar, execute `EXPLAIN ANALYZE` e **anote o tempo**:

> Tempo da view regular: _________ ms

---

## Tarefa 3 — Otimização com Materialized View

Agora transforme a view da Tarefa 2 em uma **materialized view** com o nome `mv_relatorio_vendas`.

**Requisitos adicionais**:
- Adicione uma coluna `data_atualizacao` com a data atual (para saber quando os dados foram gerados)
- Crie **dois índices** na materialized view. Você decide quais colunas indexar — justifique sua escolha abaixo:

> Índice 1: coluna _________ — por quê? ____________________
> Índice 2: coluna _________ — por quê? ____________________

Execute `EXPLAIN ANALYZE` e anote:

> Tempo da materialized view: _________ ms

---

## Tarefa 4 — Análise comparativa

Preencha e **explique**:

| | View regular | Materialized view |
|---|---|---|
| Tempo de consulta | | |
| O que o banco faz internamente? | | |
| Dados estão atualizados? | | |

**Pergunta**: Se um novo pedido foi inserido na tabela `orders` após a criação da MV, esse pedido aparece na MV? Por quê?

> Resposta: ___________________________________________________

---

## Tarefa 5 — Refresh: quando e como?

Um analista da Northwind precisa que o relatório seja atualizado. Ele considerou duas opções:

**Opção A**: `REFRESH MATERIALIZED VIEW mv_relatorio_vendas;`
**Opção B**: `REFRESH MATERIALIZED VIEW CONCURRENTLY mv_relatorio_vendas;`

Responda:

1. Qual a diferença prática entre as duas opções?

2. A Opção B tem um pré-requisito. **Descubra qual é** testando no banco (vai dar erro). O que o erro diz? O que você precisa fazer para resolver?

> Erro encontrado: _____________________________________________
> Solução: ____________________________________________________

3. Em qual cenário real cada opção seria melhor? Dê um exemplo para cada.

> Opção A é melhor quando: ____________________________________
> Opção B é melhor quando: ____________________________________

---

## Tarefa 6 — Desafio

A diretoria da Northwind quer um **novo relatório** de desempenho de funcionários com:

- Nome completo do funcionário
- Total de pedidos atendidos
- Valor total vendido
- Quantidade de clientes distintos atendidos
- Ticket médio por pedido

**Você deve**:
1. Criar uma view regular com esses dados
2. Criar uma materialized view equivalente
3. Comparar os tempos
4. Escolher **um índice** para a MV e justificar por quê

> View regular: _________ ms
> Materialized view: _________ ms
> Índice criado: _________ — justificativa: ____________________

---

## Tarefa 7 — Materialized View como Snapshot Momentâneo

Uma materialized view funciona como uma **fotografia** dos dados em um instante específico. Ela "congela" o resultado de uma query no momento em que foi criada (ou do último REFRESH).

### Discussão em dupla

Imagine o seguinte cenário:

> A diretoria da empresa pediu um relatório de vendas do mês passado para apresentar na reunião de resultados trimestrais. O relatório precisa mostrar **exatamente** os dados como estavam no dia 31/03 às 23h59.

**Perguntas:**

1. Por que uma view regular **não** serviria para esse caso? O que aconteceria se alguém alterasse ou deletasse um pedido depois do dia 31/03?

> ___________________________________________________________

2. Como uma materialized view resolve esse problema? Explique o conceito de "snapshot" com suas palavras.

> ___________________________________________________________

3. Crie uma materialized view chamada `mv_snapshot_mensal` que registre as vendas do **último dia do mês anterior**. Inclua uma coluna `snapshot_em` com o timestamp exato da criação.

```sql
-- Escreva sua query aqui:



```

4. **Importante**: Depois de criada, essa MV deve **NUNCA** receber REFRESH. Por quê? O que aconteceria com os dados do snapshot se alguém executasse REFRESH nela?

> ___________________________________________________________

5. Que outras situações reais exigiriam um snapshot? Dê pelo menos 2 exemplos:

> Exemplo 1: _________________________________________________
> Exemplo 2: _________________________________________________

---

## Tarefa 8 — Reflexão final (entregar por escrito)

Responda em 3-5 linhas cada:

1. **Por que uma empresa real usaria materialized views?** Dê pelo menos 2 motivos concretos.

2. **Qual o risco** de depender de materialized views em um sistema? Dê um exemplo de problema real que poderia acontecer.

3. **Se você fosse o DBA** da Northwind, que estratégia de refresh usaria? Com que frequência? Justifique considerando que o sistema tem picos de vendas durante o dia.

---

## Checklist de entrega

- [ ] Tarefa 1: discussão registrada
- [ ] Tarefa 2: view regular criada e tempo anotado
- [ ] Tarefa 3: MV criada com 2 índices justificados
- [ ] Tarefa 4: tabela comparativa preenchida com explicações
- [ ] Tarefa 5: erro do CONCURRENTLY investigado e resolvido
- [ ] Tarefa 6: MV de funcionários com comparação de tempo
- [ ] Tarefa 7: snapshot discutido e MV de snapshot criada
- [ ] Tarefa 8: reflexão escrita entregue
