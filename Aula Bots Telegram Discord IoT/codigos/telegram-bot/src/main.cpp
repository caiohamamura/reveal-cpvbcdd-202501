/*
 * Bot Telegram para NodeMCU ESP8266
 * Controle de LED e leitura de sensor DHT22
 * Usando AsyncTelegram2
 * 
 * Comandos:
 * /start   - Mostra mensagem de boas-vindas
 * /status  - Mostra temperatura e umidade
 * /help    - Mostra ajuda
 * 
 * Teclado inline:
 * 💡 LED ON  - Liga o LED
 * ⚫ LED OFF - Desliga o LED
 * 📊 Status  - Mostra status
 */

#include <AsyncTelegram2.h>
#include <DHT.h>
#include "secrets.h"

// Timezone - Brasil (São Paulo)
#define MYTZ "BRT3BRDT,M3.4.0,M10.4.0"

#ifdef ESP8266
  #include <ESP8266WiFi.h>
  #include <WiFiClientSecure.h>
  BearSSL::WiFiClientSecure client;
  BearSSL::Session session;
  BearSSL::X509List certificate(telegram_cert);
#endif

// ========== CONFIGURAÇÕES ==========
#define LED_PIN LED_BUILTIN         // LED embutido (GPIO2)
#define DHT_PIN 4                  // Sensor DHT22 (GPIO4/D2)
#define DHT_TYPE DHT22

// Callbacks para os botões inline
#define CB_LED_ON  "ledON"
#define CB_LED_OFF "ledOFF"
#define CB_STATUS  "status"

// ========== VARIÁVEIS GLOBAIS ==========
DHT dht(DHT_PIN, DHT_TYPE);
AsyncTelegram2 bot(client);
InlineKeyboard myInlineKbd;

bool ledState = false;
bool sensorOK = false;

// ========== PROTÓTIPOS ==========
void sendStatus(const TBMessage &msg);

// ========== CALLBACKS DOS BOTÕES ==========
void onLedOn(const TBMessage &queryMsg) {
  digitalWrite(LED_PIN, LOW);
  ledState = true;
  Serial.println("LED ON via callback");
  bot.endQuery(queryMsg, "💡 LED ligado!", true);
  String reply = "✅ *LED LIGADO*\n\n💡 Use os botões para controlar";
  bot.editMessage(queryMsg, reply, myInlineKbd);
}

void onLedOff(const TBMessage &queryMsg) {
  digitalWrite(LED_PIN, HIGH);
  ledState = false;
  Serial.println("LED OFF via callback");
  bot.endQuery(queryMsg, "⚫ LED desligado!", true);
  String reply = "⚫ *LED DESLIGADO*\n\n💡 Use os botões para controlar";
  bot.editMessage(queryMsg, reply, myInlineKbd);
}

void onStatus(const TBMessage &queryMsg) {
  Serial.println("Status via callback");
  sendStatus(queryMsg);
  bot.endQuery(queryMsg, "📊 Status atualizado!", true);
}

// ========== FUNÇÕES ==========

// Enviar status do sistema
void sendStatus(const TBMessage &msg) {
  String reply = "📊 *Status do Sistema*\n\n";
  
  // Leitura do sensor DHT22
  float temp = dht.readTemperature();
  float humidity = dht.readHumidity();
  
  if (isnan(temp) || isnan(humidity)) {
    reply += "🌡️ Temperatura: Erro\n";
    reply += "💧 Umidade: Erro\n";
  } else {
    reply += "🌡️ Temperatura: " + String(temp, 1) + " °C\n";
    reply += "💧 Umidade: " + String(humidity, 1) + " %\n";
  }
  
  reply += "\n💡 LED: ";
  reply += ledState ? "*LIGADO*" : "*DESLIGADO*";
  reply += "\n📶 WiFi: ";
  reply += WiFi.RSSI();
  reply += " dBm";

  bot.sendMessage(msg, reply.c_str(), myInlineKbd);
}

