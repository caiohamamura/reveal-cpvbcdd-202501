/*
 * Bot Telegram para NodeMCU ESP8266
 * Controle de LED e leitura de sensor DHT22
 * 
 * Comandos:
 * /start   - Mostra mensagem de boas-vindas
 * /status  - Mostra temperatura e umidade
 * /ledon   - Liga o LED
 * /ledoff  - Desliga o LED
 * /help    - Mostra ajuda
 * 
 * MELHORIAS v2:
 * - Autenticação por chat_id (só IDs autorizados podem controlar)
 * - Rate limiting (cooldown entre comandos)
 * - Reconnection WiFi automático
 */

// ========== INCLUDES ==========
#include <Arduino.h>
#include <ESP8266WiFi.h>
#include <WiFiClientSecure.h>
#include <WiFiManager.h>          // Para autoconfiguração WiFi
#include <UniversalTelegramBot.h>
#include <ArduinoJson.h>
#include <DHT.h>

// ========== CONFIGURAÇÕES ==========
#define LED_PIN 2                 // LED embutido no NodeMCU (GPIO2)
#define DHT_PIN 4                 // Sensor DHT22 no GPIO4 (D2)
#define DHT_TYPE DHT22

// Tempo entre verificações do bot (ms)
#define BOT_INTERVAL 1000

// Rate limiting: tempo mínimo entre comandos (ms)
#define COMMAND_COOLDOWN 1500     // 1.5 segundos entre comandos

// ========== CHAT IDs AUTORIZADOS ==========
// ⚠️ SUBSTITUA pelos seus chat_ids!
// Para descobrir seu chat_id: mande /start no bot e olhe o Serial Monitor
String authorized_ids[] = {
  "123456789",    // Exemplo: substitua pelo seu
  "987654321"     // Adicione mais IDs aqui para outros usuários
};

// ========== VARIÁVEIS GLOBAIS ==========
DHT dht(DHT_PIN, DHT_TYPE);
WiFiManager wifiManager;
WiFiClientSecure secured_client;
UniversalTelegramBot* bot;

unsigned long lastMessageTime = 0;
unsigned long lastCommandTime = 0;  // Para rate limiting
bool ledState = false;

// ========== FUNÇÕES ==========

// Verifica se o chat_id é autorizado
bool isAuthorized(String chat_id) {
  for (int i = 0; i < sizeof(authorized_ids)/sizeof(authorized_ids[0]); i++) {
    if (chat_id == authorized_ids[i]) {
      return true;
    }
  }
  return false;
}

// Verifica e reconecta WiFi se necessário
bool checkWiFiConnection() {
  if (WiFi.status() != WL_CONNECTED) {
    Serial.println("⚠️ Wi-Fi desconectado!");
    Serial.println("   Tentando reconectar...");
    
    WiFi.disconnect();
    WiFi.reconnect();
    
    int attempts = 0;
    while (WiFi.status() != WL_CONNECTED && attempts < 10) {
      delay(1000);
      attempts++;
      Serial.print(".");
    }
    Serial.println();
    
    if (WiFi.status() == WL_CONNECTED) {
      Serial.println("✅ Wi-Fi reconectado!");
      Serial.print("📶 IP: ");
      Serial.println(WiFi.localIP());
      return true;
    } else {
      Serial.println("❌ Falha ao reconectar. Tentando novamente em 10s...");
      return false;
    }
  }
  return true;
}

// Mensagem de boas-vindas
String welcomeMessage() {
  String msg = "🤖 *Bot IoT - NodeMCU ESP8266*\n\n";
  msg += "Bem-vindo! Este bot controla seu dispositivo IoT.\n\n";
  msg += "*Comandos disponíveis:*\n";
  msg += "/start - Mensagem de boas-vindas\n";
  msg += "/status - Ver temperatura e umidade\n";
  msg += "/ledon - Ligar LED\n";
  msg += "/ledoff - Desligar LED\n";
  msg += "/help - Mostrar ajuda\n";
  return msg;
}

// Ler sensor DHT22
String readSensor() {
  float temp = dht.readTemperature();
  float humidity = dht.readHumidity();
  
  if (isnan(temp) || isnan(humidity)) {
    return "❌ Erro ao ler sensor DHT22!";
  }
  
  String msg = "📊 *Leituras do Sensor*\n";
  msg += "🌡️ Temperatura: " + String(temp, 1) + "°C\n";
  msg += "💧 Umidade: " + String(humidity, 1) + "%\n";
  return msg;
}

