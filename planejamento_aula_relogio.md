# 📚 Planejamento da Aula IoT - Relógios, NTP, Temporizadores e Osciladores

**Módulo/Tópico:** Relógios, NTP, Temporizadores e Osciladores
**Duração Estimada:** 3 horas (4 x 45 minutos)
**Público Alvo:** Alunos do 4º ano Técnico Integrado em Informática.
**Hardware Base:** NodeMCU ESP8266.
**Objetivo Principal:** Capacitar os alunos a implementar mecanismos de tempo precisos, entendendo as limitações de `delay()` e utilizando `millis()` e sincronização NTP.

---

### 🎯 Objetivos de Aprendizagem (Ao final da aula, o aluno deve saber):
1. Diferenciar o uso de `delay()` (bloqueante) de métodos não bloqueantes como `millis()`.
2. Implementar temporizadores eficientes em sistemas embarcados com ESP8266.
3. Configurar e utilizar a sincronização de tempo com Network Time Protocol (NTP) para manter relógios precisos remotamente.

### ⏱️ Roteiro Detalhado (Minuto a Minuto Sugerido)

**Bloco 1: Revisão e Problema (45 min)**
*   **Tópico:** O Problema do Tempo no Código.
*   **Teoria:** Revisitar a função `delay()`. Mostrar exemplos de código onde `delay()` paralisa todo o sistema, impedindo outras tarefas (ex: ler um sensor enquanto espera).
*   **Prática Guiada (Hands-on):** Escrever um código simples usando apenas `delay()` para piscar um LED e acionar um buzzer. **Resultado:** O sistema travará por 2 segundos.
*   **Conceito Chave:** Bloqueio de thread/loop principal.

**Bloco 2: Soluções Não Bloqueantes (45 min)**
*   **Tópico:** `millis()` e `Ticker.h` (ou Timer Interrupts).
*   **Teoria:** Introduzir o uso de `unsigned long` e a comparação de `millis()` em vez de esperar.
*   **Prática Guiada (Hands-on):** Reescrever o código anterior usando `millis()` para piscar LED e buzzer em intervalos de tempo definidos, sem travar o sistema. Introduzir a leitura de um sensor paralelo.
*   **Desafio:** Fazer LED piscar *e* acionar um buzzer em intervalos *diferentes* simultaneamente.

**Bloco 3: Sincronização e Precisão (45 min)**
*   **Tópico:** NTP e RTC (Real Time Clock).
*   **Teoria:** Explicar que `millis()` depende do *boot* do dispositivo e pode perder o tempo se for reiniciado. Apresentar o conceito de NTP (Protocolo de Tempo de Rede).
*   **Prática Guiada (Hands-on):** Configurar o ESP8266 para conectar-se a um servidor NTP e sincronizar o horário do sistema. Criar um display (se disponível, ou apenas enviar via Serial) mostrando a data e hora sincronizada.
*   **Conexão IoT:** Mostrar como a informação de tempo preciso é crucial para agendamentos e logs em um servidor central (MQTT/Cloud).

**Bloco 4: Consolidação e Projeto (45 min)**
*   **Tópico:** Montagem do Relógio IoT Funcional.
*   **Atividade:** Os alunos montarão um sistema que:
    1. Usa o tempo NTP para exibir data/hora.
    2. Pisca um LED em um ciclo de tempo *independente* do ciclo de leitura de sensores (simulando um relógio de backup).
    3. Envia um *heartbeat* MQTT contendo a hora atual para um broker.
*   **Avaliação Formativa:** Checkpoint na funcionalidade de sincronização e estabilidade do *loop*.

---

### 🚀 Materiais Complementares para o Professor
*   **Slides:** Foco visual nos exemplos de código (Antes/Depois de `delay()` vs `millis()`).
*   **Recursos:** Sugerir a utilização do `ArduinoJson` para estruturar o payload MQTT com `{"timestamp": "YYYY-MM-DD HH:MM:SS", "device_id": "ESP001", ...}`.
*   **Próxima Aula:** Transição para **RTC + Gerenciamento de Energia (Deep Sleep)**, explicando como o hardware pode manter o tempo mesmo sem energia (melhorando o conceito de tempo fora da rede).