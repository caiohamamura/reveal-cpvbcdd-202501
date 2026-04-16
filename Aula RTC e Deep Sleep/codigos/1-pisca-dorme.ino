/*
 * Código 1: Pisca-Dorme
 * O "Hello World" do Deep Sleep
 * Pisca o LED 3 vezes e dorme por 10 segundos
 * 
 * ⚠️ LEMBRETE: Conectar D0 (GPIO 16) ao RST!
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
  ESP.deepSleep(10e6);
}

void loop() {
  // NUNCA executa após deep sleep!
  // O ESP8266 reinicia do zero (roda setup() novamente)
}
