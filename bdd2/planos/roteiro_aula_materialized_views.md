# Roteiro de Aula: Materialized Views

**Disciplina**: Banco de Dados 2 — IFSP Capivari  
**Duração estimada**: 2 aulas (100 minutos)  
**Dataset**: Northwind com dados sintéticos (~500 mil itens)  
**Slides**: `bdd2/materialized_views.html`

---

## Pré-aula (antes dos alunos chegarem)

- [ ] Verificar se o PostgreSQL está rodando no laboratório
- [ ] Executar o script `02northwind_synthetic_data.sql` para gerar os dados sintéticos
- [ ] Confirmar que as tabelas `orders`, `order_details`, `customers` têm volume correto (~100k pedidos, ~500k itens)
- [ ] Abrir DBeaver/pgAdmin nos computadores dos alunos
- [ ] Abrir os slides no navegador

---

## AULA 1 — Teoria + Demonstração (50 min)

### Bloco 1: Contexto e Motivação (10 min)

**Slide: Capa (Materialized Views - Performance com Cache)**

> "Bom dia pessoal. Hoje vamos ver uma das técnicas mais usadas no mercado para otimizar consultas pesadas: Materialized Views."

**Slide: O que falaremos (Agenda)**

> "Vamos começar entendendo o problema, depois ver a solução na teoria e na prática."

**Slide: O Problema na Prática**

- Mostre a query de vendas por categoria
- Pergunte à turma: "Se essa query demora 5 segundos e a diretoria acessa o dashboard 200 vezes por dia, qual é o impacto?"
- **Resposta esperada**: consome recursos do servidor, experiência ruim para o usuário

**Slide: O Volume dos Nossos Dados**

> "Nós vamos trabalhar com dados reais de verdade. Geramos ~500 mil itens de pedido sobre o Northwind pra simular um cenário de empresa real."

- Garanta que os alunos entendam que 500k linhas é um volume modesto — sistemas reais têm milhões

**Slides: Por que essa query é lenta? (3 slides com animação)**

- Slide 1: Destaque os 3 JOINs — pergunte "por que JOIN é custoso?" (cada junção percorre tabelas)
- Slide 2: Destaque as agregações — "SUM e COUNT(DISTINCT) recalculam tudo do zero a cada execução"
- Slide 3: Transição — "E se rodássemos essa query UMA VEZ e guardássemos o resultado?"

> **Ponto de atenção**: Alunos podem não lembrar o que é JOIN. Se necessário, faça uma revisão rápida: "JOIN liga dados de duas tabelas usando uma chave estrangeira."

---

### Bloco 2: Conceito — View vs Materialized View (15 min)

**Slide: View Regular — Como funciona**

> "Uma view regular é só um atalho. Ela guarda a RECEITA, não o BOLO."

- Execute no DBeaver: `CREATE VIEW vw_vendas_categoria AS ...`
- Execute: `SELECT * FROM vw_vendas_categoria;`
- Pergunte: "Se eu alterar um pedido agora e rodar o SELECT de novo, o que acontece?" → Mostra o novo dado

**Slide: Materialized View — Como funciona**

> "A Materialized View guarda o BOLO PRONTO. Ela executou a query e guardou o resultado fisicamente."

- Execute: `CREATE MATERIALIZED VIEW mv_vendas_categoria AS ... WITH DATA;`
- Execute: `SELECT * FROM mv_vendas_categoria;`
- Destaque: "Vejam que o resultado é o mesmo, mas como chegamos lá é completamente diferente."

**Slide: Analogia do Restaurante**

> "View regular é como pedir no restaurante: sempre fresco, mas demora. Materialized view é o buffet: comida pronta, rápido, mas precisa repor."

- Deixe os alunos rirem do "buffet de dados" — isso ajuda a fixar o conceito
- Pergunte: "E o que seria o REFRESH no buffet?" → Reposição dos pratos

**Slide: View Regular vs Materialized View (tabela comparativa)**

- Leia cada linha da tabela com a turma
- Enfatize: "A MV ocupa espaço em disco — nada é de graça. É um trade-off: velocidade vs atualidade"

---

### Bloco 3: Sintaxe Detalhada (10 min)

**Slides: Criando uma MV — Passo a Passo (6 slides)**

> "Agora vamos dissecar cada parte do comando. Isso é importante porque no mercado vocês vão precisar escrever isso sem colar de stack overflow."

- Slide 1 (visão geral): "Vamos explorar cada linha..."
- Slide 2 (CREATE MATERIALIZED VIEW): Destaque a convenção `mv_` para nomes
- Slide 3 (SELECT): Explique cada coluna e por que tem alias
- Slide 4 (FROM + JOINs): "Quais tabelas estamos juntando? Por quê?"
- Slide 5 (GROUP BY): Relembre: "GROUP BY é obrigatório quando temos SUM, COUNT"
- Slide 6 (WITH DATA): "Se esquecerem o WITH DATA, a MV cria vazia. Já vi DBA sênior errar isso."

