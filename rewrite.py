import re

with open('bdd2/aula15-duckdb-analise-colunar.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Slide 1
slide1_orig = r'<h2>1\. Criar tabela a partir do arquivo</h2>\s*<code-block lang="python" data-trim>'
slide1_new = '''<h2>1. Criar tabela a partir do arquivo</h2>
          <div class="flow-row" style="margin: 0 0 15px 0;">
            <div class="flow-node">
              <i class="fa-solid fa-file-csv fa-2x" style="color: #ff5555; margin-bottom: 10px;"></i>
              <strong style="color: #f8f8f2;">vendas.csv</strong>
              <span>Disco local</span>
            </div>
            <div class="flow-arrow">→</div>
            <div class="flow-node duckdb-node">
              <i class="fa-solid fa-table fa-2x" style="color: #fff100; margin-bottom: 10px;"></i>
              <strong style="color: #f8f8f2;">Tabela vendas</strong>
              <span>Memória (DuckDB)</span>
            </div>
          </div>
          <code-block lang="python" data-trim>'''
content = re.sub(slide1_orig, slide1_new, content)

# 2. Slide 2
slide2_orig = r'<div style="flex:1">\s*<div class="box">\s*<p>Antes de responder perguntas, precisamos saber:</p>\s*<ul>\s*<li>quais colunas existem</li>\s*<li>quais tipos foram detectados</li>\s*<li>quantas linhas temos</li>\s*<li>se os dados parecem coerentes</li>\s*</ul>\s*</div>\s*</div>'
slide2_new = '''<div style="flex:1">
              <div class="artifact-card" style="border-top: 4px solid #bd93f9; height: 100%;">
                <h3 style="color: #bd93f9; display: flex; align-items: center; gap: 8px;">
                  <i class="fa-solid fa-magnifying-glass"></i> O que buscar?
                </h3>
                <ul style="list-style-type: none; padding: 0; margin: 10px 0 0 0;">
                  <li style="margin-bottom: 12px;"><i class="fa-solid fa-table-columns" style="color: #8be9fd; width: 24px;"></i> <strong>Colunas:</strong> quais nomes e campos existem?</li>
                  <li style="margin-bottom: 12px;"><i class="fa-solid fa-fingerprint" style="color: #8be9fd; width: 24px;"></i> <strong>Tipos:</strong> foram detectados corretamente?</li>
                  <li style="margin-bottom: 12px;"><i class="fa-solid fa-list-ol" style="color: #8be9fd; width: 24px;"></i> <strong>Volume:</strong> quantas linhas temos no total?</li>
                  <li style="margin-bottom: 12px;"><i class="fa-solid fa-eye" style="color: #8be9fd; width: 24px;"></i> <strong>Coerência:</strong> os dados fazem sentido visualmente?</li>
                </ul>
              </div>
            </div>'''
content = re.sub(slide2_orig, slide2_new, content)

# 3. Slide 3
slide3_orig = r'<h2>3\. Agregar</h2>\s*<code-block lang="sql" data-trim>\s*SELECT\s*categoria,\s*AVG\(valor\) AS media,\s*SUM\(valor\) AS total\s*FROM vendas\s*GROUP BY categoria\s*ORDER BY total DESC;\s*</code-block>\s*<code-block lang="sql" data-trim>\s*SELECT produto, COUNT\(\*\) AS quantidade\s*FROM vendas\s*GROUP BY produto\s*ORDER BY quantidade DESC;\s*</code-block>'
slide3_new = '''<h2>3. Agregar</h2>
          <multi-col style="gap:15px">
            <div style="flex:1">
              <code-block lang="sql" data-trim>
                SELECT
                categoria,
                AVG(valor) AS media,
                SUM(valor) AS total
                FROM vendas
                GROUP BY categoria
                ORDER BY total DESC;
              </code-block>
              <code-block lang="sql" data-trim>
                SELECT produto, COUNT(*) AS quantidade
                FROM vendas
                GROUP BY produto
                ORDER BY quantidade DESC;
              </code-block>
            </div>
            <div style="flex:1; display: flex; flex-direction: column; justify-content: center;">
              <div class="artifact-card" style="border-top: 4px solid #f1fa8c; margin-top: 15px;">
                <h3 style="color: #f1fa8c; display: flex; align-items: center; gap: 8px; font-size: 0.6em; margin-bottom: 10px;">
                  <i class="fa-solid fa-compress"></i> Resumo (Exemplo)
                </h3>
                <table class="mini-table" style="width: 100%; font-size: 0.5em; text-align: right;">
                  <thead>
                    <tr><th style="text-align: left;">categoria</th><th>media</th><th>total</th></tr>
                  </thead>
                  <tbody>
                    <tr><td style="text-align: left;">Notebook</td><td>4500.00</td><td>90000.00</td></tr>
                    <tr><td style="text-align: left;">Celular</td><td>2100.00</td><td>84000.00</td></tr>
                    <tr><td style="text-align: left;">Periferico</td><td>150.00</td><td>15000.00</td></tr>
                  </tbody>
                </table>
              </div>
            </div>
          </multi-col>'''
content = re.sub(slide3_orig, slide3_new, content)

# 4. Slide 4
slide4_orig = r'<h2>4\. Analisar no tempo</h2>\s*<code-block lang="sql" data-trim>'
slide4_new = '''<h2>4. Analisar no tempo</h2>
          <div style="display: flex; align-items: center; justify-content: center; gap: 15px; margin-bottom: 15px; color: #8be9fd;">
            <i class="fa-solid fa-calendar-days fa-2x"></i>
            <i class="fa-solid fa-arrow-right"></i>
            <i class="fa-solid fa-chart-line fa-2x"></i>
          </div>
          <code-block lang="sql" data-trim>'''
content = re.sub(slide4_orig, slide4_new, content)

# 5. Slide 5
slide5_orig = r'<h2>5\. Exportar resultado</h2>\s*<code-block lang="sql" data-trim>\s*COPY \(\s*SELECT\s*categoria,\s*SUM\(valor\) AS total\s*FROM vendas\s*GROUP BY categoria\s*\) TO \'resumo_categorias\.csv\'\s*\(HEADER, DELIMITER \',\'\);\s*</code-block>\s*<code-block lang="sql" data-trim>\s*COPY \(\s*SELECT\s*categoria,\s*SUM\(valor\) AS total\s*FROM vendas\s*GROUP BY categoria\s*\) TO \'resumo_categorias\.parquet\'\s*\(FORMAT PARQUET\);\s*</code-block>'
slide5_new = '''<h2>5. Exportar resultado</h2>
          <div class="artifact-grid">
            <div class="artifact-card" style="border-top: 4px solid #ff5555; padding: 10px;">
              <h3 style="color: #ff5555; display: flex; align-items: center; gap: 8px; font-size: 0.65em;">
                <i class="fa-solid fa-file-csv"></i> Para CSV
              </h3>
              <code-block lang="sql" data-trim style="font-size: 0.85em; margin: 0;">
                COPY (
                SELECT
                categoria,
                SUM(valor) AS total
                FROM vendas
                GROUP BY categoria
                ) TO 'resumo_categorias.csv'
                (HEADER, DELIMITER ',');
              </code-block>
            </div>
            <div class="artifact-card" style="border-top: 4px solid #50fa7b; padding: 10px;">
              <h3 style="color: #50fa7b; display: flex; align-items: center; gap: 8px; font-size: 0.65em;">
                <i class="fa-solid fa-database"></i> Para Parquet
              </h3>
              <code-block lang="sql" data-trim style="font-size: 0.85em; margin: 0;">
                COPY (
                SELECT
                categoria,
                SUM(valor) AS total
                FROM vendas
                GROUP BY categoria
                ) TO 'resumo_categorias.parquet'
                (FORMAT PARQUET);
              </code-block>
            </div>
          </div>'''
content = re.sub(slide5_orig, slide5_new, content)

# 6. Slide 6
slide6_orig = r'<h2 style="color: #ffb86c;">Etapa 6: Integracao direta \(Postgres\)</h2>\s*<p>O DuckDB possui uma extensao nativa para ler e escrever diretamente em bancos PostgreSQL\.</p>\s*<code-block lang="sql" data-trim>'
slide6_new = '''<h2 style="color: #ffb86c;">Etapa 6: Integracao direta (Postgres)</h2>
          <p>O DuckDB possui uma extensao nativa para ler e escrever diretamente em bancos PostgreSQL.</p>
          <div class="flow-row" style="margin: 15px 0;">
            <div class="flow-node">
              <i class="fa-solid fa-database fa-2x" style="color: #8be9fd; margin-bottom: 10px;"></i>
              <strong style="color: #f8f8f2;">PostgreSQL</strong>
              <span>Servidor remoto</span>
            </div>
            <div class="flow-arrow">↔</div>
            <div class="flow-node duckdb-node">
              <i class="fa-solid fa-server fa-2x" style="color: #fff100; margin-bottom: 10px;"></i>
              <strong style="color: #f8f8f2;">DuckDB</strong>
              <span>Análise local</span>
            </div>
          </div>
          <code-block lang="sql" data-trim>'''
content = re.sub(slide6_orig, slide6_new, content)

# 7. Slide 7
slide7_orig = r'<h3>Na string de conexao</h3>\s*<code-block lang="sql" data-trim>\s*-- Senha inline\s*ATTACH \'dbname=vendas user=postgres\s*host=localhost password=minha_senha\'\s*AS pg \(TYPE postgres\);\s*</code-block>\s*<div class="pink-box" style="margin-top:8px">\s*<p>Nunca versione senhas em arquivos de codigo\.</p>\s*</div>\s*</div>\s*<div style="flex:1">\s*<h3>Variaveis de ambiente</h3>\s*<code-block lang="powershell" data-trim>\s*# Variáveis padrão PostgreSQL\s*\$env:PGHOST="localhost"\s*\$env:PGPORT="5432"\s*\$env:PGDATABASE="vendas"\s*\$env:PGUSER="postgres"\s*\$env:PGPASSWORD="minha_senha"\s*</code-block>\s*<div class="green-box" style="margin-top:8px">\s*<p>Com as variaveis definidas, basta <code>ATTACH \'\' AS pg \(TYPE postgres\)</code>\.</p>\s*</div>'
slide7_new = '''<div class="artifact-card" style="border-top: 4px solid #ff5555; height: 100%;">
                <h3 style="color: #ff5555; display: flex; align-items: center; gap: 8px; font-size: 0.7em;">
                  <i class="fa-solid fa-triangle-exclamation"></i> Na string de conexão
                </h3>
                <code-block lang="sql" data-trim style="font-size: 0.85em;">
                  -- Senha inline
                  ATTACH 'dbname=vendas user=postgres
                  host=localhost password=minha_senha'
                  AS pg (TYPE postgres);
                </code-block>
                <p style="font-size: 0.6em; color: #f8f8f2; margin-top: 10px;"><i class="fa-solid fa-xmark" style="color: #ff5555;"></i> Nunca versione senhas no código.</p>
              </div>
            </div>
            <div style="flex:1">
              <div class="artifact-card" style="border-top: 4px solid #50fa7b; height: 100%;">
                <h3 style="color: #50fa7b; display: flex; align-items: center; gap: 8px; font-size: 0.7em;">
                  <i class="fa-solid fa-shield-halved"></i> Variáveis de ambiente
                </h3>
                <code-block lang="powershell" data-trim style="font-size: 0.85em;">
                  # Variáveis padrão PostgreSQL
                  $env:PGHOST="localhost"
                  $env:PGPORT="5432"
                  $env:PGDATABASE="vendas"
                  $env:PGUSER="postgres"
                  $env:PGPASSWORD="minha_senha"
                </code-block>
                <p style="font-size: 0.6em; color: #f8f8f2; margin-top: 10px;"><i class="fa-solid fa-check" style="color: #50fa7b;"></i> Basta usar <code>ATTACH '' AS pg</code></p>
              </div>'''
content = re.sub(slide7_orig, slide7_new, content)

with open('bdd2/aula15-duckdb-analise-colunar.html', 'w', encoding='utf-8') as f:
    f.write(content)
print('Done!')
