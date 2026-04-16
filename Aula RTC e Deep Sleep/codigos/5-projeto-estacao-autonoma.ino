/*
 * Código 5: Projeto Integrador — Estação Autônoma de Monitoramento
 * 
 * Funcionalidades:
 * 1. Acorda a cada 5 minutos
 * 2. Lê temperatura e umidade (DHT11)
 * 3. Sincroniza NTP apenas na primeira vez
 * 4. RTC memory preserva hora e contador entre ciclos
 * 5. Timestamp correto em cada leitura
 * 6. Desafio: histórico de 10 leituras na RTC memory
 * 
 * Hardware:
 * - NodeMCU ESP8266
 * - DHT11 no pino D4
 * - LED onboard (GPIO 2)
 * - Fio D0 → RST (obrigatório!)
 * - Bateria ou fonte USB
 */

#include <ESP8266WiFi.h>
#include <DHT.h>
#include <WiFiUdp.h>
#include <NtpClientLib.h>

// === Configuração ===
#define DHT_PIN D4
#define DHT_TYPE DHT11
#define LED_PIN 2
#define TEMP_MAX_ALERTA 30.0  // Alerta acima de 30°C
#define INTERVALO_SLEEP 300e6 // 5 minutos em microssegundos

const char* ssid = "SUA_REDE_WIFI";
const char* senha = "SUA_SENHA_WIFI";

// === Estrutura para histórico de leituras ===
struct Leitura {
  time_t timestamp;
  float temperatura;
  float umidade;
  bool valida;
};

// === RTC Memory — persiste entre deep sleeps ===
RTC_DATA_ATTR bool ntpOk = false;
RTC_DATA_ATTR time_t epochBase = 0;
RTC_DATA_ATTR unsigned long millisBase = 0;
RTC_DATA_ATTR int totalCiclos = 0;
RTC_DATA_ATTR Leitura historico[10] = {};
RTC_DATA_ATTR int posHistorico = 0;

// === Objeto do sensor ===
DHT dht(DHT_PIN, DHT_TYPE);

// === Funções Auxiliares ===

time_t horaAtual() {
  if (!ntpOk) return 0;
  return epochBase + (millis() - millisBase) / 1000;
}

String formatarHora(time_t t) {
  struct tm* tm_info = localtime(&t);
  char buffer[20];
  strftime(buffer, sizeof(buffer), "%d/%m/%Y %H:%M:%S", tm_info);
  return String(buffer);
}

bool sincronizarNTP() {
  Serial.println("📡 Conectando Wi-Fi para NTP...");
  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, senha);
  
  int tentativas = 0;
  while (WiFi.status() != WL_CONNECTED && tentativas < 30) {
    delay(500);
    Serial.print(".");
    tentativas++;
  }
  
  if (WiFi.status() != WL_CONNECTED) {
    Serial.println("\n❌ Falha na conexão Wi-Fi!");
    return false;
  }
  
  Serial.println("\n✅ Wi-Fi conectado!");
  
  NTP.begin("pool.ntp.org", -3);
  NTP.waitSet();
  
  epochBase = time(nullptr);
  millisBase = millis();
  ntpOk = true;
  
  Serial.printf("🕐 NTP sincronizado: %s", ctime(&epochBase));
  
  // Desliga Wi-Fi para economizar
  WiFi.disconnect(true);
  WiFi.mode(WIFI_OFF);
  Serial.println("📡 Wi-Fi desligado");
  
  return true;
}

void imprimirHistorico() {
  Serial.println("\n📊 === HISTÓRICO DE LEITURAS ===");
  for (int i = 0; i < 10; i++) {
    if (historico[i].valida) {
      Serial.printf("  #%d | %s | %.1f°C | %.1f%%\n",
                    i + 1,
                    formatarHora(historico[i].timestamp).c_str(),
                    historico[i].temperatura,
                    historico[i].umidade);
    }
  }
  Serial.println("================================\n");
}

