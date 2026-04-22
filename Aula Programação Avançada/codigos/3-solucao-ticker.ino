/*
 * CÓDIGO 3: SOLUÇÃO COM Ticker (Timer.h)
 * 
 * Este código demonstra como usar a biblioteca Ticker
 * para agendar funções em intervalos regulares.
 * 
 * Hardware necessário:
 * - NodeMCU ESP8266
 * - LED no pino D4 (LED_BUILTIN)
 * - Buzzer no pino D5
 * 
 * Biblioteca necessária:
 * - Ticker (instalar via Library Manager do Arduino IDE)
 */

#include <Ticker.h>

const int LED_PIN = LED_BUILTIN;    // D4 no NodeMCU
const int BUZZER_PIN = D5;          // Pino do buzzer

// Criar objetos Ticker para cada tarefa
Ticker timerLED;      // Timer para o LED
Ticker timerBuzzer;   // Timer para o buzzer

// Variáveis de estado
bool estadoLED = false;
int contadorBips = 0;

void setup() {
  Serial.begin(115200);
  Serial.println("=== SOLUÇÃO COM Ticker (Timer.h) ===");
  Serial.println("Timer do LED: 1 segundo");
  Serial.println("Timer do Buzzer: 0,5 segundos");
  Serial.println("As tarefas são executadas AUTOMATICAMENTE!");
  Serial.println();
  
  pinMode(LED_PIN, OUTPUT);
  pinMode(BUZZER_PIN, OUTPUT);
  
  // Estado inicial
  digitalWrite(LED_PIN, LOW);
  
  // ============================================
  // CONFIGURAR OS TIMERS
  // ============================================
  
  // Timer do LED: executa função piscarLED() a cada 1 segundo
  timerLED.attach(1.0, piscarLED);  // 1.0 = 1 segundo
  
  // Timer do buzzer: executa função tocarBuzzer() a cada 0,5 segundos
  timerBuzzer.attach(0.5, tocarBuzzer);  // 0.5 = 500ms
  
  Serial.println("Timers configurados!");
  Serial.println("O loop() está vazio - os timers cuidam de tudo!");
  Serial.println();
}

void loop() {
  // O loop() está VAZIO! 😮
  // Os timers executam as funções automaticamente.
  
  // Podemos fazer outras coisas aqui se quisermos:
  // - Ler sensores
  // - Processar comunicação
  // - Atualizar display
  
  // Exemplo: mostrar status a cada 10 segundos
  static unsigned long ultimoStatus = 0;
  if (millis() - ultimoStatus >= 10000) {
    ultimoStatus = millis();
    Serial.print("Sistema ativo há ");
    Serial.print(millis() / 1000);
    Serial.print(" segundos. Bips: ");
    Serial.println(contadorBips);
  }
}

// ============================================
// FUNÇÕES CHAMADAS PELOS TIMERS
// ============================================

void piscarLED() {
  // Alterna o estado do LED
  estadoLED = !estadoLED;
  digitalWrite(LED_PIN, estadoLED);
  
  Serial.print("LED: ");
  Serial.println(estadoLED ? "LIGADO" : "DESLIGADO");
}

void tocarBuzzer() {
  // Toca o buzzer por 100ms
  tone(BUZZER_PIN, 1000, 100);  // 1000Hz por 100ms
  
  contadorBips++;
  
  Serial.print("BUZZER: BIP #");
  Serial.println(contadorBips);
  
  // Exemplo: bip especial a cada 10 bips
  if (contadorBips % 10 == 0) {
    Serial.println("🎵 BIP ESPECIAL! 🎵");
    tone(BUZZER_PIN, 1500, 200);  // Tom diferente
  }
}

/*
 * COMO FUNCIONA O Ticker:
 * 
 * 1. Criamos objetos Ticker para cada tarefa periódica
 * 2. Usamos .attach(intervalo, função) para agendar
 * 3. A função é chamada AUTOMATICAMENTE a cada intervalo
 * 4. O loop() principal fica livre para outras tarefas
 * 
 * PARÂMETROS DO .attach():
 * - .attach(segundos, função)  → intervalo em segundos (float)
 * - .attach_ms(ms, função)     → intervalo em milissegundos
 * 
 * VANTAGENS:
 * - Código mais organizado e modular
 * - Separação clara de responsabilidades
 * - Fácil adicionar/remover tarefas
 * - Precisão melhor que millis() para intervalos fixos
 * 
 * DESVANTAGENS:
 * - Consome mais memória (cada timer tem overhead)
 * - Menos flexível que millis() para tempos variáveis
 * - Dificuldade em parar/retomar timers dinamicamente
 * 
 * BOAS PRÁTICAS:
 * 1. Mantenha as funções do timer CURTAS e RÁPIDAS
 * 2. NÃO use delay() dentro das funções do timer
 * 3. Use variáveis globais para comunicação entre funções
 * 4. Teste a estabilidade com múltiplos timers
 * 
 * EXERCÍCIOS:
 * 1. Adicione um terceiro timer para piscar outro LED
 * 2. Crie um timer que pare após 10 execuções
 * 3. Implemente um sistema de prioridade entre timers
 */

/*
 * ALTERNATIVA: ESP8266Timer
 * 
 * Se precisar de mais precisão ou mais timers:
 * #include <ESP8266Timer.h>
 * 
 * ESP8266Timer timer;
 * timer.setInterval(1000000, piscarLED);  // Microssegundos
 */