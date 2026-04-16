# 2026-04-12 - Planejamento da aula "Relógios, NTP, Temporizadores e Osciladores"

## 📅 Contexto
**Data:** 12 de abril de 2026  
**Professor:** Caio Hamamura  
**Assistente:** Lucia (OpenClaw)  
**Tema:** Primeira aula do módulo "Programação Avançada" em IoT

## 🎯 Objetivo da sessão
Criar material completo para aula sobre timing e concorrência no ESP8266, incluindo slides, códigos, roteiro e avaliação.

## 📋 Materiais criados

### 1. **Slides da aula** (`/Aula Programação Avançada/slides/aula-timing-concorrencia.md`)
- 45 slides em formato markdown
- Estrutura didática: problema → soluções → projeto
- Analogias visuais (cozinheiro, orquestra)
- Comparação das 4 técnicas de timing

### 2. **Roteiro detalhado** (`/Aula Programação Avançada/materiais/roteiro-aula-detalhado.md`)
- Timing minuto a minuto das 4 aulas
- Checklist do professor
- Materiais necessários por aluno
- Problemas antecipados e soluções
- Diferenciação pedagógica

### 3. **Códigos progressivos** (`/Aula Programação Avançada/codigos/`)
1. `1-problema-delay.ino` - Demonstra o problema do delay()
2. `2-solucao-millis.ino` - Solução com millis()
3. `3-solucao-ticker.ino` - Solução com Ticker
4. `4-solucao-interrupt.ino` - Solução com Interrupt (avançado)
5. `5-projeto-ntp-relogio.ino` - Projeto integrador completo

### 4. **Checklist de projeto** (`/Aula Programação Avançada/projeto/checklist-projeto.md`)
- Avaliação formativa (100 pontos)
- Testes obrigatórios
- Critérios de qualidade
- Problemas comuns + soluções
- Desafios extras (opcional)

### 5. **Resumo executivo** (`/Aula Programação Avançada/materiais/resumo-executivo.md`)
- Visão geral para o professor
- Resultados de aprendizagem
- Pontos críticos de atenção
- Próximos passos

## 🧠 Decisões pedagógicas tomadas

### **Estrutura da aula:**
1. **Aula 1:** Teoria (clock + problema)
2. **Aula 2:** Prática (millis + Timer)
3. **Aula 3:** Prática (Interrupt + NTP)
4. **Aula 4:** Projeto integrador

### **Diferenciação:**
- **Iniciantes:** Foco em millis() (suficiente para 90% dos casos)
- **Intermediários:** Explorar Ticker
- **Avançados:** Desafios com interrupts

### **Avaliação:**
- Checklist com critérios claros
- Autoavaliação do aluno
- Portfólio no GitHub

## 💡 Insights importantes

### **Transição crítica:**
Esta aula marca a passagem do "Arduino hobby" para "Embedded Systems". Alunos começam a entender a arquitetura interna do microcontrolador.

### **Problema didático:**
Começar mostrando código que NÃO funciona (delay()) cria efeito "aha!" e motiva a busca por soluções.

### **Analogias eficazes:**
- Clock = coração do microcontrolador
- Concorrência = cozinheiro com várias panelas
- Interrupt = emergência que interrompe tudo

## 🔗 Conexão com ementa
Esta aula cobre aspectos de:
- Arquitetura de sistemas embarcados (clock)
- Programação concorrente
- Sincronização de tempo
- Preparação para RTC + low power (próxima aula)

## 📈 Métricas de sucesso esperadas
- 90% completam projeto básico
- 70% implementam desafios extras
- Redução significativa no uso de delay() em projetos futuros
- Feedback positivo sobre transição básico→avançado

## 🔮 Próximos passos
**Próxima aula:** RTC + Gerenciamento de Energia
- Relógio em Tempo Real (DS3231)
- Deep Sleep do ESP8266
- Acordar por alarme + interrupt
- Projeto: Despertador IoT com autonomia

## 📝 Observações finais
Material completo e pronto para uso. Testar códigos antes da aula. Verificar se bibliotecas (Ticker, NTPClient) estão instaladas. Preparar componentes hardware suficientes para todos os alunos.

---

**Status:** ✅ Planejamento concluído  
**Próxima ação:** Revisão do professor Caio  
**Data próxima sessão:** A combinar