/*
 * Código 3: Persistência com LittleFS + ArduinoJson
 * 
 * PROBLEMA: RTC_DATA_ATTR só funciona no ESP32!
 * SOLUÇÃO: Usar LittleFS (filesystem interno) + ArduinoJson
 * 
 * Por que LittleFS em vez de SPIFFS?
 * - LittleFS é mais novo e mais eficiente para escritas frequentes
 * - Suporta diretórios
 * - Melhor gestão de wear-leveling
 * 
 * Vantagens sobre RTC_DATA_ATTR:
 * - ✅ Funciona no ESP8266 (e ESP32!)
 * - ✅ Sobrevive a power-off (dados persistem)
 * - ✅ Estruturas dinâmicas (JSON)
 * - ✅ Pode armazenar arquivos
 * - ✅ Pode guardar configurações complexas
 * 
 * Desvantagens:
 * - ⚠️ Mais lento que RTC memory
 * - ⚠️ Wear da flash (mas LittleFS distribui escritas)
 * - ⚠️ Usa mais memória (ArduinoJson)
 * 
 * Para instalar:
 * 1. ArduinoJson: Biblioteca → Gerenciador → "ArduinoJson" → Instalar
 * 2. LittleFS: Já vem com ESP8266 Arduino Core
 */

#include <ESP8266WiFi.h>
#include <LittleFS.h>
#include <ArduinoJson.h>

#define LED_PIN 2
#define ARQUIVO_DADOS "/dados.json"

// === Configurações da estação ===
struct Config {
  bool ntpSincronizado = false;
  time_t epochBase = 0;
  unsigned long millisBase = 0;
  int totalCiclos = 0;
  int contagemDia = 0;      // Leituras feitas durante o dia
  int contagemNoite = 0;    // Tentativas durante a noite
  float ultimaTemp = 0;
  float ultimaUmid = 0;
};

// Objeto global para configurações
Config config;

// === Funções de Persistência ===

bool carregarConfig() {
  Serial.println("\n📂 Carregando dados da flash...");
  
  if (!LittleFS.begin()) {
    Serial.println("❌ Falha ao inicializar LittleFS!");
    return false;
  }
  
  if (!LittleFS.exists(ARQUIVO_DADOS)) {
    Serial.println("📝 Arquivo não existe — primeira vez!");
    return false;
  }
  
  File file = LittleFS.open(ARQUIVO_DADOS, "r");
  if (!file) {
    Serial.println("❌ Falha ao abrir arquivo para leitura!");
    return false;
  }
  
  // Buffer para o JSON (deve ser grande o suficiente!)
  StaticJsonDocument<512> doc;
  DeserializationError error = deserializeJson(doc, file);
  file.close();
  
  if (error) {
    Serial.printf("❌ Erro ao parsear JSON: %s\n", error.c_str());
    return false;
  }
  
  // Carrega valores para a struct
  config.ntpSincronizado = doc["ntpSincronizado"] | false;
  config.epochBase = doc["epochBase"] | 0;
  config.millisBase = doc["millisBase"] | 0;
  config.totalCiclos = doc["totalCiclos"] | 0;
  config.contagemDia = doc["contagemDia"] | 0;
  config.contagemNoite = doc["contagemNoite"] | 0;
  config.ultimaTemp = doc["ultimaTemp"] | 0.0;
  config.ultimaUmid = doc["ultimaUmid"] | 0.0;
  
  Serial.println("✅ Dados carregados com sucesso!");
  return true;
}

bool salvarConfig() {
  Serial.println("\n💾 Salvando dados na flash...");
  
  StaticJsonDocument<512> doc;
  
  doc["ntpSincronizado"] = config.ntpSincronizado;
  doc["epochBase"] = config.epochBase;
  doc["millisBase"] = config.millisBase;
  doc["totalCiclos"] = config.totalCiclos;
  doc["contagemDia"] = config.contagemDia;
  doc["contagemNoite"] = config.contagemNoite;
  doc["ultimaTemp"] = config.ultimaTemp;
  doc["ultimaUmid"] = config.ultimaUmid;
  
  File file = LittleFS.open(ARQUIVO_DADOS, "w");
  if (!file) {
    Serial.println("❌ Falha ao abrir arquivo para escrita!");
    return false;
  }
  
  if (serializeJson(doc, file) == 0) {
    Serial.println("❌ Erro ao serializar JSON!");
    file.close();
    return false;
  }
  
  file.close();
  Serial.println("✅ Dados salvos com sucesso!");
  return true;
}

// === Funções de Tempo ===

time_t horaAtual() {
  if (!config.ntpSincronizado) return 0;
  return config.epochBase + (millis() - config.millisBase) / 1000;
}

String formatarHora(time_t t) {
  struct tm* tm_info = localtime(&t);
  char buffer[20];
  strftime(buffer, sizeof(buffer), "%d/%m/%Y %H:%M:%S", tm_info);
  return String(buffer);
}

// === Setup ===
void setup() {
  Serial.begin(115200);
  delay(100);
  
  pinMode(LED_PIN, OUTPUT);
  
  // Tenta carregar dados salvos
  bool dadosExistentes = carregarConfig();
  
  config.totalCiclos++;
  
  Serial.println("\n╔══════════════════════════════════════════════╗");
  Serial.printf("║  CICLO #%04d — LittleFS + ArduinoJson          ║\n", config.totalCiclos);
  Serial.println("╚══════════════════════════════════════════════╝");
  
  if (dadosExistentes) {
    Serial.println("📊 Dados carregados da flash:");
    Serial.printf("   Total de ciclos: %d\n", config.totalCiclos);
    Serial.printf("   Leituras de dia: %d\n", config.contagemDia);
    Serial.printf("   Leituras de noite: %d\n", config.contagemNoite);
    if (config.ntpSincronizado) {
      Serial.printf("   Última temperatura: %.1f°C\n", config.ultimaTemp);
      Serial.printf("   Última umidade: %.1f%%\n", config.ultimaUmid);
      Serial.printf("   Hora atual: %s\n", formatarHora(horaAtual()).c_str());
    }
  }
  
  // Feedback visual
  digitalWrite(LED_PIN, LOW);
  delay(1000);
  digitalWrite(LED_PIN, HIGH);
  
  // Simula "trabalho" — aqui seria a leitura do sensor
  config.ultimaTemp = 25.3 + random(-20, 20) / 10.0;  // Simula leitura
  config.ultimaUmid = 65.0 + random(-50, 50) / 10.0;
  
  // Salva os novos dados
  salvarConfig();
  
  Serial.println("\n💤 Ciclo concluído. Dormindo 10 segundos...");
  Serial.println("(Na versão real, dormiria até detectar luz novamente)");
  
  ESP.deepSleep(10e6);  // 10 segundos (para demo)
}

void loop() {
  // Nunca executa!
}

/*
 * NOTA IMPORTANTE sobre LittleFS no ESP8266:
 * 
 * LittleFS.format() em caso de corrupção:
 * Se o filesystem ficar corrompido, você pode usar:
 *   LittleFS.format();
 * antes de LittleFS.begin()
 * 
 * CUIDADO: Apaga todos os dados!
 * 
 * Para debugging, você pode listar arquivos:
 * 
 *   Dir dir = LittleFS.openDir("/");
 *   while (dir.next()) {
 *     Serial.println(dir.fileName());
 *   }
 */
