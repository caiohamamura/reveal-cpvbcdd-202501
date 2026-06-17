import re
import random
from datetime import datetime
import subprocess
import os

# Set fixed seed for reproducibility
random.seed(42)

with open('base-questoes-bdd2.md', 'r', encoding='utf-8') as f:
    lines = f.readlines()

categories = {}
current_category = None
current_question = None

for line in lines:
    m_cat = re.match(r'^## (.*)', line)
    if m_cat:
        cat_name = m_cat.group(1).strip()
        current_category = cat_name
        categories[current_category] = []
        continue
    
    m_q = re.match(r'^### Q\d+ — .*', line)
    if m_q:
        if current_question:
            categories[current_category].append(current_question)
        current_question = {'text': '', 'options': [], 'answer': ''}
        continue
    
    if current_question is not None:
        if line.startswith('**Gabarito:**'):
            current_question['answer'] = line.split('**Gabarito:**')[1].strip()
        elif line.strip() == '---':
            continue
        elif re.match(r'^[A-E]\) ', line):
            current_question['options'].append(line[3:].strip())
        else:
            if not current_question['options']:
                current_question['text'] += line
            else:
                if line.strip():
                    current_question['options'][-1] += ' ' + line.strip()

if current_question:
    categories[current_category].append(current_question)

for cat in categories:
    for q in categories[cat]:
        q['text'] = q['text'].strip()

distribution = {
    "Procedures e funções": 2,
    "Triggers": 1,
    "Views": 1,
    "Materialized views": 1,
    "NoSQL — conceitos gerais": 1,
    "NoSQL — chave-valor": 1,
    "NoSQL — documentos": 1,
    "NoSQL — colunar": 1,
    "NoSQL — grafos": 1
}

def escape_latex(text):
    code_blocks = []
    def repl_code(m):
        code_blocks.append(m.group(1))
        return f"@@CODEBLOCK{len(code_blocks)-1}@@"
    text = re.sub(r'`(.*?)`', repl_code, text)
    
    bold_blocks = []
    def repl_bold(m):
        bold_blocks.append(m.group(1))
        return f"@@BOLDBLOCK{len(bold_blocks)-1}@@"
    text = re.sub(r'\*\*(.*?)\*\*', repl_bold, text)
    
    text = text.replace('%', '\\%').replace('$', '\\$').replace('#', '\\#').replace('&', '\\&')
    text = text.replace('_', '\\_')
    
    for i, c in enumerate(code_blocks):
        c_esc = c.replace('%', '\\%').replace('$', '\\$').replace('#', '\\#').replace('&', '\\&').replace('_', '\\_')
        text = text.replace(f"@@CODEBLOCK{i}@@", f"\\texttt{{{c_esc}}}")
        
    for i, b in enumerate(bold_blocks):
        b_esc = b.replace('%', '\\%').replace('$', '\\$').replace('#', '\\#').replace('&', '\\&').replace('_', '\\_')
        text = text.replace(f"@@BOLDBLOCK{i}@@", f"\\textbf{{{b_esc}}}")
        
    text = text.replace('  \n', '\\\\ \n')
    return text

exams = []
NUM_EXAMS = 34

for i in range(NUM_EXAMS):
    version_id = f"{i+1:02d}"
    exam_questions = []
    for cat, count in distribution.items():
        sampled = random.sample(categories[cat], count)
        exam_questions.extend(sampled)
    
    random.shuffle(exam_questions)
    exams.append({
        'version': version_id,
        'questions': exam_questions
    })

with open('main.tex', 'r', encoding='utf-8') as f:
    main_tex = f.read()

# Fix LaTeX errors
main_tex = main_tex.replace('\\INItrue', '')
main_tex = main_tex.replace('\\usepackage{fancyhdr}', '')
main_tex = main_tex.replace('\\pagestyle{fancy}', '')

# CORRECTLY remove the entire fancypagestyle block
main_tex = re.sub(r'\\fancypagestyle\{firstpage\}.*?\\cfoot\{\}', '', main_tex, flags=re.DOTALL)

# Apply requested modifications
main_tex = main_tex.replace('Técnico em Informática', 'Análise e Desenvolvimento de Sistemas')

today_str = datetime.now().strftime('%d/%m/%Y')
main_tex = re.sub(r'\\newcommand\{\\data\}\{.*?\}', f'\\\\newcommand{{\\\\data}}{{{today_str}}}', main_tex)

main_tex = main_tex.replace('Prova Final \\\\', 'Prova Final - Versão \\versao \\\\')

preamble = main_tex.split('\\begin{document}')[0]
preamble += '\\def\\versao{00}\n'
preamble += '\\footer{}{Página \\thepage}{}\n'

provas_tex = preamble + '\\begin{document}\n'

for exam in exams:
    provas_tex += f"\\def\\versao{{{exam['version']}}}\n"
    provas_tex += "\\setcounter{question}{0}\n"
    provas_tex += "\\setcounter{page}{1}\n"
    provas_tex += "\\noindent\\cabecalho\n\n"
    provas_tex += "\\vspace{1cm}\n"
    provas_tex += "\\begin{questions}\n"
    provas_tex += "\\begin{multicols}{2}\n"
    
    for q in exam['questions']:
        provas_tex += "\\begin{minipage}{\\linewidth}\n"
        provas_tex += f"\\question {escape_latex(q['text'])}\n"
        provas_tex += "\\begin{enumerate}[label={(\\alph*)}]\n"
        for opt in q['options']:
            provas_tex += f"    \\item {escape_latex(opt)}\n"
        provas_tex += "\\end{enumerate}\n"
        provas_tex += "\\end{minipage}\n\n"
        
    provas_tex += "\\end{multicols}\n"
    provas_tex += "\\end{questions}\n"
    provas_tex += "\\newpage\n\n"

provas_tex += "\\end{document}\n"

with open('provas_completas.tex', 'w', encoding='utf-8') as f:
    f.write(provas_tex)

# Generate Gabaritos as Table
gabaritos_tex = r"""\documentclass[12pt]{article}
\usepackage[utf8]{inputenc}
\usepackage[brazilian]{babel}
\usepackage[a4paper, margin=2cm]{geometry}
\usepackage{booktabs}
\begin{document}
\section*{Gabaritos}
\begin{center}
\renewcommand{\arraystretch}{1.2}
\begin{tabular}{c | *{10}{c}}
\toprule
\textbf{Versão} & \textbf{Q1} & \textbf{Q2} & \textbf{Q3} & \textbf{Q4} & \textbf{Q5} & \textbf{Q6} & \textbf{Q7} & \textbf{Q8} & \textbf{Q9} & \textbf{Q10} \\
\midrule
"""

for exam in exams:
    answers = " & ".join(q['answer'] for q in exam['questions'])
    gabaritos_tex += f"{exam['version']} & {answers} \\\\\n"

gabaritos_tex += r"""\bottomrule
\end{tabular}
\end{center}
\end{document}
"""

with open('gabaritos_completos.tex', 'w', encoding='utf-8') as f:
    f.write(gabaritos_tex)

print("Compiling PDFs...")
subprocess.run(["pdflatex", "-interaction=nonstopmode", "provas_completas.tex"])
subprocess.run(["pdflatex", "-interaction=nonstopmode", "gabaritos_completos.tex"])
print("Arquivos LaTeX e PDF gerados com sucesso!")