// ========== SETUP ==========
void setup() {
  Serial.begin(115200);
  Serial.println("\n=== Bot Telegram IoT - AsyncTelegram2 ===");

  // Configurar pinos
  pinMode(LED_PIN, OUTPUT);
  digitalWrite(LED_PIN, HIGH); // LED desligado inicialmente

  // Inicializar sensor DHT
  dht.begin();
  float temp = dht.readTemperature();
  float humidity = dht.readHumidity();
  if (!isnan(temp) && !isnan(humidity)) {
    sensorOK = true;
    Serial.println("Sensor DHT22 OK!");
  } else {
    Serial.println("Sensor DHT22 não encontrado!");
  }

  // Conectar WiFi
  WiFi.mode(WIFI_STA);
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  
  Serial.print("Conectando ao WiFi: ");
  Serial.print(WIFI_SSID);
  
  int attempts = 0;
  while (WiFi.status() != WL_CONNECTED && attempts < 30) {
    delay(500);
    Serial.print(".");
    attempts++;
  }
  
  if (WiFi.status() == WL_CONNECTED) {
    Serial.println("\nWiFi conectado!");
    Serial.print("IP: ");
    Serial.println(WiFi.localIP());
  } else {
    Serial.println("\nFalha ao conectar WiFi!");
    return;
  }

#ifdef ESP8266
  // Configurar hora para certificado TLS
  configTime(MYTZ, "time.google.com", "time.windows.com", "pool.ntp.org");
  client.setSession(&session);
  client.setTrustAnchors(&certificate);
  client.setBufferSizes(1024, 1024);
#endif

  // Inicializar bot
  bot.setUpdateTime(1000);
  bot.setTelegramToken(TELEGRAM_BOT_TOKEN);

  Serial.print("Testando conexão com Telegram... ");
  if (bot.begin()) {
    Serial.println("OK!");
    Serial.print("Nome do Bot: @");
    Serial.println(bot.getBotName());
    digitalWrite(LED_PIN, LOW); // LED ligado = bot online
    delay(500);
    digitalWrite(LED_PIN, HIGH);
  } else {
    Serial.println("FALHA!");
    return;
  }

  // Configurar teclado inline com callbacks
  myInlineKbd.addButton("💡 LED ON", CB_LED_ON, KeyboardButtonQuery, onLedOn);
  myInlineKbd.addButton("⚫ LED OFF", CB_LED_OFF, KeyboardButtonQuery, onLedOff);
  myInlineKbd.addRow();
  myInlineKbd.addButton("📊 Status", CB_STATUS, KeyboardButtonQuery, onStatus);

  Serial.println("\nComandos disponíveis:");
  Serial.println("/start - Mensagem de boas-vindas");
  Serial.println("/status - Status do sistema");
  Serial.println("/help - Ajuda");
}

// ========== LOOP ==========
void loop() {
  // LED pisca para indicar que está rodando
  static uint32_t ledTime = 0;
  if (millis() - ledTime > 1000) {
    ledTime = millis();
    digitalWrite(LED_PIN, !digitalRead(LED_PIN)); // Pisca LED
  }

  TBMessage msg;
  if (bot.getNewMessage(msg)) {
    MessageType msgType = msg.messageType;
    String msgText = msg.text;

    switch (msgType) {
      case MessageText:
        // Mensagens de texto
        Serial.print("Texto: ");
        Serial.println(msgText);

        if (msgText.equalsIgnoreCase("/start") || msgText.equalsIgnoreCase("/help")) {
          String reply = "🤖 *Bot IoT - ESP8266*\n\n";
          reply += "Bem-vindo! Este bot controla seu dispositivo IoT.\n\n";
          reply += "*Comandos:*\n";
          reply += "/start - Esta mensagem\n";
          reply += "/status - Ver temperatura e umidade\n";
          reply += "/help - Ajuda\n\n";
          reply += "*Use os botões abaixo para controlar o LED:*";
          bot.sendMessage(msg, reply.c_str(), myInlineKbd);
        }
        else if (msgText.equalsIgnoreCase("/status")) {
          sendStatus(msg);
        }
        else {
          String reply = "📝 Echo: " + msgText;
          reply += "\n\nUse /start para ver os comandos";
          bot.sendMessage(msg, reply.c_str(), myInlineKbd);
        }
        break;

      case MessageQuery:
        // Callback dos botões inline - tratados automaticamente
        break;

      default:
        break;
    }
  }
}