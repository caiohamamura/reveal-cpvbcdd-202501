/*
 * Código 2: Sensor que Dorme
 * Lê DHT11, imprime no Serial, e dorme 30 segundos
 * 
 * Hardware:
 * - DHT11 no pino D4
 * - Fio D0 → RST (obrigatório para deep sleep)
 */

#include <ESP8266WiFi.h>
#include <DHT.h>

#define DHT_PIN D4
#define DHT_TYPE DHT11
#define LED_PIN 2

DHT dht(DHT_PIN, DHT_TYPE);

void setup() {
  Serial.begin(115200);
  delay(100);
  
  pinMode(LED_PIN, OUTPUT);
  dht.begin();
  
  Serial.println("\n=== Leitura do Sensor ===");
  
  // Feedback visual: LED acendeu
  digitalWrite(LED_PIN, LOW);
  
  // Aguarda 2 segundos para o DHT estabilizar
  delay(2000);
  
  float temp = dht.readTemperature();
  float umid = dht.readHumidity();
  
  if (isnan(temp) || isnan(umid)) {
    Serial.println("❌ ERRO: Falha ao ler o DHT11!");
    Serial.println("Verifique a ligação e o pino.");
  } else {
    Serial.printf("✅ Temperatura: %.1f °C\n", temp);
    Serial.printf("✅ Umidade: %.1f %%\n", umid);
  }
  
  digitalWrite(LED_PIN, HIGH);  // Desliga LED
  
  Serial.println("\n💤 Dormindo 30 segundos...");
  ESP.deepSleep(30e6);  // 30 segundos
}

void loop() {}
