/*
 * PROJETO 5: Estação Solar de Monitoramento
 * ===========================================
 * Sistema autônomo que só acorda quando detecta luz (dia)
 * Usa LittleFS + ArduinoJson para persistência (funciona no ESP8266!)
 * 
 * HARDWARE NECESSÁRIO:
 * - NodeMCU ESP8266
 * - LDR (Light Dependent Resistor)
 * - Transistor KSP2222A (NPN)
 * - Trimpot 10kΩ ou 100kΩ
 * - Resistor 10kΩ
 * - DHT11 (sensor de temperatura/umidade)
 * - LED (para feedback)
 * - Protoboard e jumpers
 * 
 * CIRCUITO DO SENSOR DE LUZ:
 * 
 *   3.3V ──── LDR ──── ◬─── Base do KSP2222A (via resistor 10kΩ)
 *                        │
 *                   Trimpot
 *                        │
 *                       GND
 *   
 *   Coletor do KSP2222A ─── RST do ESP8266
 *   Emissor do KSP2222A ─── GND
 * 
 * FUNCIONAMENTO:
 * 1. Noite: LDR tem alta resistência → transistor OFF → ESP dorme
 * 2. Amanhecer: luz aumenta → LDR resistência cai → transistor ON
 * 3. Transistor ON → RST LOW → ESP ACORDA!
 * 4. ESP lê sensor, salva dados, volta a dormir
 * 5. Se ainda estiver dia, transistor ainda está ON → ESP acorda de novo
 * 6. Noite: transistor OFF → ESP fica dormindo até amanhecer
 * 
 * AJUSTE DO TRIMPOT:
 * - Gire para lado do LDR = detecta mais luz (amanhecer mais cedo)
 * - Gire para lado do GND = detecta menos luz ( só acorda com sol forte)
 * 
 * BIBLIOTECAS NECESSÁRIAS:
 * - ArduinoJson (via Library Manager)
 * - DHT sensor library (via Library Manager)
 */

#include <ESP8266WiFi.h>
#include <LittleFS.h>
#include <ArduinoJson.h>
#include <DHT.h>
#include <NTPClient.h>
#include <WiFiUdp.h>

// ===========================================
// CONFIGURAÇÕES — EDITAR AQUI
// ===========================================
#define DHT_PIN D4
#define DHT_TYPE DHT11
#define LED_PIN 2
#define LDR_PIN A0  // Leitura do divisor de tensão (opcional, para debug)

const char* ssid = "SUA_REDE_WIFI";
const char* senha = "SUA_SENHA_WIFI";

// Arquivo de dados na flash
#define ARQUIVO_ESTADO "/estado.json"
#define ARQUIVO_LEITURAS "/leituras.json"

// Intervalo de sleep (quando acordado por luz, dormir X segundos)
#define INTERVALO_SLEEP 60e6  // 60 segundos (ajustar conforme necessidade)

// Limiar de luz para o LDR (0-1023, ADC do ESP8266)
// Valor alto = mais luz
#define LIMIAR_LUZ 500

// ===========================================
// ESTRUTURAS DE DADOS
// ===========================================

struct Estado {
  bool ntpOk = false;
  time_t epochBase = 0;
  unsigned long millisBase = 0;
  int totalCiclos = 0;
  int ciclosDia = 0;      // Ciclos realizados durante o dia
  int ciclosNoite = 0;    // Tentativas durante a noite (0 = normal, >0 = muito escuro)
};

struct Leitura {
  time_t timestamp;
  float temperatura;
  float umidade;
  int leituraLDR;
  bool valida;
};

const int MAX_LEITURAS = 20;  // Histórico máximo na flash

// ===========================================
// OBJETOS GLOBAIS
// ===========================================

DHT dht(DHT_PIN, DHT_TYPE);
WiFiUDP ntpUDP;
NTPClient timeClient(ntpUDP, "pool.ntp.org", -10800, 60000);

Estado estado;
Leitura leituras[MAX_LEITURAS];
int posicaoLeitura = 0;

// ===========================================
// FUNÇÕES DE PERSISTÊNCIA (LittleFS + ArduinoJson)
// ===========================================

bool carregarEstado() {
  if (!LittleFS.begin()) {
    Serial.println("❌ LittleFS não inicializado!");
    return false;
  }
  
  if (!LittleFS.exists(ARQUIVO_ESTADO)) {
    Serial.println("📝 Primeira inicialização!");
    return false;
  }
  
  File file = LittleFS.open(ARQUIVO_ESTADO, "r");
  if (!file) {
    Serial.println("❌ Erro ao abrir estado!");
    return false;
  }
  
  StaticJsonDocument<512> doc;
  DeserializationError error = deserializeJson(doc, file);
  file.close();
  
  if (error) {
    Serial.printf("❌ Erro parse: %s\n", error.c_str());
    return false;
  }
  
  estado.ntpOk = doc["ntpOk"] | false;
  estado.epochBase = doc["epochBase"] | 0;
  estado.millisBase = doc["millisBase"] | 0;
  estado.totalCiclos = doc["totalCiclos"] | 0;
  estado.ciclosDia = doc["ciclosDia"] | 0;
  estado.ciclosNoite = doc["ciclosNoite"] | 0;
  
  return true;
}