// Processar comandos do Telegram
void handleNewMessages(int numNewMessages) {
  for (int i = 0; i < numNewMessages; i++) {
    String chat_id = bot->messages[i].chat_id;
    String text = bot->messages[i].text;
    
    Serial.print("📨 Comando de ");
    Serial.print(chat_id);
    Serial.print(": ");
    Serial.println(text);
    
    // ========== AUTENTICAÇÃO ==========
    if (!isAuthorized(chat_id)) {
      Serial.println("❌ Acesso não autorizado!");
      bot->sendMessage(chat_id, "❌ *Acesso negado.*\n\nVocê não tem permissão para controlar este dispositivo.", "Markdown");
      continue;
    }
    
    // ========== RATE LIMITING ==========
    unsigned long now = millis();
    if (now - lastCommandTime < COMMAND_COOLDOWN) {
      unsigned long waitTime = (COMMAND_COOLDOWN - (now - lastCommandTime)) / 1000;
      Serial.println("⏳ Rate limit: comando ignorado");
      bot->sendMessage(chat_id, "⏳ *Aguarde " + String(waitTime) + "s* antes de enviar outro comando.", "Markdown");
      continue;
    }
    lastCommandTime = now;
    
    // ========== PROCESSAMENTO DE COMANDOS ==========
    if (text == "/start") {
      bot->sendMessage(chat_id, welcomeMessage(), "Markdown");
      Serial.println("✅ /start executado");
    }
    else if (text == "/help") {
      bot->sendMessage(chat_id, welcomeMessage(), "Markdown");
      Serial.println("✅ /help executado");
    }
    else if (text == "/status") {
      bot->sendMessage(chat_id, readSensor(), "Markdown");
      Serial.println("✅ /status executado");
    }
    else if (text == "/ledon") {
      digitalWrite(LED_PIN, LOW);  // LOW = LED aceso (invertido)
      ledState = true;
      bot->sendMessage(chat_id, "✅ *LED ligado!* 💡", "Markdown");
      Serial.println("✅ LED ligado");
    }
    else if (text == "/ledoff") {
      digitalWrite(LED_PIN, HIGH); // HIGH = LED apagado
      ledState = false;
      bot->sendMessage(chat_id, "⚫ *LED desligado!*", "Markdown");
      Serial.println("✅ LED desligado");
    }
    else if (text == "/resetwifi") {
      // Reset WiFi Manager (apaga credenciais salvas)
      bot->sendMessage(chat_id, "🔄 *Resetando WiFi...* Configure novamente pelo portal.", "Markdown");
      delay(1000);
      wifiManager.resetSettings();
      ESP.reset();
    }
    else {
      String error = "❓ *Comando não reconhecido:* `" + text + "`\n\n";
      error += "Digite /help para ver os comandos disponíveis.";
      bot->sendMessage(chat_id, error, "Markdown");
    }
  }
}

// Setup
void setup() {
  Serial.begin(115200);
  delay(500);
  
  Serial.println();
  Serial.println("===========================================");
  Serial.println("🤖 Bot Telegram IoT - NodeMCU ESP8266 v2");
  Serial.println("===========================================");
  
  // Inicializar LED
  pinMode(LED_PIN, OUTPUT);
  digitalWrite(LED_PIN, HIGH); // LED desligado initially
  
  // Inicializar DHT
  dht.begin();
  
  // Configurar WiFi com WiFiManager
  Serial.println("🔧 Configurando WiFi...");
  Serial.println("   Procure a rede 'IoT-Bot-Config' no seu celular");
  wifiManager.autoConnect("IoT-Bot-Config");
  
  Serial.println("✅ WiFi conectado!");
  Serial.print("📶 IP: ");
  Serial.println(WiFi.localIP());
  Serial.print("📶 RSSI (sinal): ");
  Serial.print(WiFi.RSSI());
  Serial.println(" dBm");
  
  // Inicializar Telegram Bot
  #include "secrets.h"
  secured_client.setInsecure(); // ⚠️ Para testes apenas! Produção: usar setTrustAnchors
  bot = new UniversalTelegramBot(TELEGRAM_BOT_TOKEN, secured_client);
  
  Serial.println("✅ Bot Telegram inicializado!");
  Serial.println("📱 Envie /start para o bot!");
}

// Loop principal
void loop() {
  // Verifica WiFi a cada 30 segundos
  static unsigned long lastWiFiCheck = 0;
  if (millis() - lastWiFiCheck > 30000) {
    checkWiFiConnection();
    lastWiFiCheck = millis();
  }
  
  // Verificar novas mensagens
  if (millis() - lastMessageTime > BOT_INTERVAL) {
    int numNewMessages = bot->getUpdates(bot->last_message_received + 1);
    
    if (numNewMessages) {
      Serial.println("📨 Nova(s) mensagem(ns): " + String(numNewMessages));
      handleNewMessages(numNewMessages);
    }
    
    lastMessageTime = millis();
  }
  
  // Small delay para não sobrecarregar
  delay(10);
}
