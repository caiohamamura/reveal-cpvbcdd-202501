/*
 * Código 3: Acordar por Botão
 * Deep sleep "infinito" — só acorda quando RST vai LOW (botão)
 * 
 * Hardware:
 * - Botão push-button entre RST e GND
 * - Fio D0 → RST (para timer sleep, mas aqui usamos deepSleep(0))
 * 
 * Aplicação: sensor de porta, alerta de movimento, etc.
 */

#include <ESP8266WiFi.h>

#define LED_PIN 2

void setup() {
  Serial.begin(115200);
  delay(100);
  pinMode(LED_PIN, OUTPUT);
  
  Serial.println("\n=== 🔔 Acordei por botão! ===");
  Serial.println("Alguém apertou o botão (ou o sensor disparou).");
  Serial.println("Fazendo trabalho rápido...");
  
  // Liga LED por 3 segundos (simula "trabalho")
  digitalWrite(LED_PIN, LOW);
  delay(3000);
  digitalWrite(LED_PIN, HIGH);
  
  Serial.println("Trabalho concluído.");
  Serial.println("💤 Voltando a dormir. Aperte o botão de novo!");
  
  // Deep sleep "infinito" (0 = só acorda por RST externo)
  ESP.deepSleep(0);
}

void loop() {}