bool salvarEstado() {
  StaticJsonDocument<512> doc;
  doc["ntpOk"] = estado.ntpOk;
  doc["epochBase"] = estado.epochBase;
  doc["millisBase"] = estado.millisBase;
  doc["totalCiclos"] = estado.totalCiclos;
  doc["ciclosDia"] = estado.ciclosDia;
  doc["ciclosNoite"] = estado.ciclosNoite;
  
  File file = LittleFS.open(ARQUIVO_ESTADO, "w");
  if (!file) return false;
  
  if (serializeJson(doc, file) == 0) {
    file.close();
    return false;
  }
  
  file.close();
  return true;
}

bool carregarLeituras() {
  if (!LittleFS.exists(ARQUIVO_LEITURAS)) {
    return false;
  }
  
  File file = LittleFS.open(ARQUIVO_LEITURAS, "r");
  if (!file) return false;
  
  StaticJsonDocument<1024> doc;
  DeserializationError error = deserializeJson(doc, file);
  file.close();
  
  if (error) return false;
  
  posicaoLeitura = doc["pos"] | 0;
  
  JsonArray arr = doc["leituras"];
  int i = 0;
  for (JsonObject item : arr) {
    if (i >= MAX_LEITURAS) break;
    leituras[i].timestamp = item["t"] | 0;
    leituras[i].temperatura = item["temp"] | 0.0;
    leituras[i].umidade = item["umid"] | 0.0;
    leituras[i].leituraLDR = item["ldr"] | 0;
    leituras[i].valida = item["valida"] | false;
    i++;
  }
  
  return true;
}

bool salvarLeituras() {
  StaticJsonDocument<1024> doc;
  
  doc["pos"] = posicaoLeitura;
  
  JsonArray arr = doc.createNestedArray("leituras");
  for (int i = 0; i < MAX_LEITURAS; i++) {
    if (leituras[i].valida) {
      JsonObject item = arr.createNestedObject();
      item["t"] = leituras[i].timestamp;
      item["temp"] = leituras[i].temperatura;
      item["umid"] = leituras[i].umidade;
      item["ldr"] = leituras[i].leituraLDR;
      item["valida"] = leituras[i].valida;
    }
  }
  
  File file = LittleFS.open(ARQUIVO_LEITURAS, "w");
  if (!file) return false;
  
  if (serializeJson(doc, file) == 0) {
    file.close();
    return false;
  }
  
  file.close();
  return true;
}

// ===========================================
// FUNÇÕES DE TEMPO
// ===========================================

time_t horaAtual() {
  if (!estado.ntpOk) return 0;
  return estado.epochBase + (millis() - estado.millisBase) / 1000;
}

String formatarHora(time_t t) {
  if (t == 0) return "---";
  struct tm* tm_info = localtime(&t);
  char buffer[30];
  strftime(buffer, sizeof(buffer), "%d/%m %H:%M:%S", tm_info);
  return String(buffer);
}

// ===========================================
// NTP
// ===========================================

bool sincronizarNTP() {
  Serial.println("📡 Conectando Wi-Fi...");
  
  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, senha);
  
  int t = 0;
  while (WiFi.status() != WL_CONNECTED && t < 30) {
    delay(500);
    Serial.print(".");
    t++;
  }
  
  if (WiFi.status() != WL_CONNECTED) {
    Serial.println("\n❌ Wi-Fi falhou!");
    WiFi.mode(WIFI_OFF);
    return false;
  }
  
  Serial.println("\n✅ Wi-Fi conectado!");
  
  timeClient.begin();
  delay(500);
  timeClient.update();
  
  estado.epochBase = timeClient.getEpochTime();
  estado.millisBase = millis();
  estado.ntpOk = true;
  
  Serial.printf("🕐 NTP: %s\n", formatarHora(estado.epochBase).c_str());
  
  WiFi.disconnect(true);
  WiFi.mode(WIFI_OFF);
  Serial.println("📡 Wi-Fi desligado");
  
  return true;
}

// ===========================================
// SENSOR
// ===========================================