> **Pergunta para a turma**: "O que acontece se eu criar com WITH NO DATA?" → MV fica vazia, precisa de REFRESH antes de consultar.

---

### Bloco 4: Performance e REFRESH (15 min)

**Slide: Performance: Números Reais**

- Execute ao vivo no DBeaver:
  - `EXPLAIN ANALYZE SELECT * FROM vw_vendas_categoria;` → ~3000ms
  - `EXPLAIN ANALYZE SELECT * FROM mv_vendas_categoria;` → ~20ms
- Deixe os alunos verem os números reais no tela

> "150x mais rápido. Isso é a diferença entre 'carregando...' e 'pronto'."

**Slide: Como provar? EXPLAIN ANALYZE**

> "Anotem isso: EXPLAIN ANALYZE é o seu melhor amigo para medir performance. Mostra o plano de execução E o tempo real."

**Slide: REFRESH**

> "A MV não atualiza sozinha. É como o buffet: se ninguém repõe, a comida acaba."

- Execute: `REFRESH MATERIALIZED VIEW mv_vendas_categoria;`
- Destaque: "Durante o REFRESH, ninguém consegue ler a MV — ela fica travada."

**Slides: REFRESH CONCURRENTLY (2 slides)**

> "Para resolver o bloqueio, existe o REFRESH CONCURRENTLY. Mas tem um preço: precisa de índice único."

- Tente executar sem o índice para mostrar o erro:
  `REFRESH MATERIALIZED VIEW CONCURRENTLY mv_vendas_categoria;`
- Mostre o erro na tela
- Crie o índice único e execute novamente

> **Momento "aha!"**: Os alunos veem o erro acontecer e a solução em tempo real.

**Slide: REFRESH — Comparação (tabela)**

- Leia a tabela comparativa rapidamente
- Sintetize: "REFRESH comum pra batch noturno, CONCURRENTLY pra produção durante o dia"

---

## AULA 2 — Prática Guiada (50 min)

### Bloco 5: Setup e Recap (5 min)

**Slide: Capa Prática Guiada**

> "Agora é mão na massa. Abram o DBeaver e conectem no banco Northwind."

**Slide: Recap Rápido**

- Leitura rápida da tabela comparativa
- Mostre a sintaxe básica novamente

**Slide: Setup do Ambiente**

> "Se alguém não tem os dados sintéticos carregados, me avisa agora. Precisamos dos ~500 mil itens."

---

### Bloco 6: Prática 1 — Dashboard de Vendas (15 min)

**Slide: Prática 1 — O Problema**

> "Primeiro, vamos ver o volume de dados e sentir na pele a lentidão."

- Peça para os alunos executarem o COUNT e a query lenta
- Cada aluno deve anotar o tempo do EXPLAIN ANALYZE

**Slides: Prática 1 — Criando a MV (2 slides)**

- Passo 1: Alunos criam a MV
- Passo 2: Alunos comparam os tempos

> "Quem teve mais de 100x de diferença? Levanta a mão."

**Slide: Prática 1 — Verifique o Resultado**

- Alunos consultam a MV e comparam com a view regular
- Circule pela sala verificando se todos conseguiram

> **Dificuldade antecipada**: Alguns alunos podem esquecer o `WITH DATA`. Se a MV estiver vazia, esse é o motivo.

---

### Bloco 7: Prática 2 — Desempenho de Funcionários (10 min)

**Slide: Prática 2 — Cenário**

> "Agora o RH quer saber quem vende mais. Mesma lógica: view regular vs MV."

**Slides: Prática 2 — Criando a MV**

- Alunos criam a view e a MV de desempenho de funcionários
- Destaque o uso de `LEFT JOIN` — "por que LEFT e não INNER?" → Para incluir funcionários sem pedidos

**Slide: Adicionando Índices**

> "Agora o segredo: índices na MV. Vai ficar ainda mais rápido."

- Alunos criam os índices
- Destaque: "Índice único é obrigatório se quiser usar CONCURRENTLY"

**Slide: Medindo o Ganho dos Índices**

- Compare: view regular (~3000ms) → MV sem índice (~120ms) → MV com índice (~8ms)
> "Três ordens de magnitude de diferença. É como ir de carro de boi a Foguete."

---

### Bloco 8: REFRESH na Prática + Agendamento (10 min)

**Slide: Praticando o REFRESH**

> "Vamos provar que a MV não atualiza sozinha."

- Peça para os alunos inserirem um pedido novo
- Consultar a MV — o pedido NÃO aparece
- Dar REFRESH
- Consultar novamente — agora aparece

> **Momento-chave**: Os alunos VEEM que a MV está desatualizada e depois VEEM o REFRESH corrigir. Isso fixa o conceito.

**Slide: REFRESH CONCURRENTLY na Prática**

- Alunos testam o CONCURRENTLY

**Slides: Agendamento (pg_cron e crontab)**

> "No mundo real, ninguém fica digitando REFRESH manualmente. Agendamos."

