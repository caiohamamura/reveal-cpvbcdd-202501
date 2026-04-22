/*
 * CÓDIGO 4: SOLUÇÃO COM INTERRUPTS (Ticker + Interrupt)
 * 
 * Este código demonstra como usar interrupts com timer
 * para tarefas que requerem TEMPO CRÍTICO.
 * 
 * ATENÇÃO: Interrupts são para casos ESPECIAIS!
 * Use apenas quando precisar de máxima precisão.
 * 
 * Hardware necessário:
 * - NodeMCU ESP8266
 * - LED no pino D4 (LED_BUILTIN)
 * 
 * Biblioteca necessária:
 * - Ticker (instalar via Library Manager do Arduino IDE)
 */

#include <Ticker.h>

const int LED_PIN = LED_BUILTIN;    // D4 no NodeMCU

// Timer que gera interrupts
Ticker timerInterrupt;

// Variáveis compartilhadas (volatile para interrupts)
volatile bool flagInterrupt = false;
volatile int contadorInterrupt = 0;

void setup() {
  Serial.begin(115200);
  Serial.println("=== SOLUÇÃO COM INTERRUPTS ===");
  Serial.println("Timer gera interrupt a cada 1 segundo");
  Serial.println("Interrupt alterna uma flag (rápido!)");
  Serial.println("Loop principal verifica a flag e age");
  Serial.println();
  
  pinMode(LED_PIN, OUTPUT);
  digitalWrite(LED_PIN, LOW);
  
  // ============================================
  // CONFIGURAR TIMER COM INTERRUPT
  // ============================================
  
  // Configurar timer para chamar a função de interrupt
  // ICACHE_RAM_ATTR é OBRIGATÓRIO para funções de interrupt no ESP8266
  timerInterrupt.attach(1.0, gerarInterrupt);
  
  Serial.println("Timer de interrupt configurado!");
  Serial.println("A função gerarInterrupt() será chamada a cada 1s");
  Serial.println("MAS ela será MUITO RÁPIDA (apenas seta uma flag)");
  Serial.println();
  
  Serial.println("⚠️  REGRAS DE OURO PARA INTERRUPTS:");
  Serial.println("1. Seja RÁPIDO (microssegundos, não milissegundos)");
  Serial.println("2. NÃO use Serial.print()");
  Serial.println("3. NÃO use delay()");
  Serial.println("4. NÃO use funções WiFi");
  Serial.println("5. Use variáveis 'volatile' para comunicação");
  Serial.println();
}

void loop() {
  // ============================================
  // LOOP PRINCIPAL (faz o trabalho pesado)
  // ============================================
  
  // Verificar se o interrupt aconteceu
  if (flagInterrupt) {
    // RESET da flag (deve ser feito rápido)
    flagInterrupt = false;
    
    // Agora podemos fazer o trabalho "pesado"
    // que não cabia no interrupt
    
    // Alternar LED
    static bool estadoLED = false;
    estadoLED = !estadoLED;
    digitalWrite(LED_PIN, estadoLED);
    
    // Mostrar no Serial (NUNCA no interrupt!)
    Serial.print("Interrupt #");
    Serial.print(contadorInterrupt);
    Serial.print(" - LED: ");
    Serial.println(estadoLED ? "LIGADO" : "DESLIGADO");
    
    // Exemplo de trabalho mais complexo (OK aqui no loop)
    processarDados();
  }
  
  // Outras tarefas do loop principal
  tarefaSecundaria();
}

// ============================================
// FUNÇÃO DE INTERRUPT (DEVE SER RÁPIDA!)
// ============================================

void ICACHE_RAM_ATTR gerarInterrupt() {
  // ⚠️  ESTA FUNÇÃO DEVE SER SUPER RÁPIDA!
  // ⚠️  NÃO COLOQUE NADA PESADO AQUI!
  
  // Apenas setar flags/variáveis
  flagInterrupt = true;
  contadorInterrupt++;
  
  // TEMPO DE EXECUÇÃO: < 10 microssegundos
  // Se demorar mais, pode perder outros interrupts!
}

// ============================================
// FUNÇÕES DO LOOP PRINCIPAL
// ============================================

void processarDados() {
  // Simulação de processamento mais complexo
  static int processamentos = 0;
  processamentos++;
  
  // Exemplo: processar a cada 5 interrupts
  if (contadorInterrupt % 5 == 0) {
    Serial.print("  Processamento batch #");
    Serial.println(processamentos);
    
    // Simular trabalho (ainda no loop principal)
    delay(50);  // OK aqui, pois não está no interrupt!
    Serial.println("  Processamento concluído!");
  }
}

void tarefaSecundaria() {
  // Exemplo de outra tarefa no loop principal
  static unsigned long ultimaExecucao = 0;
  
  if (millis() - ultimaExecucao >= 3000) {  // A cada 3 segundos
    ultimaExecucao = millis();
    
    Serial.print("Tarefa secundária - Interrupts totais: ");
    Serial.println(contadorInterrupt);
  }
}

/*
 * QUANDO USAR INTERRUPTS:
 * 
 * 1. TEMPO CRÍTICO: quando cada microssegundo importa
 * 2. EVENTOS EXTERNOS: botões, sensores de borda
 * 3. TIMERS DE ALTA PRECISÃO: controle PWM, áudio
 * 4. COMUNICAÇÃO: UART, I2C, SPI (já usam interrupts internamente)
 * 
 * QUANDO NÃO USAR INTERRUPTS:
 * 
 * 1. Tarefas comuns (use millis() ou Ticker)
 * 2. Qualquer coisa que use Serial
 * 3. Comunicação WiFi/HTTP
 * 4. Quando não há necessidade real de precisão
 * 
 * ARQUITETURA TÍPICA COM INTERRUPTS:
 * 
 * Interrupt (rápido):
 *   - Seta uma flag
 *   - Incrementa contador
 *   - Atualiza variável volatile
 * 
 * Loop principal (lento, mas seguro):
 *   - Verifica flag
 *   - Faz trabalho pesado
 *   - Usa Serial, WiFi, etc.
 * 
 * VANTAGENS:
 * - Máxima precisão temporal
 * - Resposta imediata a eventos
 * - Não depende do loop() estar livre
 * 
 * DESVANTAGENS:
 * - Complexidade aumentada
 * - Debug difícil
 * - Risco de corromper dados
 * - Pode causar "race conditions"
 * 
 * EXERCÍCIO AVANÇADO:
 * 
 * Implemente um sistema com:
 * 1. Interrupt por timer (1ms) para ler sensor analógico
 * 2. Interrupt por botão para emergência
 * 3. Loop principal que mostra dados no Serial
 * 4. Verificação de conflito entre interrupts
 */

/*
 * DICA DE PERFORMANCE:
 * 
 * Use o atributo ICACHE_RAM_ATTR para forçar a função
 * a ser armazenada na RAM (mais rápido que Flash).
 * 
 * No ESP8266, funções na Flash têm latência variável
 * devido ao cache. Na RAM, são sempre rápidas.
 */