/*
 * Código 2: Acorda por Luz (Interrupt no D0)
 * 
 *Este código DEMONSTRA o interrupt externo via transistor.
 * NÃO entra em deep sleep - fica esperando o transistor "disparar".
 * 
 * Para o projeto completo com deep sleep, veja o Código 5.
 * 
 * Conceito:
 * - O pino D0 (GPIO 16) está conectado ao RST internamente para timer
 * - Quando D0 vai LOW → RST vai LOW → ESP acorda
 * - O transistor simula um "botão" que o sensor de luz aperta
 * 
 * Circuito:
 *   LDR ──────┬──────── Transistor KSP2222A (coletor)
 *             │
 *   Trimpot ──┴──────── Base (via resistor ~10kΩ)
 *             |
 *   GND ─────────────── Emissor
 *   
 *   Coletor do transistor → RST do ESP8266
 *   
 * Funcionamento:
 * - Luz alta (dia): LDR tem baixa resistência → corrente na base → transistor conduz
 * - Transistor conduz → collector vai LOW → RST vai LOW → ESP ACORDA!
 * - Luz baixa (noite): transistor não conduz → ESP fica dormindo
 * 
 * ⚠️ IMPORTANTE: Este código é para TESTAR o circuito apenas.
 * O ESP8266 NÃO entra em deep sleep aqui - fica acordado
 * esperando o interrupt funcionar.
 */

#include <ESP8266WiFi.h>

#define LED_PIN 2
#define TRANSISTOR_BASE D1  // Pino para monitorar o transistor (opcional, para debug)
#define INTERRUPT_PIN D0    // GPIO 16 - mesmo pino do RST

// Contador de despertares por luz
int contadorLuz = 0;

void ICACHE_RAM_ATTR despertarPorLuz() {
  // Esta função é chamada quando o D0/RST vai LOW
  // No entanto, como é um reset, o código não continua aqui
  // O contador será incrementado quando setup() rodar novamente
  contadorLuz++;
}

void setup() {
  Serial.begin(115200);
  delay(100);
  
  pinMode(LED_PIN, OUTPUT);
  
  // Para debug: monitorar o que acontece no circuito
  pinMode(TRANSISTOR_BASE, INPUT);
  
  contadorLuz++;
  
  Serial.println("\n╔══════════════════════════════════════════════╗");
  Serial.println("║  ACORDEI POR LUZ!  ☀️                        ║");
  Serial.println("╚══════════════════════════════════════════════╝");
  
  Serial.printf("Ciclo #%d\n", contadorLuz);
  
  // Feedback visual: LED acesso = trabalhando
  digitalWrite(LED_PIN, LOW);
  
  // Lê o valor do divisor de tensão (base do transistor)
  int valorLuz = analogRead(A0);
  Serial.printf("Leitura do LDR (A0): %d\n", valorLuz);
  
  // Simula "trabalho" - LED acesso por 3 segundos
  delay(3000);
  
  digitalWrite(LED_PIN, HIGH);  // LED apagado = trabalho concluído
  
  Serial.println("\n💡 Para testar o interrupt:");
  Serial.println("1. Cubra o LDR (escuro) → transistor desliga");
  Serial.println("2. Ilumine o LDR (luz forte) → transistor liga");
  Serial.println("3. Quando transistor liga → D0 LOW → RST LOW → ESP ACORDA!");
  Serial.println("\n⚠️  Neste código, o ESP fica ACORDADO para demo.");
  Serial.println("⚠️  No projeto real (código 5), ele volta a dormir.");
  
  // ============================================
  // NOTA: NÃO USA deepSleep() AQUI - é só demo!
  // ============================================
}

void loop() {
  // Fica parado aqui para demo
  // No projeto real, aqui teria ESP.deepSleep()
  
  // Pisca LED lentamente para mostrar que está "esperando"
  digitalWrite(LED_PIN, LOW);
  delay(500);
  digitalWrite(LED_PIN, HIGH);
  delay(500);
  
  // Para forçar teste: se ler valor alto do LDR, reinicia manualmente
  int valorLuz = analogRead(A0);
  if (valorLuz > 900) {
    Serial.println("\n🔄 Luz forte detectada! Resetando para simular ciclo...\n");
    delay(100);
    ESP.restart();  // Reinicia para simular wake-up por luz
  }
}

/*
 * CIRCUITO COMPLETO (transistor KSP2222A):
 * 
 *   ESP8266 NodeMCU
 *   ┌────────────────┐
 *   │                │
 *   │   RST ◄────────┼──┬── COLLECTOR (C) do KSP2222A
 *   │                │  │
 *   │   D0/GPIO16 ────┘  │
 *   │                    │
 *   │   A0 ◄─────────────┼──(opcional) para debug
 *   │                    │
 *   └────────────────────┘
 *   
 *   KSP2222A Pinout (vista de frente):
 *      ┌─────────┐
 *      │  B  C   │
 *      │  │ │    │
 *      │  E       │
 *      └──────────┘
 *      
 *   E = Emissor → GND
 *   B = Base → LDR + Trimpot (via resistor ~10kΩ)
 *   C = Coletor → RST do ESP
 *   
 *   LDR Circuit:
 *   
 *   3.3V ─── LDR ──── ◄─── Base do transistor
 *                 │
 *            Trimpot (entre LDR e GND, ajustar threshold)
 *                 │
 *            GND
 *   
 *   Como ajustar:
 *   - Trimpot define o limiar de luz
 *   - No escuro: LDR = ~1MΩ, transistor OFF
 *   - No claro: LDR = ~10kΩ, transistor ON → RST LOW → ACORDA!
 */
