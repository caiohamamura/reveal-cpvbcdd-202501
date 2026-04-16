# 📋 Roteiro Detalhado da Aula
## "Relógios, NTP, Temporizadores e Osciladores"

**Duração total:** 3 horas (4 aulas de 45 minutos)
**Professor:** Caio Hamamura
**Turma:** 4º ano Técnico Integrado em Informática

---

## 📅 Estrutura da Aula

### **Aula 1/4** (45 min) - Teoria: Clock e o Problema
### **Aula 2/4** (45 min) - Prática: millis() e Timer
### **Aula 3/4** (45 min) - Prática: Interrupts e NTP  
### **Aula 4/4** (45 min) - Projeto Integrador

---

## 🕐 TIMING DETALHADO

### **AULA 1 - TEORIA (45 minutos)**

#### **0-5 min: Abertura e Contexto** ⏰
- [ ] **Boas-vindas** e chamada
- [ ] **Recapitulação** rápida: O que vimos até agora em IoT?
- [ ] **Apresentação** do novo módulo: "Programação Avançada"
- [ ] **Objetivos** da aula no quadro

#### **5-15 min: Parte 1 - O Clock do Microcontrolador** ⏱️
- [ ] **Pergunta provocativa:** "Como o microcontrolador sabe quanto tempo passou?"
- [ ] **Explicação conceitual:** O que é clock? Oscilador interno?
- [ ] **Demonstração visual:** Mostrar cristal no NodeMCU
- [ ] **Analogia:** Clock = coração do microcontrolador
- [ ] **Números concretos:** 1MHz, 40MHz, 80MHz - o que significa?
- [ ] **Atividade rápida:** Calcular quantas instruções em 1 segundo

#### **15-25 min: Parte 2 - O Problema do delay()** 🚫
- [ ] **Revisão:** Mostrar código `delay()` que todos conhecem
- [ ] **Desafio proposto:** "E se quisermos LED E buzzer?"
- [ ] **Demonstração ao vivo:** Código que NÃO funciona
- [ ] **Discussão:** Por que não funciona? O que acontece?
- [ ] **Conclusão:** `delay()` congela TODO o sistema

#### **25-35 min: Parte 3 - Introdução à Concorrência** 💡
- [ ] **Conceito:** Microcontroladores não fazem multitarefa real
- [ ] **Solução:** Concorrência cooperativa
- [ ] **Analogia:** Cozinheiro com várias panelas
- [ ] **Exemplo real:** ESP8266 fazendo WiFi + LED + sensor
- [ ] **Pergunta aos alunos:** Como implementar isso?

#### **35-45 min: Transição para Prática** 🔄
- [ ] **Preparação:** Distribuir materiais (NodeMCU, LEDs, buzzers)
- [ ] **Instalação:** Verificar Arduino IDE com todos
- [ ] **Configuração:** Biblioteca Ticker instalada?
- [ ] **Tarefa para casa (opcional):** Pensar em 2 tarefas concorrentes

---

### **AULA 2 - PRÁTICA: millis() e Timer (45 minutos)**

#### **0-10 min: Revisão e Aquecimento** 🔥
- [ ] **Perguntas rápidas:** O que aprendemos sobre clock?
- [ ] **Demonstração rápida:** Problema do `delay()` novamente
- [ ] **Apresentação da solução:** `millis()` ao resgate!

#### **10-25 min: Parte 4 - millis() em Ação** 🛠️
- [ ] **Explicação:** O que `millis()` retorna?
- [ ] **Código no quadro:** Estrutura básica com `millis()`
- [ ] **DEMONSTRAÇÃO AO VIVO:** 
  - Passo 1: LED piscando com `millis()`
  - Passo 2: Adicionar buzzer
  - Passo 3: Mostrar funcionando simultaneamente
- [ ] **Atividade guiada:** Todos implementam no seu NodeMCU
- [ ] **Suporte individual:** Circular pela sala