- Mostre rapidamente os dois métodos
- Não precisa executar — só mostrar que é possível

**Slide: Monitorando suas MVs**

> "Como saber se sua MV está ocupando muito espaço? Essas queries aqui são úteis."

---

### Bloco 9: Snapshot — Materialized View como Fotografia (10 min)

**Slide: Materialized Views como Snapshot**

> "Agora vamos ver um terceiro uso das MVs que muita gente esquece: como fotografia dos dados."

**Slide: O Problema do Tempo**

> "Imagina: a diretoria pede o relatório de março. Você roda no dia 5 de abril. Mas alguém cancelou pedidos entre o fechamento e hoje. O relatório está ERRADO."

- Pergunte: "Como garantir que o relatório mostre os dados como estavam no dia 31/03?"

**Slide: View Regular Não Resolve**

> "View não serve porque ela sempre mostra o estado ATUAL. Se o dado foi alterado, a view mostra a alteração."

**Slide: Snapshot = Fotografia dos Dados**

- Use a analogia visual: 📷 foto vs 🎥 câmera ao vivo
> "MV congelada no momento da criação = fotografia. View = câmera ao vivo."

**Slide: Criando um Snapshot**

- Mostre o SQL com `snapshot_en` (timestamp)
- Execute ao vivo se possível

**Slide: Regra de Ouro do Snapshot**

> "E aqui está a regra mais importante: **NUNCA dê REFRESH em um snapshot**. Se der REFRESH, você tira uma foto nova e perde a original."

- Pergunte: "Por que REFRESH destrói o snapshot?" → Porque substitui os dados antigos pelo estado atual

**Slide: Três Usos de Materialized Views (tabela)**

| | View Regular | MV (cache) | MV (snapshot) |
|---|---|---|---|
| Dados | Tempo real | Cache periódico | Congelados |
| Refresh | N/A | Periódico | **Nunca** |
| Uso | Abstração | Performance | Auditoria |

> "Então vimos hoje TRÊS papéis: view pra abstração, MV pra performance, MV-snapshot pra auditoria/compliance."

**Slide: Quando Usar Snapshot?**

- Casos: fechamento contábil, auditoria, compliance fiscal, ranking congelado
> "No mercado, o fechamento mensal de uma empresa É um snapshot. Ninguém pode alterar os dados depois que o mês fechou."

**Slide: Reflexão**

- Leia o cenário do estorno de R$ 15.000
- Deixe os alunos discutirem em dupla por 2 minutos
- Peça respostas de 2-3 duplas

---

### Encerramento (5 min)

**Slide: Exercício Livre**

> "Para quem terminar cedo, tem um exercício de análise de fornecedores. Quem quiser pode entregar."

**Slide: Checklist de Aprendizado**

- Leia rapidamente cada item
> "Se vocês sabem fazer tudo nessa lista, estão prontos para usar MVs no mercado."

**Slide: Resumo Final**

> "Sintetizando: View = atalho. MV = tabela física com resultado. Ganho: 100-400x mais rápido. Trade-off: velocidade vs atualidade."

**Slide: Próxima Aula — Triggers**

> "Na próxima aula vamos ver Triggers. E adivinhem: triggers podem atualizar MVs automaticamente quando os dados base mudam."

**Slide: Dúvidas?**

- Responda perguntas
- Deixe os links da documentação do PostgreSQL

---

## Notas para o Professor

### Dificuldades antecipadas dos alunos:

1. **Esquecer WITH DATA** — MV cria vazia, SELECT retorna erro. Solução: mostrar o erro e explicar
2. **Não entender o trade-off** — Alunos podem achar que MV é "sempre melhor". Reforce: MV não é atualizada em tempo real
3. **REFRESH CONCURRENTLY sem índice único** — Vai dar erro. Isso é intencional e pedagógico
4. **Confundir MV-snapshot com MV-cache** — Enfatize a diferença: uma NUNCA recebe REFRESH, a outra recebe periodicamente

### Tempo sugerido por bloco:

| Bloco | Conteúdo | Tempo |
|---|---|---|
| 1 | Contexto e Motivação | 10 min |
| 2 | Conceito View vs MV | 15 min |
| 3 | Sintaxe Detalhada | 10 min |
| 4 | Performance e REFRESH | 15 min |
| — | *Intervalo* | — |
| 5 | Setup e Recap | 5 min |
| 6 | Prática 1: Dashboard | 15 min |
| 7 | Prática 2: Funcionários + Índices | 10 min |
| 8 | REFRESH + Agendamento | 10 min |
| 9 | Snapshot | 10 min |
| — | Encerramento | 5 min |

### Material de apoio:

- **Prática escrita**: `bdd2/pratica_materialized_views.md`
- **Diagrama ER**: `bdd2/diagrama_er_delivery.png` (para atividade futura)
- **Scripts SQL**: `bdd2/01northwind.sql` e `bdd2/02northwind_synthetic_data.sql`
- **Slides**: `bdd2/materialized_views.html`