void lerSensor(float& temp, float& umid, int& ldr) {
  // Lê DHT
  temp = dht.readTemperature();
  umid = dht.readHumidity();
  
  // Lê LDR (divisor de tensão)
  ldr = analogRead(LDR_PIN);
  
  // Se DHT falhar, usa valores inválidos
  if (isnan(temp)) temp = -999;
  if (isnan(umid)) umid = -999;
}

// ===========================================
// HISTÓRICO
// ===========================================

void adicionarLeitura(time_t timestamp, float temp, float umid, int ldr) {
  leituras[posicaoLeitura].timestamp = timestamp;
  leituras[posicaoLeitura].temperatura = temp;
  leituras[posicaoLeitura].umidade = umid;
  leituras[posicaoLeitura].leituraLDR = ldr;
  leituras[posicaoLeitura].valida = true;
  
  posicaoLeitura = (posicaoLeitura + 1) % MAX_LEITURAS;
  
  salvarLeituras();
}

void imprimirHistorico() {
  Serial.println("\n📊 === HISTÓRICO (últimas 10 leituras) ===");
  
  // Mostra do mais antigo ao mais recente
  int inicio = (posicaoLeitura >= 10) ? (posicaoLeitura - 10) : 0;
  
  for (int i = inicio; i < posicaoLeitura; i++) {
    Leitura& l = leituras[i];
    if (l.valida) {
      Serial.printf("  %s | %.1f°C | %.1f%% | LDR:%d\n",
        formatarHora(l.timestamp).c_str(),
        l.temperatura,
        l.umidade,
        l.leituraLDR);
    }
  }
  
  Serial.println("===========================================");
}

// ===========================================
// AUTONOMIA
// ===========================================

void calcularAutonomia() {
  // Dados típicos
  float capacidadeBat = 3000.0;  // mAh (bateria 18650)
  float consumoAcordado = 80.0;   // mA (com Wi-Fi)
  float consumoDormindo = 0.02;   // mA (deep sleep)
  float tempoAcordado = 5.0;      // segundos
  float intervalosDia = 288.0;   // ciclos por dia (se acordar a cada 5 min)
  
  // Consumo efetivo por dia (estimativa)
  float consumoDiaAcordado = consumoAcordado * (tempoAcordado / 3600.0) * intervalosDia;
  float consumoDiaDormindo = consumoDormindo * 24.0;
  
  float consumoTotalDia = consumoDiaAcordado + consumoDiaDormindo;
  float autonomia = capacidadeBat / consumoTotalDia;
  
  Serial.printf("\n🔋 Autonomia estimada (bateria 3000mAh): %.0f dias\n", autonomia);
  Serial.printf("   Consumo acordado: %.1f mAh/dia\n", consumoDiaAcordado);
  Serial.printf("   Consumo dormindo: %.2f mAh/dia\n", consumoDiaDormindo);
}

// ===========================================
// MAIN
// ===========================================

void setup() {
  Serial.begin(115200);
  delay(100);
  
  pinMode(LED_PIN, OUTPUT);
  dht.begin();
  
  // Inicializa LittleFS
  LittleFS.begin();
  
  // Carrega dados salvos
  carregarEstado();
  carregarLeituras();
  
  // Incrementa ciclos
  estado.totalCiclos++;
  
  // Lê valor do LDR para saber se é dia ou noite
  int ldrValor = analogRead(LDR_PIN);
  bool ehDia = (ldrValor > LIMIAR_LUZ);
  
  Serial.println("\n╔══════════════════════════════════════════════╗");
  Serial.printf("║  ☀️  ESTAÇÃO SOLAR — Ciclo #%04d              ║\n", estado.totalCiclos);
  Serial.println("╚══════════════════════════════════════════════╝");
  
  Serial.printf("📈 LDR: %d (%s)\n", ldrValor, ehDia ? "DIA ☀️" : "NOITE 🌙");
  
  if (ehDia) {
    estado.ciclosDia++;
  } else {
    estado.ciclosNoite++;
  }
  
  // Feedback visual — LED acende
  digitalWrite(LED_PIN, LOW);
  
  // Sincroniza NTP se necessário
  if (!estado.ntpOk) {
    sincronizarNTP();
  }
  
  // Lê sensor
  float temp, umid;
  lerSensor(temp, umid, ldrValor);
  
  time_t agora = horaAtual();
  
  Serial.printf("🌡️ Temperatura: %.1f °C\n", temp);
  Serial.printf("💧 Umidade: %.1f %%\n", umid);
  Serial.printf("🕐 Timestamp: %s\n", formatarHora(agora).c_str());
  
  // Salva leitura
  adicionarLeitura(agora, temp, umid, ldrValor);
  
  // Mostra histórico a cada 10 ciclos
  if (estado.totalCiclos % 10 == 0) {
    imprimirHistorico();
  }
  
  // Salva estado
  salvarEstado();
  
  // Desliga LED
  digitalWrite(LED_PIN, HIGH);
  
  // Calcula e mostra autonomia
  calcularAutonomia();
  
  // Decide se dorme ou não baseado na luz
  if (!ehDia) {
    Serial.println("\n🌙 NOITE — Não há luz suficiente!");
    Serial.println("   transistor OFF → ESP fica em deep sleep");
    Serial.println("   Só acordará quando transistor ligar (amanhecer)");
    Serial.printf("   💡 Dica: Ajuste o trimpot para um limiar menor\n");
    Serial.printf("   para que acorde mais cedo de manhã.\n");
  } else {
    Serial.println("\n☀️ DIA — Ciclo completo, voltando a dormir...");
    Serial.printf("   Próximo ciclo em ~%d segundos\n", (int)(INTERVALO_SLEEP / 1000000));
  }
  
  Serial.println("───────────────────────────────────────────");
  
  // Deep sleep!
  // Se for dia: dorme por INTERVALO_SLEEP e acorda (transistor ainda liga)
  // Se for noite: deepSleep(0) só acorda quando transistor ligar (amanhecer)
  if (ehDia) {
    ESP.deepSleep(INTERVALO_SLEEP);
  } else {
    ESP.deepSleep(0);  // Só acorda por RST (transistor)
  }
}

