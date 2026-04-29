/*
 * Discord Webhook para NodeMCU ESP8266
 * Envia dados de sensor DHT22 para um canal Discord
 * 
 * Não requer bot Discord - usa apenas webhook (HTTP POST)
 */

#include <Arduino.h>
#include <ESP8266WiFi.h>
#include <WiFiManager.h>          // Para autoconfiguração WiFi
#include <DHT.h>
#include <ArduinoJson.h>

// ========== CONFIGURAÇÕES ==========
#define DHT_PIN 4                // Sensor DHT22 no GPIO4 (D2)
#define DHT_TYPE DHT22

// Intervalo entre envios (ms) - 30 segundos
#define SEND_INTERVAL 30000

// Número de tentativas de retry
#define MAX_RETRIES 3
#define RETRY_DELAY 1000         // 1 segundo entre retries

// ========== VARIÁVEIS GLOBAIS ==========
DHT dht(DHT_PIN, DHT_TYPE);
WiFiManager wifiManager;

//last send time
unsigned long lastSendTime = 0;

// ========== FUNÇÕES ==========

// Enviar dados para Discord via webhook (com retry)
bool sendToDiscord(float temp, float humidity) {
  WiFiClient client;
  
  // Parse webhook URL
  String webhookUrl = DISCORD_WEBHOOK_URL;
  
  // Determinar host e caminho
  String host;
  String path;
  
  if (webhookUrl.startsWith("https://discord.com/api/webhooks/")) {
    // Extrair host e path da URL
    String fullPath = webhookUrl.substring(8); // remove "https://"
    int slashIdx = fullPath.indexOf('/');
    host = fullPath.substring(0, slashIdx);
    path = fullPath.substring(slashIdx);
  } else {
    Serial.println("❌ URL do webhook inválida!");
    return false;
  }
  
  Serial.print("📡 Enviando para Discord (");
  Serial.print(host);
  Serial.println(path + ")...");
  
  // Construir JSON payload
  StaticJsonDocument<256> doc;
  doc["content"] = "📊 *Dados do Sensor IoT*\n🌡️ Temp: " + String(temp, 1) + "°C\n💧 Umidade: " + String(humidity, 1) + "%";
  
  String payload;
  serializeJson(doc, payload);
  
  // Tentar envio com retry
  for (int attempt = 1; attempt <= MAX_RETRIES; attempt++) {
    Serial.print("Tentativa ");
    Serial.print(attempt);
    Serial.print("/");
    Serial.print(MAX_RETRIES);
    Serial.println("...");
    
    if (client.connect(host.c_str(), 443)) {
      // Enviar requisição HTTP
      client.println("POST " + path + " HTTP/1.1");
      client.println("Host: " + host);
      client.println("User-Agent: ESP8266-IoT");
      client.println("Content-Type: application/json");
      client.print("Content-Length: ");
      client.println(payload.length());
      client.println();
      client.print(payload);
      
      // Aguardar resposta
      delay(500);
      
      String response = "";
      while (client.available()) {
        response = client.readStringUntil('\n');
        if (response.startsWith("HTTP/1.1")) {
          Serial.println("Resposta: " + response);
        }
      }
      client.stop();
      
      if (response.indexOf("204") != -1 || response.indexOf("200") != -1) {
        Serial.println("✅ Dados enviados com sucesso!");
        return true;
      }
    }
    
    if (attempt < MAX_RETRIES) {
      delay(RETRY_DELAY);
    }
  }
  
  Serial.println("❌ Falha ao enviar após " + String(MAX_RETRIES) + " tentativas");
  client.stop();
  return false;
}

// Ler sensor DHT22
bool readDHT(float& temp, float& humidity) {
  temp = dht.readTemperature();
  humidity = dht.readHumidity();
  
  if (isnan(temp) || isnan(humidity)) {
    Serial.println("❌ Erro ao ler sensor DHT22!");
    return false;
  }
  
  Serial.print("🌡️ Temperatura: ");
  Serial.print(temp, 1);
  Serial.println("°C");
  
  Serial.print("💧 Umidade: ");
  Serial.print(humidity, 1);
  Serial.println("%");
  
  return true;
}

// Setup
void setup() {
  Serial.begin(115200);
  delay(1000);
  
  // Inicializar DHT
  dht.begin();
  
  // Configurar WiFi com WiFiManager
  Serial.println("🔧 Configurando WiFi...");
  Serial.println("📡 Connecte-se à rede 'IoT-Discord-Config' para configurar");
  wifiManager.autoConnect("IoT-Discord-Config");
  
  Serial.println("✅ WiFi conectado!");
  Serial.print("📶 IP: ");
  Serial.println(WiFi.localIP());
  
  Serial.println("✅ Sistema inicializado!");
  Serial.println("📡 Enviando dados a cada " + String(SEND_INTERVAL / 1000) + " segundos");
}

// Loop principal
void loop() {
  unsigned long currentTime = millis();
  
  // Verificar se é hora de enviar
  if (currentTime - lastSendTime >= SEND_INTERVAL) {
    float temp, humidity;
    
    Serial.println("\n========== Leitura de Sensor ==========");
    
    if (readDHT(temp, humidity)) {
      sendToDiscord(temp, humidity);
    }
    
    lastSendTime = currentTime;
  }
  
  // Permitir que eventos do WiFiManager sejam processados
  wifiManager.process();
}