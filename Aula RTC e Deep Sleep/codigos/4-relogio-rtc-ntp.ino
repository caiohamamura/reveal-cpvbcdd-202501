/*
 * Código 4: Relógio que Não Esquece
 * Sincroniza NTP uma vez, mantém hora via RTC memory
 * 
 * Como funciona:
 * 1. Primeiro ciclo: conecta Wi-Fi, sincroniza NTP, salva epoch na RTC memory
 * 2. Ciclos seguintes: calcula hora sem Wi-Fi (economia de energia!)
 * 3. Wi-Fi é desligado após sincronização
 * 
 * Hardware:
 * - Fio D0 → RST
 * - (DHT11 opcional para aula 4)
 */

#include <ESP8266WiFi.h>
#include <WiFiUdp.h>
#include <NtpClientLib.h>

// RTC memory — persiste entre ciclos de deep sleep
RTC_DATA_ATTR bool ntpSincronizado = false;
RTC_DATA_ATTR time_t epochBase = 0;
RTC_DATA_ATTR unsigned long millisBase = 0;
RTC_DATA_ATTR int ciclos = 0;

const char* ssid = "SUA_REDE_WIFI";
const char* senha = "SUA_SENHA_WIFI";

void setup() {
  Serial.begin(115200);
  delay(100);
  
  ciclos++;
  Serial.printf("\n========================================\n");
  Serial.printf("  CICLO #%d\n", ciclos);
  Serial.printf("========================================\n");
  
  // === Sincronizar NTP (só na primeira vez) ===
  if (!ntpSincronizado) {
    Serial.println("📡 Primeira vez! Conectando Wi-Fi...");
    WiFi.mode(WIFI_STA);
    WiFi.begin(ssid, senha);
    
    int tentativas = 0;
    while (WiFi.status() != WL_CONNECTED && tentativas < 30) {
      delay(500);
      Serial.print(".");
      tentativas++;
    }
    
    if (WiFi.status() == WL_CONNECTED) {
      Serial.println("\n✅ Wi-Fi conectado!");
      Serial.print("IP: ");
      Serial.println(WiFi.localIP());
      
      // Sincroniza NTP
      Serial.println("🕐 Sincronizando NTP...");
      NTP.begin("pool.ntp.org", -3);  // GMT-3 (Brasília)
      NTP.waitSet();
      
      // Salva referência de tempo
      epochBase = time(nullptr);
      millisBase = millis();
      ntpSincronizado = true;
      
      Serial.printf("✅ Hora NTP: %s", ctime(&epochBase));
      
      // Desliga Wi-Fi para economizar energia
      WiFi.disconnect(true);
      WiFi.mode(WIFI_OFF);
      Serial.println("📡 Wi-Fi desligado (economia)");
    } else {
      Serial.println("\n❌ Falha ao conectar Wi-Fi!");
      Serial.println("Hora não sincronizada. Tentando novamente no próximo ciclo.");
    }
  }
  
  // === Calcular hora atual ===
  if (ntpSincronizado) {
    time_t agora = epochBase + (millis() - millisBase) / 1000;
    struct tm* t = localtime(&agora);
    char buffer[30];
    strftime(buffer, sizeof(buffer), "%d/%m/%Y %H:%M:%S", t);
    Serial.printf("🕐 Hora atual (sem Wi-Fi): %s\n", buffer);
  } else {
    Serial.println("⚠️ Hora não disponível (NTP não sincronizado)");
  }
  
  // === Deep Sleep ===
  Serial.println("\n💤 Dormindo 5 minutos...");
  Serial.printf("========================================\n");
  ESP.deepSleep(300e6);  // 5 minutos
}

void loop() {}