void loop() {
  // NUNCA executa!
}

/*
 * ===========================================
 * CIRCUITO COMPLETO — ESTAÇÃO SOLAR
 * ===========================================
 * 
 * COMPONENTES:
 * - NodeMCU ESP8266
 * - LDR (Sensor de luz)
 * - Transistor KSP2222A (NPN)
 * - Trimpot 10-100kΩ
 * - Resistor 10kΩ
 * - DHT11 (temperatura/umidade)
 * - LED (feedback)
 * 
 * FIO OBRIGATÓRIO: D0 (GPIO16) → RST (para deep sleep funcionar)
 * 
 * ESQUEMA DE PINAGEM:
 * 
 *    NodeMCU ESP8266
 *    ┌──────────────────────────────────┐
 *    │                                  │
 *    │  3.3V ──────────────────────────┼───────┐
 *    │                                  │       │
 *    │  D0/GPIO16 ─────────────────────┼──┬────┤  RST
 *    │                                  │  │    │
 *    │  D4 ─────────────────────────────┼──┤    │
 *    │  (DHT11)                         │  │    │
 *    │                                  │  │    │
 *    │  A0 ─────────────────────────────┼──┤    │
 *    │  (debug opcional)                │  │    │
 *    │                                  │  │    │
 *    │  2 (LED) ─────────────────────────┼──┘    │
 *    │                                  │       │
 *    │  GND ────────────────────────────└───────┘
 *    │                                              │
 *    └──────────────────────────────────────────────┘
 *    
 *    KSP2222A (vista de frente)
 *         ┌──────────────┐
 *         │  B    C      │
 *         │  │    │      │
 *         └──│────│──────┘
 *            │    │
 *            │    └──────────→ RST do ESP8266
 *            │
 *            └──────┬──── R (10kΩ) ─── LDR ─── 3.3V
 *                   │
 *               Trimpot
 *                   │
 *                  GND
 * 
 * CIRCUITO DO LDR:
 * 
 *   3.3V ─── LDR ──────┬────────── Base (B) do KSP2222A
 *                      │
 *                 Trimpot
 *                      │
 *                     GND
 * 
 * Ligação do Transistor:
 * - Emissor (E): GND
 * - Base (B): Via resistor 10kΩ + LDR + Trimpot (divisor de tensão)
 * - Coletor (C): RST do ESP8266
 * 
 * COMO FUNCIONA:
 * 1. Luz alta (dia): LDR tem baixa resistência (~10kΩ)
 *    → Divisor de tensão gera tensão alta na base
 *    → Transistor satura → Coletor (C) vai LOW
 *    → RST vai LOW → ESP8266 ACORDA!
 * 
 * 2. Luz baixa (noite): LDR tem alta resistência (~1MΩ)
 *    → Divisor de tensão gera tensão baixa na base
 *    → Transistor corta → Coletor fica "aberto"
 *    → RST não é puxado LOW → ESP8266 DORME!
 * 
 * AJUSTE DO TRIMPOT:
 * - Gire para lado do LDR: limiar mais baixo = acorda com menos luz
 * - Gire para lado do GND: limiar mais alto = só acorda com sol forte
 * - Objetivo: acordar ~6h da manhã, dormir ~6h da noite
 * 
 * NOTA: O ESP8266 acorda brevemente quando deepSleep(0) é chamado
 * porque ele faz um reset. Para evitar loops infinitos de dia,
 * usamos deepSleep(INTERVALO_SLEEP) para dormir por um tempo.
 */