#### **25-40 min: Parte 5 - Timer.h (Ticker)** ⏲️
- [ ] **Introdução:** "E se quisermos ainda mais organização?"
- [ ] **Instalação:** Biblioteca Ticker (se não tiver)
- [ ] **Demonstração:** Timer cuidando do LED sozinho
- [ ] **Vantagens:** Código mais limpo, separação de responsabilidades
- [ ] **Atividade:** Converter código `millis()` para Timer
- [ ] **Desafio:** Adicionar terceira tarefa (ex: serial print)

#### **40-45 min: Comparação e Discussão** 📊
- [ ] **Tabela no quadro:** `delay()` vs `millis()` vs Timer
- [ ] **Votação:** Qual método preferem? Por quê?
- [ ] **Dicas:** Quando usar cada um

---

### **AULA 3 - PRÁTICA: Interrupts e NTP (45 minutos)**

#### **0-10 min: Revisão e Contexto** 🔄
- [ ] **Quick demo:** Aluno mostra solução com Timer
- [ ] **Problema novo:** "E se precisarmos de PRECISÃO absoluta?"
- [ ] **Introdução:** Interrupts - quando cada microssegundo conta

#### **10-25 min: Parte 6 - Interrupts na Prática** ⚡️
- [ ] **Conceito:** O que interrompe um microcontrolador?
- [ ] **Exemplos reais:** Botão, sensor, timer
- [ ] **CUIDADO:** O que NÃO fazer em interrupts
- [ ] **Demonstração:** Interrupt por timer
- [ ] **Código no quadro:** Estrutura `ICACHE_RAM_ATTR`
- [ ] **Atividade prática:** Implementar interrupt simples

#### **25-40 min: Parte 8 - NTP: Hora na Internet** 🌍
- [ ] **Problema:** `millis()` não sabe que horas são!
- [ ] **Solução:** NTP - perguntar na internet
- [ ] **Configuração WiFi:** Revisão rápida
- [ ] **Biblioteca:** Instalar NTPClient
- [ ] **Demonstração ao vivo:** Pegar hora da internet
- [ ] **Atividade:** Todos conectam e pegam hora
- [ ] **Desafio:** Mostrar hora formatada (HH:MM:SS)

#### **40-45 min: Preparação para Projeto** 🎯
- [ ] **Apresentação do projeto:** Relógio IoT
- [ ] **Requisitos:** WiFi + NTP + LED + Buzzer
- [ ] **Distribuição de materiais:** Checklist do projeto
- [ ] **Formação de duplas** (opcional)

---

### **AULA 4 - PROJETO INTEGRADOR (45 minutos)**

#### **0-5 min: Briefing do Projeto** 📝
- [ ] **Revisão dos requisitos**
- [ ] **Cronograma:** 40 minutos para implementar
- [ ] **Critérios de avaliação:** O que será avaliado

#### **5-35 min: Implementação do Projeto** 💻
- [ ] **Fase 1 (10 min):** Conexão WiFi + NTP
  - [ ] Conectar ao WiFi
  - [ ] Sincronizar hora
  - [ ] Mostrar no Serial
- [ ] **Fase 2 (10 min):** LED com millis()
  - [ ] LED pisca a cada 1 segundo
  - [ ] Estado visível (ON/OFF)
- [ ] **Fase 3 (10 min):** Buzzer com Timer
  - [ ] Buzzer a cada 1 minuto
  - [ ] Som diferente para horas cheias
- [ ] **Fase 4 (5 min):** Integração final
  - [ ] Tudo funcionando junto
  - [ ] Teste completo

**SUPORTE DO PROFESSOR:** 
- Circular pela sala
- Resolver bugs comuns
- Dar dicas individuais
- Controlar tempo

#### **35-40 min: Apresentações Rápidas** 🎤
- [ ] **1 minuto por dupla:** Mostrar projeto funcionando
- [ ] **Feedback rápido:** O que funcionou? Dificuldades?
- [ ] **Melhor solução:** Votação para a mais criativa