// === Setup — Roda a cada ciclo (após acordar) ===
void setup() {
  Serial.begin(115200);
  delay(100);
  
  pinMode(LED_PIN, OUTPUT);
  dht.begin();
  
  totalCiclos++;
  
  Serial.println("\n╔══════════════════════════════════════╗");
  Serial.printf("║  ESTAÇÃO AUTÔNOMA — Ciclo #%04d      ║\n", totalCiclos);
  Serial.println("╚══════════════════════════════════════╝");
  
  // --- Sincronizar NTP se necessário ---
  if (!ntpOk) {
    sincronizarNTP();
  }
  
  // --- Feedback visual ---
  digitalWrite(LED_PIN, LOW);  // LED ligado = trabalhando
  
  // --- Aguardar estabilização do DHT ---
  delay(2000);
  
  // --- Ler sensor ---
  float temp = dht.readTemperature();
  float umid = dht.readHumidity();
  
  // --- Processar leitura ---
  if (isnan(temp) || isnan(umid)) {
    Serial.println("❌ Erro na leitura do DHT11!");
  } else {
    time_t agora = horaAtual();
    
    Serial.printf("🌡️ Temperatura: %.1f °C\n", temp);
    Serial.printf("💧 Umidade: %.1f %%\n", umid);
    
    if (ntpOk) {
      Serial.printf("🕐 Timestamp: %s\n", formatarHora(agora).c_str());
    }
    
    // Alerta de temperatura
    if (temp > TEMP_MAX_ALERTA) {
      Serial.printf("⚠️ ALERTA! Temperatura acima de %.0f°C!\n", TEMP_MAX_ALERTA);
      // Pisca LED rápido como alerta
      for (int i = 0; i < 5; i++) {
        digitalWrite(LED_PIN, LOW);
        delay(100);
        digitalWrite(LED_PIN, HIGH);
        delay(100);
      }
    }
    
    // --- Salvar no histórico (RTC memory) ---
    historico[posHistorico].timestamp = agora;
    historico[posHistorico].temperatura = temp;
    historico[posHistorico].umidade = umid;
    historico[posHistorico].valida = true;
    posHistorico = (posHistorico + 1) % 10;  // Buffer circular
    
    // --- Imprimir histórico completo ---
    if (totalCiclos % 5 == 0) {  // A cada 5 ciclos
      imprimirHistorico();
    }
  }
  
  // --- Re-sincronizar NTP a cada 100 ciclos (corrigir drift) ---
  if (ntpOk && totalCiclos % 100 == 0) {
    Serial.println("🔄 Re-sincronizando NTP (manutenção)...");
    ntpOk = false;  // Força nova sincronização
  }
  
  // --- Dormir ---
  digitalWrite(LED_PIN, HIGH);  // Desliga LED
  
  // Calcular autonomia estimada
  float consumoAcordado = 80.0;     // mA
  float consumoDormindo = 0.02;     // mA
  float tempoAcordadoSeg = 5.0;     // segundos por ciclo
  float intervaloSeg = 300.0;       // 5 min entre ciclos
  float bateria = 3000.0;           // mAh (18650)
  
  float consumoDia = (consumoAcordado * (tempoAcordadoSeg * 288 / 3600.0)) +
                      (consumoDormindo * (24.0 - tempoAcordadoSeg * 288 / 3600.0));
  float autonomiaDias = bateria / consumoDia;
  
  Serial.printf("\n🔋 Autonomia estimada: %.0f dias (bateria 3000mAh)\n", autonomiaDias);
  Serial.printf("💤 Dormindo %d segundos...\n", INTERVALO_SLEEP / 1000000);
  Serial.println("───────────────────────────────────────\n");
  
  ESP.deepSleep(INTERVALO_SLEEP);
}

void loop() {
  // Nunca executa — deep sleep reinicia do zero
}
