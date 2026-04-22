/*
 * Código 4: Sincronização NTP + LittleFS
 * 
 * Objetivo: Sincronizar hora via NTP UMA VEZ e calcular localmente depois
 * 
 * Conceito de "NTP Inteligente":
 * 1. Primeira vez: conecta Wi-Fi → sincroniza NTP → salva epoch na flash
 * 2. Ciclos seguintes: calcula hora matematicamente (SEM Wi-Fi!)
 * 3. Economia: Wi-Fi consome ~80mA por 5s = muita energia gasta
 *    Sem Wi-Fi = só 5ms a 20mA para calcular o tempo local
 * 
 * Importante:
 * - Não usa RTC_DATA_ATTR (só funciona no ESP32!)
 * - Usa LittleFS + ArduinoJson para persistir epoch e millis
 * - Re-sincroniza a cada 100 ciclos para corrigir drift
 * 
 * Para instalar:
 * - ArduinoJson library (via Library Manager)
 * - NTPClient (já vem com ESP8266 Arduino Core)
 */

#include <ESP8266WiFi.h>
#include <LittleFS.h>
#include <ArduinoJson.h>
#include <NTPClient.h>
#include <WiFiUdp.h>

#define LED_PIN 2
#define ARQUIVO_DADOS "/dados.json"

// Configurações de rede
const char* ssid = "SUA_REDE_WIFI";
const char* senha = "SUA_SENHA_WIFI";

// NTP
WiFiUDP ntpUDP;
NTPClient timeClient(ntpUDP, "pool.ntp.org", -10800, 60000);  // GMT-3 (Brasil)

// Estados do sistema
struct Estado {
  bool ntpSincronizado = false;
  time_t epochBase = 0;
  unsigned long millisBase = 0;
  int ciclos = 0;
};

Estado estado;

bool carregarEstado() {
  if (!LittleFS.begin()) {
    Serial.println("❌ LittleFS falhou!");
    return false;
  }
  
  if (!LittleFS.exists(ARQUIVO_DADOS)) {
    Serial.println("📝 Primeira vez — sem dados salvos");
    return false;
  }
  
  File file = LittleFS.open(ARQUIVO_DADOS, "r");
  StaticJsonDocument<512> doc;
  DeserializationError error = deserializeJson(doc, file);
  file.close();
  
  if (error) {
    Serial.printf("❌ Erro parse: %s\n", error.c_str());
    return false;
  }
  
  estado.ntpSincronizado = doc["ntpSincronizado"] | false;
  estado.epochBase = doc["epochBase"] | 0;
  estado.millisBase = doc["millisBase"] | 0;
  estado.ciclos = doc["ciclos"] | 0;
  
  return true;
}

bool salvarEstado() {
  StaticJsonDocument<512> doc;
  doc["ntpSincronizado"] = estado.ntpSincronizado;
  doc["epochBase"] = estado.epochBase;
  doc["millisBase"] = estado.millisBase;
  doc["ciclos"] = estado.ciclos;
  
  File file = LittleFS.open(ARQUIVO_DADOS, "w");
  if (!file) return false;
  
  serializeJson(doc, file);
  file.close();
  return true;
}

time_t horaAtual() {
  if (!estado.ntpSincronizado) return 0;
  return estado.epochBase + (millis() - estado.millisBase) / 1000;
}

String formatarHora(time_t t) {
  struct tm* tm_info = localtime(&t);
  char buffer[30];
  strftime(buffer, sizeof(buffer), "%d/%m/%Y %H:%M:%S", tm_info);
  return String(buffer);
}

bool sincronizarNTP() {
  Serial.println("\n📡 Conectando Wi-Fi para NTP...");
  
  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, senha);
  
  int tentativas = 0;
  while (WiFi.status() != WL_CONNECTED && tentativas < 30) {
    delay(500);
    Serial.print(".");
    tentativas++;
  }
  
  if (WiFi.status() != WL_CONNECTED) {
    Serial.println("\n❌ Wi-Fi não conectou!");
    WiFi.mode(WIFI_OFF);
    return false;
  }
  
  Serial.println("\n✅ Wi-Fi conectado!");
  
  // Inicializa NTP
  timeClient.begin();
  timeClient.update();
  
  // Aguarda update
  delay(1000);
  
  estado.epochBase = timeClient.getEpochTime();
  estado.millisBase = millis();
  estado.ntpSincronizado = true;
  
  Serial.printf("🕐 NTP: %s\n", formatarHora(estado.epochBase).c_str());
  
  // IMPORTANTE: Desliga Wi-Fi para economizar!
  WiFi.disconnect(true);
  WiFi.mode(WIFI_OFF);
  Serial.println("📡 Wi-Fi desligado (economia de energia!)");
  
  return true;
}

void setup() {
  Serial.begin(115200);
  delay(100);
  
  pinMode(LED_PIN, OUTPUT);
  
  // Carrega dados salvos
  carregarEstado();
  estado.ciclos++;
  
  Serial.println("\n╔══════════════════════════════════════════════╗");
  Serial.printf("║  CICLO #%04d                                   ║\n", estado.ciclos);
  Serial.println("╚══════════════════════════════════════════════╝");
  
  // Sincroniza NTP se necessário
  if (!estado.ntpSincronizado) {
    if (!sincronizarNTP()) {
      Serial.println("⚠️ NTP falhou — continuando sem hora!");
    }
  } else {
    // Verifica se precisa re-sincronizar (a cada 100 ciclos)
    if (estado.ciclos % 100 == 0) {
      Serial.println("🔄 Re-sincronizando NTP (manutenção)...");
      estado.ntpSincronizado = false;
      sincronizarNTP();
    } else {
      Serial.println("✅ NTP já sincronizado — calculando localmente!");
    }
  }
  
  // Mostra hora atual
  if (estado.ntpSincronizado) {
    time_t agora = horaAtual();
    Serial.printf("🕐 Hora atual: %s\n", formatarHora(agora).c_str());
  }
  
  // Salva estado
  salvarEstado();
  
  // Feedback visual
  digitalWrite(LED_PIN, LOW);
  delay(500);
  digitalWrite(LED_PIN, HIGH);
  
  Serial.println("\n💤 Dormindo 30 segundos (para demo)...");
  ESP.deepSleep(30e6);
}

void loop() {
  // Nunca executa!
}

/*
 * 💡 POR QUE ECONOMIZA ENERGIA?
 * 
 * Com Wi-Fi a cada ciclo (5 min):
 * - 5s conectado × 80mA = 400 mAs por ciclo
 * - 288 ciclos/dia × 400 mAs = 115200 mAs = 32 mAh/dia
 * 
 * Sem Wi-Fi (NTP inteligente):
 * - Só conecta 1 vez (5s × 80mA = 400 mAs)
 * - Depois: cálculo local = negligible
 * - 288 ciclos dormindo = ~0,5 mAh/dia
 * 
 * Economia: ~64x menos consumo!
 */
