# MEMORY.md - Histórico de Planejamento de Aulas IoT

## Sobre este arquivo

Este é o registro das aulas planejadas, decisões pedagógicas, feedback recebido e evolução do planejamento para o curso de IoT do IFSP Capivari.

**Formato de registro**: Data | Tópico | Decisões/Notas

## Histórico

### 2026-04-12
- **Criação do assistente**: Início do planejamento de aulas de IoT
- **Arquivos base criados**: SOUL.md, USER.md, MEMORY.md, PLANEJAMENTO_AULAS.md
- **Contexto**: O professor Caio solicitou assistência para planejar aulas práticas de IoT para o 4º ano do Técnico Integrado em Informática

### 2026-04-12 (continuação)
- **Definição do contexto**:
  - 4 aulas de 45 minutos semanais
  - Turma: 4º ano do ensino médio integrado
  - Hardware principal: NodeMCU ESP8266 (foco exclusivo)
  - Recursos especiais: impressora 3D, cortadora a laser, sensores variados, motores
- **Planejamento estruturado**:
  - Estrutura de 13 tópicos alinhados à ementa oficial
  - Cronograma de 16 semanas (1 semestre)
  - Cada tópico ocupa aproximadamente 3 horas (4 aulas de 45 min)
  - Integração dos recursos especiais nos projetos
- **Decisões pedagógicas**:
  - Foco 100% em ESP8266 (mais barato, Wi-Fi integrado, compatível com Arduino IDE)
  - Abordagem prática: cada tópico culmina em atividade hands-on
  - Projeto integrador utilizando impressora 3D/cortadora laser
  - Critérios de avaliação alinhados aos objetivos da disciplina

## Princípios pedagógicos estabelecidos

1. **Aprendizado baseado em projetos**: Cada tópico culmina em atividade prática
2. **Escalonamento de complexidade**: Começar com LED, evoluir para sistemas IoT completos
3. **Documentação como parte do aprendizado**: GitHub como portfólio dos projetos
4. **Avaliação contínua**: Checkpoints semanais com rubricas específicas
5. **Integração de recursos especiais**: Uso de impressora 3D e cortadora laser nos projetos
6. **Foco em hardware acessível**: ESP8266 como plataforma principal (custo-benefício)
7. **Alinhamento com ementa oficial**: Cobertura completa dos 13 tópicos exigidos
8. **Preparação para o mercado**: Projetos com aplicações reais e versionamento profissional

## Recursos confirmados

- **Hardware principal**: NodeMCU ESP8266
- **Sensores disponíveis**: temperatura (DHT11/22), umidade, movimento (PIR), luz (LDR), outros variados
- **Atuadores**: LEDs, relés, servo motores, buzzers
- **Equipamentos especiais**: impressora 3D, cortadora a laser
- **Laboratório**: computadores com acesso USB, internet, espaço para protótipos
- **Software**: Arduino IDE, Python, Mosquitto (MQTT), Node-RED, Git

## Tópicos já planejados (13 tópicos da ementa)

1. Noções básicas de ESP8266
2. Conectividade à Internet
3. Protocolos de Comunicação (HTTP, MQTT)
4. Aplicativos WEB
5. Fluxos complexos: Node-RED
6. Padrões de IoT: Clientes em tempo real
7. Padrões de IoT: Controle remoto
8. Padrões de IoT: Clientes sob demanda
9. Padrões de IoT: Aplicativos web
10. Padrões de IoT: De máquina para homem
11. Padrões de IoT: Máquina para máquina
12. Plataformas de IoT (ThingSpeak, Blynk, Firebase)
13. Projeto Integrador com recursos especiais

## Aulas desenvolvidas

### 2026-04-12: Módulo "Programação Avançada" - Aula 1
**Título:** Relógios, NTP, Temporizadores e Osciladores
**Conteúdo:**
- Arquitetura do clock do ESP8266 (40MHz)
- Problema do delay() e concorrência
- Soluções: millis(), Timer.h (Ticker), Interrupts
- Sincronização de tempo com NTP
- Projeto integrador: Relógio IoT com LED e buzzer
**Materiais criados:**
- Slides completos (45 slides)
- Roteiro detalhado (timing minuto a minuto)
- 5 códigos progressivos (do problema à solução)
- Checklist de projeto com avaliação formativa
- Resumo executivo para o professor
**Duração:** 4 aulas de 45 minutos (3 horas)