#### **40-45 min: Encerramento e Próxima Aula** 🔮
- [ ] **Recapitulação:** O que aprendemos hoje?
- [ ] **Tabela final:** Comparação dos 4 métodos
- [ ] **Gancho para próxima aula:** "E sem WiFi? RTC!"
- [ ] **Tarefa para casa:** Pesquisar sobre RTC DS3231
- [ ] **Agradecimentos e encerramento**

---

## 🧰 MATERIAIS NECESSÁRIOS

### **Por aluno/dupla:**
- [ ] 1x NodeMCU ESP8266
- [ ] 1x LED (qualquer cor)
- [ ] 1x Buzzer ativo
- [ ] 2x Resistor 220Ω
- [ ] 1x Protoboard
- [ ] Cabos jumper (macho-macho)
- [ ] Cabo USB micro-B

### **Para demonstração do professor:**
- [ ] Projetor + computador
- [ ] NodeMCU montado no projeto completo
- [ ] Slides preparados
- [ ] Quadro branco + marcadores

### **Software:**
- [ ] Arduino IDE 2.x instalado
- [ ] Bibliotecas: Ticker, NTPClient, WiFi
- [ ] Drivers CH340/CP2102 instalados

---

## ⚠️ PONTOS DE ATENÇÃO

### **Antecipar problemas comuns:**
1. **WiFi não conecta:** Verificar senha, rede 2.4GHz
2. **NTP falha:** Testar servidor alternativo (pool.ntp.org)
3. **Interrupt não funciona:** Verificar função `ICACHE_RAM_ATTR`
4. **Timer instável:** Não usar `delay()` dentro de timer

### **Diferenciação pedagógica:**
- **Iniciantes:** Focar em `millis()` (suficiente para 90% dos casos)
- **Intermediários:** Explorar Timer.h
- **Avançados:** Desafio com interrupts + otimização

### **Avaliação:**
- **Checklist** do projeto completo
- **Participação** nas discussões
- **Código** no GitHub (portfólio)
- **Autoavaliação:** Qual método entenderam melhor?

---

## 📝 NOTAS DO PROFESSOR

### **Dicas para melhor engajamento:**
- Começar com DEMONSTRAÇÃO que falha (efeito "aha!")
- Usar analogias do mundo real (cozinheiro, orquestra)
- Mostrar aplicações reais: semáforos, alarmes, sistemas industriais
- Competição saudável: quem faz o LED mais rápido?

### **Adaptações possíveis:**
- Se houver menos tempo: focar em `millis()` + NTP
- Se alunos avançados: adicionar desafio com watchdog timer
- Se problemas com WiFi: usar NTP simulado (hora do computador)

### **Links úteis:**
- GitHub com códigos: [link]
- Documentação Ticker: [link]
- Servidores NTP Brasil: br.pool.ntp.org
- Simulador online: wokwi.com (para quem não tem hardware)

---

## ✅ CHECKLIST FINAL DO PROFESSOR

**ANTES DA AULA:**
- [ ] Slides prontos e testados
- [ ] Códigos de demonstração funcionando
- [ ] Materiais distribuídos nas mesas
- [ ] WiFi da sala testado
- [ ] Projetor funcionando

**DURANTE A AULA:**
- [ ] Timing respeitado (usar cronômetro)
- [ ] Participação ativa dos alunos
- [ ] Problemas técnicos resolvidos rapidamente
- [ ] Todos os objetivos alcançados

**APÓS A AULA:**
- [ ] Materiais recolhidos e contados
- [ ] Feedback dos alunos coletado
- [ ] Códigos enviados para GitHub
- [ ] Preparação para próxima aula (RTC)

---

**Boa aula, professor!** 🚀

> "O timing não é tudo... é a única coisa quando se programa microcontroladores!"