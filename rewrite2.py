import re

with open('bdd2/aula15-duckdb-analise-colunar.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Slide: "OLTP: trabalho transacional"
oltp_orig = r'<h2>OLTP: trabalho transacional</h2>\s*<div class="cyan-box">\s*<p><strong>OLTP</strong> vem de <em>Online Transaction Processing</em>: processamento de transacoes online\.\s*</p>\s*</div>\s*<multi-col style="gap:15px">\s*<div style="flex:1">\s*<h3>Exemplos</h3>\s*<ul>\s*<li>Cadastro de usuarios</li>\s*<li>Registro de pedidos</li>\s*<li>Atualizacao de estoque</li>\s*<li>Login e sessoes</li>\s*</ul>\s*</div>\s*<div style="flex:1">\s*<h3>Caracteristica</h3>\s*<div class="box">\s*<p>Muitas operacoes pequenas, frequentes, concorrentes e com cuidado forte de integridade\.</p>\s*</div>\s*<p><span class="pill">Exemplo</span> PostgreSQL atendendo uma aplicacao web\.</p>\s*</div>\s*</multi-col>'

oltp_new = '''<h2>OLTP: trabalho transacional</h2>
          <div class="cyan-box" style="margin-bottom: 20px;">
            <p><strong>OLTP</strong> vem de <em>Online Transaction Processing</em>: processamento de transacoes online.</p>
          </div>
          
          <div class="flow-row" style="margin-bottom: 20px;">
            <div class="flow-node">
              <i class="fa-solid fa-mobile-screen-button fa-2x" style="color: #bd93f9; margin-bottom: 10px;"></i>
              <strong style="color: #f8f8f2;">App Web / Mobile</strong>
              <span>(Milhares de acessos)</span>
            </div>
            <div class="flow-arrow">↔</div>
            <div class="flow-node" style="border-color: #336791; background: rgba(51, 103, 145, 0.1);">
              <img src="../img/postgres_logo.svg" alt="PostgreSQL" style="height: 50px; margin-bottom: 10px; filter: drop-shadow(0 4px 6px rgba(0,0,0,0.5));" />
              <strong style="color: #8be9fd;">PostgreSQL</strong>
              <span>(Transacional)</span>
            </div>
            <div class="flow-arrow">↔</div>
            <div class="flow-node">
              <i class="fa-solid fa-table-list fa-2x" style="color: #f1fa8c; margin-bottom: 10px;"></i>
              <strong style="color: #f8f8f2;">Registros Singulares</strong>
              <span>(Ex: Pedido #1234)</span>
            </div>
          </div>
          
          <div class="artifact-card" style="border-top: 4px solid #bd93f9;">
             <h3 style="color: #bd93f9;"><i class="fa-solid fa-bolt"></i> Caracteristicas</h3>
             <p style="font-size: 0.65em; margin:0;">Muitas operacoes pequenas, frequentes, concorrentes e com cuidado forte de integridade (Ex: Cadastro, Login, Compras).</p>
          </div>'''
content = re.sub(oltp_orig, oltp_new, content)

# 2. Slide: "OLAP: trabalho analitico"
olap_orig = r'<h2>OLAP: trabalho analitico</h2>\s*<div class="cyan-box">\s*<p><strong>OLAP</strong> vem de <em>Online Analytical Processing</em>: processamento analitico online\.</p>\s*</div>\s*<multi-col style="gap:15px">\s*<div style="flex:1">\s*<h3>Perguntas comuns</h3>\s*<ul>\s*<li>Total de vendas por mes</li>\s*<li>Media de notas por turma</li>\s*<li>Acessos por cidade</li>\s*<li>Comparacao entre categorias</li>\s*</ul>\s*</div>\s*<div style="flex:1\.2">\s*<code-block lang="sql" data-trim>\s*SELECT produto, SUM\(valor\) AS total\s*FROM vendas\s*GROUP BY produto\s*ORDER BY total DESC;\s*</code-block>\s*<div class="green-box">\s*<p>A consulta percorre muitos registros e devolve um resumo\.</p>\s*</div>\s*</div>\s*</multi-col>'

olap_new = '''<h2>OLAP: trabalho analitico</h2>
          <div class="cyan-box" style="margin-bottom: 20px;">
            <p><strong>OLAP</strong> vem de <em>Online Analytical Processing</em>: processamento analitico online.</p>
          </div>
          
          <div class="flow-row" style="margin-bottom: 20px;">
            <div class="flow-node" style="border-color: #50fa7b; background: rgba(80, 250, 123, 0.1);">
              <img src="../img/parquet_logo.svg" alt="Apache Parquet" style="height: 50px; margin-bottom: 10px; filter: drop-shadow(0 4px 6px rgba(0,0,0,0.5));" />
              <strong style="color: #50fa7b;">Data Lake / Arquivos</strong>
              <span>(Milhoes de registros)</span>
            </div>
            <div class="flow-arrow">→</div>
            <div class="flow-node duckdb-node">
              <img src="planos/aula15_duckdb_assets/duckdb-logo-stacked.svg" alt="DuckDB" style="height: 50px; margin-bottom: 10px;" />
              <strong style="color: #fff100;">DuckDB</strong>
              <span>(Motor Analitico)</span>
            </div>
            <div class="flow-arrow">→</div>
            <div class="flow-node">
              <i class="fa-solid fa-chart-pie fa-2x" style="color: #ff79c6; margin-bottom: 10px;"></i>
              <strong style="color: #f8f8f2;">Dashboard / BI</strong>
              <span>(Visao Resumida)</span>
            </div>
          </div>
          
          <div class="artifact-card" style="border-top: 4px solid #50fa7b;">
             <h3 style="color: #50fa7b;"><i class="fa-solid fa-calculator"></i> Caracteristicas</h3>
             <p style="font-size: 0.65em; margin:0;">Percorre muitos registros filtrando e agrupando para devolver um resumo (Ex: Total de vendas por mes, Media de notas).</p>
          </div>'''
content = re.sub(olap_orig, olap_new, content)

# 3. Slide: "Hive partitioning"
hive_orig = r'<h2>Hive partitioning</h2>\s*<p>Em data lakes, o valor de algumas colunas aparece no proprio caminho do arquivo\.</p>\s*<pre class="file-tree">dados/vendas/\s*ano=2026/\s*mes=01/\s*vendas_01\.parquet\s*mes=02/\s*vendas_02\.parquet</pre>\s*<div class="cyan-box">\s*<p>As pastas <code>ano=2026</code> e <code>mes=01</code> representam colunas virtuais extraidas do caminho\.\s*</p>\s*</div>'

hive_new = '''<h2>Hive partitioning</h2>
          <div style="display: flex; align-items: center; justify-content: center; margin-bottom: 15px;">
            <img src="../img/hive_logo.svg" alt="Apache Hive" style="height: 80px; filter: drop-shadow(0 4px 6px rgba(0,0,0,0.3));" />
          </div>
          <p>Esta convencao de pastas nasceu no Apache Hive (Hadoop) e virou padrao na industria.</p>
          <pre class="file-tree">dados/vendas/
  ano=2026/
    mes=01/
      vendas_01.parquet
    mes=02/
      vendas_02.parquet</pre>
          <div class="cyan-box">
            <p>O <strong>DuckDB</strong> le este padrao nativamente. As pastas <code>ano=2026</code> e <code>mes=01</code> viram colunas virtuais na consulta.</p>
          </div>'''
content = re.sub(hive_orig, hive_new, content)

# 4. Slide: "ETL direto entre fontes"
etl_orig = r'<h2>ETL direto entre fontes</h2>\s*<p>Podemos transferir dados do Postgres para o DuckDB \(ou vice-versa\) sem arquivos intermediarios\.</p>\s*<code-block lang="sql" data-trim>\s*-- Copiar de CSV para Postgres\s*INSERT INTO pg\.public\.vendas\s*SELECT \* FROM read_csv\(\'novos_dados\.csv\'\);\s*-- Consolidar Parquet e salvar no Postgres\s*INSERT INTO pg\.public\.resumo_mensal\s*SELECT\s*DATE_TRUNC\(\'month\', data\) AS mes,\s*categoria,\s*SUM\(valor\) AS total\s*FROM read_parquet\(\'dados/\*\*/\*\.parquet\'\)\s*GROUP BY mes, categoria;\s*</code-block>\s*<div class="yellow-box">\s*<p>Um script DuckDB le arquivos locais, agrega e salva o resultado diretamente em uma tabela PostgreSQL —\s*sem arquivo intermediario\.</p>\s*</div>'

etl_new = '''<h2>ETL direto entre fontes</h2>
          <div class="flow-row" style="margin-bottom: 15px;">
            <div class="flow-node">
              <img src="../img/parquet_logo.svg" alt="Parquet" style="height: 40px; margin-bottom: 10px;" />
              <strong style="color: #f8f8f2;">Parquet / CSV</strong>
            </div>
            <div class="flow-arrow">→</div>
            <div class="flow-node duckdb-node">
              <img src="planos/aula15_duckdb_assets/duckdb-logo-stacked.svg" alt="DuckDB" style="height: 40px; margin-bottom: 10px;" />
              <strong style="color: #fff100;">Agrega (Em Memoria)</strong>
            </div>
            <div class="flow-arrow">→</div>
            <div class="flow-node" style="border-color: #336791;">
              <img src="../img/postgres_logo.svg" alt="PostgreSQL" style="height: 40px; margin-bottom: 10px;" />
              <strong style="color: #8be9fd;">PostgreSQL</strong>
            </div>
          </div>
          <code-block lang="sql" data-trim>
            -- Consolidar milhares de Parquets e salvar o resumo no Postgres
            INSERT INTO pg.public.resumo_mensal
            SELECT
            DATE_TRUNC('month', data) AS mes,
            categoria,
            SUM(valor) AS total
            FROM read_parquet('dados/**/*.parquet')
            GROUP BY mes, categoria;
          </code-block>
          <div class="yellow-box" style="margin-top: 5px;">
            <p>O DuckDB atua como motor ETL: processa arquivos e envia o resumo pronto ao banco transacional, sem gerar arquivos temporarios.</p>
          </div>'''
content = re.sub(etl_orig, etl_new, content)

# 5. Slide: "Mapa mental da disciplina"
mapa_orig = r'<h2>Mapa mental da disciplina</h2>\s*<ul>\s*<li><strong>PostgreSQL:</strong> banco relacional completo para aplicacoes</li>\s*<li><strong>Redis:</strong> suporte operacional rapido em memoria</li>\s*<li><strong>MongoDB:</strong> documentos flexiveis semelhantes a JSON</li>\s*<li><strong>Neo4j:</strong> relacoes, caminhos e grafos</li>\s*<li><strong>DuckDB:</strong> motor SQL analitico local — arquivos, DataFrames e ponte para PostgreSQL</li>\s*</ul>\s*<div class="green-box fragment">\s*<p>A mesma linguagem SQL pode participar de sistemas transacionais, de analises locais e de integracao entre\s*ferramentas\.</p>\s*</div>'

mapa_new = '''<h2>Mapa mental da disciplina</h2>
          <div class="artifact-grid" style="grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 10px; margin-bottom: 15px;">
            <div class="artifact-card" style="border-top: 4px solid #336791; text-align: center;">
              <img src="../img/postgres_logo.svg" alt="PostgreSQL" style="height: 40px; margin-bottom: 5px;" />
              <h3 style="color: #8be9fd; font-size: 0.6em;">PostgreSQL</h3>
              <p style="font-size: 0.5em; margin:0;">Relacional / Transacional. A fonte da verdade para apps.</p>
            </div>
            <div class="artifact-card" style="border-top: 4px solid #ff5555; text-align: center;">
              <i class="fa-solid fa-server fa-3x" style="color: #ff5555; margin-bottom: 5px;"></i>
              <h3 style="color: #ff5555; font-size: 0.6em;">Redis</h3>
              <p style="font-size: 0.5em; margin:0;">Chave-Valor na memória. Cache e fila de alta velocidade.</p>
            </div>
            <div class="artifact-card" style="border-top: 4px solid #50fa7b; text-align: center;">
              <i class="fa-solid fa-leaf fa-3x" style="color: #50fa7b; margin-bottom: 5px;"></i>
              <h3 style="color: #50fa7b; font-size: 0.6em;">MongoDB</h3>
              <p style="font-size: 0.5em; margin:0;">Documentos flexíveis JSON. Catálogos e dados aninhados.</p>
            </div>
            <div class="artifact-card" style="border-top: 4px solid #bd93f9; text-align: center;">
              <i class="fa-solid fa-circle-nodes fa-3x" style="color: #bd93f9; margin-bottom: 5px;"></i>
              <h3 style="color: #bd93f9; font-size: 0.6em;">Neo4j</h3>
              <p style="font-size: 0.5em; margin:0;">Grafos e Relacionamentos. Redes sociais e recomendações.</p>
            </div>
            <div class="artifact-card" style="border-top: 4px solid #f1fa8c; text-align: center; grid-column: span 2;">
              <img src="planos/aula15_duckdb_assets/duckdb-logo-stacked.svg" alt="DuckDB" style="height: 40px; margin-bottom: 5px;" />
              <h3 style="color: #f1fa8c; font-size: 0.6em;">DuckDB</h3>
              <p style="font-size: 0.5em; margin:0;">Analítico local (OLAP). Ponte SQL entre DataFrames, arquivos Parquet/CSV e bancos (ETL).</p>
            </div>
          </div>
          <div class="green-box fragment">
            <p>O <strong>SQL</strong> é a linguagem universal que cruza essas ferramentas, seja para consultas simples (OLTP) ou analíticas (OLAP).</p>
          </div>'''
content = re.sub(mapa_orig, mapa_new, content)

with open('bdd2/aula15-duckdb-analise-colunar.html', 'w', encoding='utf-8') as f:
    f.write(content)
print('Done!')