### 2026-04-16: Módulo "Programação Avançada" - Aula 2
**Título:** RTC, Deep Sleep e Autonomia no ESP8266
**Conteúdo:**
- 8 exemplos reais de IoT com deep sleep (engajamento)
- 3 modos de sleep (Modem, Light, Deep)
- Deep Sleep: 20μA vs 80mA = 4000x economia
- Conexão obrigatória D0→RST
- Acordar por timer e por botão (RST externo)
- RTC memory (512 bytes, sobrevive ao deep sleep)
- NTP inteligente: sincroniza 1 vez, calcula localmente
- Calculadora de autonomia (517 dias com bateria 18650)
- Projeto integrador: Estação Autônoma de Monitoramento
**Materiais criados:**
- 31 slides com exemplos do mundo real
- Roteiro detalhado (timing minuto a minuto)
- 5 códigos progressivos (pisca-dorme → estação completa)
- Checklist/rubrica de avaliação (130 pontos + extras)
- Resumo executivo
**Duração:** 4 aulas de 45 minutos (3 horas)
**Próxima aula:** Máquina de Estados Finitos (FSM)

---

*Este arquivo será atualizado conforme o planejamento avança.*
### 2026-04-22: Atualização da Aula de RTC, Deep Sleep e Autonomia

**Mudanças solicitadas pelo Professor Caio:**

1. **Substituição de RTC_DATA_ATTR por LittleFS + ArduinoJson**
   - RTC_DATA_ATTR só funciona corretamente no ESP32
   - No ESP8266: não persiste em power-off
   - Solução: LittleFS (filesystem) + ArduinoJson para estruturas dinâmicas
   - Vantagens: persiste em power-off, funciona em ambos, estruturas flexíveis

2. **Interrupt por luz usando transistor KSP2222A**
   - Novo projeto: "Estação Solar de Monitoramento"
   - Usa LDR + trimpot + transistor KSP2222A para detectar luz
   - De dia: transistor satura → RST LOW → ESP8266 acorda
   - De noite: transistor corta → ESP8266 dorme
   - Ideal para clima tropical com ciclos de 12h de luz

3. **Materiais refeitos:**
   - 5 códigos progressivos (do pisca-dorme ao projeto completo)
   - Slides atualizados (31 slides)
   - Roteiro detalhado (4 aulas)
   - Checklist do projeto (rubrica + autoavaliação)
   - Resumo executivo

**Arquivos atualizados/criados:**
- `Aula RTC e Deep Sleep/codigos/1-pisca-dorme.ino`
- `Aula RTC e Deep Sleep/codigos/2-acorda-luz-transistor.ino` (NOVO)
- `Aula RTC e Deep Sleep/codigos/3-littlefs-persistencia.ino` (NOVO)
- `Aula RTC e Deep Sleep/codigos/4-sincronizacao-ntp.ino` (NOVO)
- `Aula RTC e Deep Sleep/codigos/5-projeto-estacao-solar.ino` (NOVO)
- `Aula RTC e Deep Sleep/slides/slides-rtc-deep-sleep.md`
- `Aula RTC e Deep Sleep/materiais/resumo-executivo.md`
- `Aula RTC e Deep Sleep/materiais/roteiro-aula-detalhado.md`
- `Aula RTC e Deep Sleep/projeto/checklist-projeto.md`

## Promoted From Short-Term Memory (2026-04-22)

<!-- openclaw-memory-promotion:memory:memory/2026-04-15.md:449:449 -->
- - Candidate: Possible Lasting Truths: No strong candidate truths surfaced. [score=0.845 recalls=0 avg=0.620 source=memory/2026-04-15.md:78-78]
<!-- openclaw-memory-promotion:memory:memory/2026-04-16.md:373:376 -->
- - Candidate: Reflections: Theme: `assistant` kept surfacing across 98 memories.; confidence: 1.00; evidence: memory/.dreams/session-corpus/2026-04-12.txt:2-2, memory/.dreams/session-corpus/2026-04-12.txt:3-3, memory/.dreams/session-corpus/2026-04-12.txt:5-5; note: reflection - confidence: 0.00 - evidence: memory/2026-04-16.md:373-376 - recalls: 0 [score=0.838 recalls=0 avg=0.620 source=memory/2026-04-16.md:3-6]
<!-- openclaw-memory-promotion:memory:memory/2026-04-16.md:379:379 -->
- - Candidate: Possible Lasting Truths: No strong candidate truths surfaced. [score=0.838 recalls=0 avg=0.620 source=memory/2026-04-16.md:358-358]
<!-- openclaw-memory-promotion:memory:memory/2026-04-17.md:378:381 -->
- - Candidate: Reflections: Theme: `assistant` kept surfacing across 100 memories.; confidence: 1.00; evidence: memory/.dreams/session-corpus/2026-04-12.txt:2-2, memory/.dreams/session-corpus/2026-04-12.txt:3-3, memory/.dreams/session-corpus/2026-04-12.txt:5-5; note: reflection - confidence: 0.00 - evidence: memory/2026-04-17.md:378-381 - recalls: 0 [score=0.832 recalls=0 avg=0.620 source=memory/2026-04-17.md:3-6]
<!-- openclaw-memory-promotion:memory:memory/2026-04-17.md:384:384 -->
- - Candidate: Possible Lasting Truths: No strong candidate truths surfaced. [score=0.832 recalls=0 avg=0.620 source=memory/2026-04-17.md:303-303]
