/*
 * Código 1: Pisca-Dorme
 * O "Hello World" do Deep Sleep
 * 
 * Objetivo: Entender o ciclo básico acordar → trabalhar → dormir
 * - LED pisca 3 vezes como feedback visual
 * - Deep sleep de 10 segundos
 * - Ciclo repete infinitamente
 * 
 * ⚠️ LEMBRETE: Conectar D0 (GPIO 16) ao RST!
 * 
 * Hardware:
 * - NodeMCU ESP8266
 * - LED onboard (GPIO 2, ativo em LOW)
 * - Fio D0 → RST (obrigatório!)
 */

#define LED_PIN 2  // LED onboard do NodeMCU (ativo em LOW)

void setup() {
  Serial.begin(115200);
  delay(100);
  
  Serial.println("\n=== Acordei! ===");
  
  // Pisca LED 3 vezes (feedback visual)
  pinMode(LED_PIN, OUTPUT);
  for (int i = 0; i < 3; i++) {
    digitalWrite(LED_PIN, LOW);   // liga LED
    delay(200);
    digitalWrite(LED_PIN, HIGH);  // desliga LED
    delay(200);
  }
  
  Serial.println("Trabalho feito. Dormindo 10 segundos...");
  
  // Deep sleep por 10 segundos (em microssegundos)
  // 10e6 = 10 × 10^6 = 10.000.000 μs = 10 segundos
  ESP.deepSleep(10e6);
}

void loop() {
  // NUNCA executa após deep sleep!
  // O ESP8266 reinicia do zero (roda setup() novamente)
}

/*
 * EXPERIMENTO:
 * 1. Carregue o código e observe o LED piscando
 * 2. Após 10 segundos, o ESP acorda sozinho? (LED pisca novamente)
 * 3. Se NÃO acordar: verifique o fio D0 → RST!
 * 
 * DESAFIO:
 * - Mude o número de piscadas do LED
 * - Mude o tempo de deep sleep para 30 segundos
 */
