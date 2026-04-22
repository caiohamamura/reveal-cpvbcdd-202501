# 📊 ROTEIRO DA AULA — RTC, Deep Sleep e Autonomia
## Versão Professor Caio — 22/04/2026

---

### 📍 Context
- **Módulo:** Programação Avançada em IoT (Aula 11)
- **Sequência:** Depois de Timing/NTP → Antes de Máquina de Estados
- **Foco:** Economia de energia + persistência de dados + interrupt por luz

### 🎯 Objetivos
1. Entender **por que** deep sleep é essencial em IoT de campo
2. Implementar deep sleep com despertar por **timer** e por **interrupt (transistor/botão)**
3. Usar **LittleFS + ArduinoJson** para persistir dados (solução ESP8266!)
4. Implementar um projeto com **MQTT + deep sleep** como projeto integrador

### Conceitos-chave
- **Deep Sleep:** 20 μA vs 80 mA = 4000x economia
- **Acorda:** por tempo (D0→RST) ou por sinal (botão/transistor)
- **D0→RST:** Conexão obrigatória para wake por timer
- **KSP2222A:** Transistor NPN como interruptor controlado por luz
- **LittleFS + ArduinoJson:** Persistência que funciona no ESP8266
- **ESP.rtcUserMemoryWrite/Read:** 512 bytes que sobrevivem ao reset (não a power-off!)

### Hardware Especial
- **Transistor KSP2222A** (NPN)
- **LDR** (Light Dependent Resistor)
- **Trimpot** 10kΩ
- **Resistor** 10kΩ (pull-up no RST)
- **Botão Push** (para wake manual)
- **Capacitor** 1µF (opcional, para pulso corto)

---

## 📅 Estrutura (4 aulas × 45 min)

| Aula | Tema | Tipo | Duração |
|------|------|------|---------|
| 1 | Engajamento + Teoria + Pisca-Dorme | Expositiva + Demo | 45 min |
| 2 | Hands-on 1 (guiado): Pisca → Sleep → Botão wake → loop | Prática guiada | 45 min |
| 3 | Hands-on 2 (base a ajustar): LittleFS + NTP + RTC memory | Prática mandiri | 45 min |
| 4 | Projeto: Contador de flashes via MQTT | Projeto em duplas | 45 min |

---

## AULA 1: "POR QUE DORMIR?" (45 min)

### 0-5 min: Abertura — "O Desafio da Bateria"
> "Quanto tempo dura um ESP8266 ligado 24/7 com uma pilha AA (2500mAh)?"
> — ~31 horas (80mA × 2500mAh)

> "E se precisasse funcionar por 6 meses numa fazenda, sem tomada?"
> → Hoje vocês aprendem a fazer o ESP durar **meses**, não horas.

### 5-15 min: Exemplos Reais (5 exemplos)

1. **🏠 Estação meteorológica na fazenda**
   - Mede a cada 30 min, envia via Wi-Fi
   - Sem sleep: 1 dia | Com sleep: **8 meses**

2. **🌾 Irrigação inteligente**
   - Acorda → mede umidade → decide → dorme
   - 5s acordado, 1h dormindo = **4.000x menos energia**

3. **🚨 Sensor de intrusão em galpão**
   - Acorda por movimento (PIR ou botão)
   - 1 ano com bateria 18650 (3000mAh)

4. **🐟 Aquicultura (tanque de peixes)**
   - Mede pH, oxigênio, temperatura
   - Sem sleep: 2 dias | Com sleep: **semanas**

5. **🌳 Sensor de queimada na floresta**
   - Local remoto na Amazônia
   - **Deep sleep não é luxo — é viabilidade**

### 15-25 min: Os 3 Modos de Sleep

| Modo | Consumo | Acorda com |
|------|---------|------------|
| Modem Sleep | ~15mA | Timer automático |
| Light Sleep | ~0.4mA | Timer ou GPIO |
| **Deep Sleep** | **~20µA** | **RST (GPIO 16 ou externo)** |

> **Deep Sleep:** tudo desligado (CPU, Wi-Fi, RAM). Só o RTC continua. Quando acorda, `setup()` roda do zero.

### 25-35 min: Como o ESP8266 Acorda

**3 formas de acordar:**

| Forma | Como | Quando usar |
|-------|------|-------------|
| **Timer** | `ESP.deepSleep(10e6)` → D0→RST pulsa | Acordar a cada X minutos |
| **Botão** | Pressionar RST-GND | Wake manual |
| **Transistor** | KSP2222A + LDR puxam RST LOW | Sensor de luz, PIR, etc |

**⏱️ Limite:** deep sleep máximo = ~71 minutos (2³² µs)

> Para projetos mais longos: ciclos de deep sleep + contador persistente

### 35-42 min: Demonstração ao Vivo — "Pisca-Dorme"

```cpp
#define LED_PIN 2

void setup() {
  Serial.begin(115200);
  pinMode(LED_PIN, OUTPUT);
  Serial.println("Acordei!");

  // Feedback visual: pisca 3x
  for (int i = 0; i < 3; i++) {
    digitalWrite(LED_PIN, LOW);
    delay(200);
    digitalWrite(LED_PIN, HIGH);
    delay(200);
  }

  Serial.println("Dormindo 10 segundos...");
  ESP.deepSleep(10e6); // 10 segundos (em microssegundos!)
}

void loop() {
  // NUNCA executa após deep sleep — o ESP reinicia!
}
```

**Testar:**
1. Carregar código → LED pisca → Serial Monitor mostra "Acordei" → "Dormindo"
2. Após 10 segundos → ESP acorda sozinho? (Se não: verificar fio D0→RST!)
3. Ciclo repete infinitamente

### 42-45 min: Exercício — Calculadora de Autonomia

| Cenário | Consumo contínuo | Com Sleep (5s acordado / 30min) | Ganho |
|---------|------------------|--------------------------------|-------|
| Pilha AA (2500mAh) | 31 horas | **~517 dias** | 400x |

> "Com 5 segundos de trabalho a cada 30 minutos, uma pilha AA dura **mais de 1 ano!**"

---

## AULA 2: Hands-on 1 (GUIADO) — "Pisca → Sleep → Botão" (45 min)

### Objetivo: Entender o ciclo completo com wake manual por botão

### 0-5 min: Revisão Rápida
1. "O que acontece quando `ESP.deepSleep()` é chamado?" → Reinicia do zero
2. "Qual pino acorda o ESP?" → RST
3. "Quanto consome em deep sleep?" → ~20µA
4. "Por que D0→RST?" → GPIO16 é o pino do RTC que envia o pulso de wake

### 5-10 min: Circuito do Botão de Wake

```
┌─────────────────────────────────────┐
│         NodeMCU ESP8266             │
│                                     │
│   3.3V ─── 10kΩ ──── RST           │
│                            │        │
│                      Botão push     │
│                            │        │
│                           GND       │
│                                     │
│   D0 (GPIO16) ──────── RST         │  ← OBRIGATÓRIO para timer wake
│                                     │
└─────────────────────────────────────┘
```

> ⚠️ **Sem pull-up de 10kΩ**, o RST pode dar resets aleatórios! O resistor mantém o RST em HIGH quando o botão não está pressionado.

### 10-40 min: Montagem e Código (guiado passo a passo)

**Código 2.1 — Pisca + Sleep + Botão (completo, entregar pronto):**

```cpp
/*
 * Código 2.1: Pisca-Dorme-Botão
 * Demonstrates deep sleep + manual wake via button
 *
 * Hardware:
 * - NodeMCU ESP8266
 * - LED onboard (GPIO 2, ativo em LOW)
 * - Fio D0 → RST (OBRIGATÓRIO!)
 * - Botão push entre RST e GND
 * - Resistor 10kΩ entre 3.3V e RST (pull-up)
 */

#define LED_PIN 2

void setup() {
  Serial.begin(115200);
  pinMode(LED_PIN, OUTPUT);

  Serial.println("\n=== ACORDEI ===");
  Serial.printf("Ciclo #%d\n", ESP.getCycleCount());

  // Feedback visual: pisca 3 vezes
  for (int i = 0; i < 3; i++) {
    digitalWrite(LED_PIN, LOW);
    delay(200);
    digitalWrite(LED_PIN, HIGH);
    delay(200);
  }

  Serial.println("Trabalho feito. Dormindo 30s...");
  Serial.println("Use o botão (RST-GND) para acordar antes, se quiser.");
  ESP.deepSleep(30e6); // 30 segundos
}

void loop() {
  // NUNCA executa!
}
```

**Fiação passo a passo (professor demonstra):**
1. Conectar fio D0 → RST (esse é o fio do timer!)
2. Conectar resistor 10kΩ entre 3.3V e RST
3. Conectar botão entre RST e GND
4. Conectar LED (opcional, para feedback visual)

**Testes:**
1. Carregar código → LED pisca 3x → ESP entra em deep sleep
2. Esperar 30 segundos → ESP acorda sozinho? ✓
3. Pressionar botão (RST-GND) antes dos 30s → acorda imediatamente? ✓
4. Contador no Serial Monitor incrementa a cada ciclo

### 40-45 min: Desafio Extra — "Contador de Boots"

Modificar o código para contar e exibir o número de resets ao acordar:

```cpp
// Adicionar variável global (PERSISTE EM RTC memory se configurado, senão reinicia todo ciclo)
int contador = 0;

// No setup():
contador++;
Serial.printf("Boot #%d\n", contador);
```

> **Pergunta:** "Se eu tirar o cabo USB e plugar de novo, o contador volta a 0? Por quê?"

---

## AULA 3: Hands-on 2 (BASE A AJUSTAR) — "LittleFS + NTP + RTC Memory" (45 min)

### Objetivo: Implementar persistência de dados — dois métodos

### 0-5 min: Revisão — "O Problema"

> "Deep sleep reinicia tudo. Variáveis normais são perdidas."
> "Como lembrar quantos ciclos já rodaram? Como saber que horas são sem conectar Wi-Fi toda vez?"

### 5-10 min: Duas Soluções para ESP8266

| Método | Persiste Reset? | Persiste Power-off? | Complexidade |
|--------|:---:|:---:|:---:|
| **ESP.rtcUserMemoryWrite/Read** | ✅ Sim | ❌ Não | Baixa (~512 bytes) |
| **LittleFS + ArduinoJson** | ✅ Sim | ✅ Sim | Média |

> ⚠️ **RTC_DATA_ATTR** no ESP8266 NÃO funciona bem — não persite em power-off!
> Para o ESP32 funciona, mas aqui no ESP8266 use **LittleFS** ou **rtcUserMemory**.

### 10-15 min: Código Base — RTC Memory (entregar pronto)

```cpp
/*
 * Código 3.1: RTC Memory — contador persistente
 *
 * 512 bytes que sobrevivem ao reset (mas NÃO a power-off!)
 * Útil para: contadores, flags, pequenas estruturas
 */

struct State {
  uint32_t ciclos;
  uint32_t checksum;
};

uint32_t calcChecksum(State s) {
  return s.ciclos ^ 0xDEADBEEF;
}

void setup() {
  State state;

  // Tenta ler estado anterior da RTC memory
  ESP.rtcUserMemoryRead(0, &state, sizeof(state));

  // Verifica se dados são válidos (checksum)
  if (state.checksum != calcChecksum(state)) {
    // Primeira vez ou dados corrompidos
    state.ciclos = 0;
  }

  state.ciclos++;
  state.checksum = calcChecksum(state);

  // Salva novo estado
  ESP.rtcUserMemoryWrite(0, &state, sizeof(state));

  Serial.begin(115200);
  Serial.printf("Ciclo #: %d\n", state.ciclos);

  ESP.deepSleep(10e6);
}

void loop() {}
```

**Teste:**
1. Reset manual (botão RST) → contador incrementa? ✅
2. Desligar USB e ligar de novo → contador volta a 0? ✅ (power-off apaga RTC memory!)

### 15-35 min: Desafio — LittleFS + NTP Inteligente (BASE A AJUSTAR)

**给了骨架代码，学生需要完成的部分用 `TODO` 标注：**

```cpp
/*
 * Código 3.2: LittleFS + NTP Inteligente
 *
 * OBJETIVO: Salvar leituras de sensor + hora correta
 * - LittleFS para persistir em flash (sobrevive a power-off!)
 * - NTP inteligente: conecta UMA vez, calcula depois localmente
 *
 * ALUNOS PRECISAM COMPLETAR:
 * 1. função horaAtual() — cálculo de hora local
 * 2. função formatarHora() — formatação dd/mm HH:MM:SS
 * 3. lógica de sincronização NTP — só na primeira vez
 * 4. salvar/carregar estado com ArduinoJson
 */

#include <ESP8266WiFi.h>
#include <LittleFS.h>
#include <ArduinoJson.h>
#include <NTPClient.h>
#include <WiFiUdp.h>

#define LED_PIN 2
#define ARQUIVO_ESTADO "/estado.json"
#define ARQUIVO_LEITURAS "/leituras.json"

const char* ssid = "SUA_REDE_WIFI";
const char* senha = "SUA_SENHA_WIFI";

WiFiUDP ntpUDP;
NTPClient timeClient(ntpUDP, "pool.ntp.org", -10800, 60000); // GMT-3

struct Estado {
  bool ntpOk = false;
  time_t epochBase = 0;
  unsigned long millisBase = 0;
  int ciclos = 0;
};

Estado estado;

// ===== TODO 1: Completar função =====
// Calcula hora local baseada em epochBase + millis transcurrido
time_t horaAtual() {
  if (!estado.ntpOk) return 0;
  // Dica: epochBase + (millis() - millisBase) / 1000
}

// ===== TODO 2: Completar função =====
// Formata time_t como "dd/mm HH:MM:SS"
String formatarHora(time_t t) {
  if (t == 0) return "---";
  // Dica: usar localtime() + strftime()
}

// ===== TODO 3: Completar lógica de NTP =====
bool sincronizarNTP() {
  // Passos:
  // 1. WiFi.begin(ssid, senha)
  // 2. Aguarda conexão
  // 3. timeClient.begin() + timeClient.update()
  // 4. Salvar epochBase = timeClient.getEpochTime()
  // 5. Salvar millisBase = millis()
  // 6. WiFi.disconnect(true) + WiFi.mode(WIFI_OFF) // ECONOMIA!
}

// ===== TODO 4: LittleFS persistência =====
// Funções carregarEstado() e salvarEstado() usando ArduinoJson

void setup() {
  Serial.begin(115200);
  pinMode(LED_PIN, OUTPUT);

  // Inicializar LittleFS
  if (!LittleFS.begin()) {
    Serial.println("❌ LittleFS falhou!");
    return;
  }

  // TODO: Carregar estado salvo (se existir)
  // Dica: verificar se ARQUIVO_ESTADO existe, usar StaticJsonDocument

  estado.ciclos++;

  // TODO: Se ntpOk==false, chamar sincronizarNTP()

  // Mostrar info
  Serial.printf("Ciclo #: %d\n", estado.ciclos);
  if (estado.ntpOk) {
    Serial.printf("Hora: %s\n", formatarHora(horaAtual()).c_str());
  }

  // TODO: Salvar estado antes de dormir

  // Pisca LED
  digitalWrite(LED_PIN, LOW);
  delay(500);
  digitalWrite(LED_PIN, HIGH);

  ESP.deepSleep(30e6);
}

void loop() {}
```

**Avaliar:**
- `horaAtual()` calcula corretamente?
- `formatarHora()` formata como "dd/mm HH:MM:SS"?
- NTP sincroniza na primeira vez e calcula localmente depois?
- LittleFS persiste entre resets e power-off?

### 35-45 min: Teste e Discussão

| Teste | RTC Memory | LittleFS |
|-------|:---:|:---:|
| Reset manual → contador incrementou? | ✅ | ✅ |
| Desligar USB → ligar → contador保留了? | ❌ | ✅ |
| Dados de hora persistiram? | ❌ | ✅ |

---

## AULA 4: PROJETO — "Contador de Flashes via MQTT" (45 min)

### 0-5 min: Briefing

**O que o projeto faz:**
1. Conectar ao broker MQTT **test.mosquitto.org:1883**
2. Inscrever-se no tópico `ifsp-capivari/ciclos/[nome-da-dupla]`
3. Receber último valor salvo (persistido pelo broker)
4. Incrementar e publicar o novo valor
5. Entrar em deep sleep

**Hardware:** Só ESP8266 + cabo USB (sem sensores, sem componentes extras!)

### 5-10 min: Explicação do MQTT

- **Broker público:** `test.mosquitto.org:1883` (Mosquitto test server)
- **Tópico:** `ifsp-capivari/ciclos/NOME_DA_DUPLA` (cada dupla usa nome único)
- **QoS 1:** "At least once" — garante que a mensagem chega, mas pode duplicar
- **Fluxo:**
  ```
  ESP conecta → broker envia último valor → ESP incrementa → ESP publica → ESP dorme
  ```

### 10-15 min: Código Base (entregar pronto com gap para nome)

```cpp
/*
 * Código 4: Contador de Flashes via MQTT
 *
 * Usa AsyncMQTTClient (marvinroger/async-mqtt-client)
 * Broker: test.mosquitto.org:1883
 *
 * OBJETIVO: Demonstrar comunicação MQTT + persistência + deep sleep
 *
 * ALUNOS AJUSTAM:
 * - Nome no tópico MQTT (uma dupla = um nome único)
 * - ssid/senha do WiFi
 */

#include <ESP8266WiFi.h>
#include <AsyncMQTTClient.h>

const char* ssid = "SUA_REDE_WIFI";
const char* senha = "SUA_SENHA_WIFI";

const char* mqtt_host = "test.mosquitto.org";
const uint16_t mqtt_port = 1883;
const char* mqtt_topic = "ifsp-capivari/ciclos/SEU_NOME_AQUI"; // ← MUDAR!

int contador = 0;
bool valorRecebido = false;

void onMessage(char* topic, char* payload, AsyncMQTTClientMessageProperties properties, size_t len, size_t index, size_t total) {
  // Callback quando chega mensagem MQTT
  if (len > 0) {
    payload[len] = '\0'; // null-terminate
    contador = atoi(payload);
    valorRecebido = true;
    Serial.printf("📥 Recebido do broker: %d\n", contador);
  }
}

void onConnect(bool sessionPresent) {
  Serial.println("✅ MQTT conectado!");
  // Inscreve no tópico para receber último valor
  AsyncMQTTClient.subscribe(mqtt_topic, 1); // QoS 1
}

void setup() {
  Serial.begin(115200);
  Serial.println("\n=== Contador MQTT ===");

  // Conectar Wi-Fi
  WiFi.begin(ssid, senha);
  while (WiFi.status() != WL_CONNECTED) {
    delay(100);
    Serial.print(".");
  }
  Serial.println("\n✅ Wi-Fi conectado!");

  // Configurar MQTT
  AsyncMQTTClient.onConnect(onConnect);
  AsyncMQTTClient.onMessage(onMessage);

  AsyncMQTTClient.begin(mqtt_host, mqtt_port);

  // Aguarda receber valor (max 5 segundos)
  unsigned long start = millis();
  while (!valorRecebido && millis() - start < 5000) {
    delay(10);
  }

  contador++;
  char msg[16];
  snprintf(msg, sizeof(msg), "%d", contador);
  Serial.printf("📤 Enviando: %s\n", msg);
  AsyncMQTTClient.publish(mqtt_topic, 1, false, msg);

  delay(500);
  Serial.println("💤 Dormindo 60s...");
  ESP.deepSleep(60e6);
}

void loop() {}
```

### 15-40 min: Implementação em Duplas

**Checklist:**
- [ ] Ajustar nome no tópico MQTT (cada dupla = nome único!)
- [ ] Ajustar ssid/senha do WiFi
- [ ] Carregar código
- [ ] Observar Serial Monitor: conecta → recebe → incrementa → publica → dorme
- [ ] Verificar se contador incrementa a cada ciclo

**Testar persistência MQTT:**
1. Dupla A: observa o contador subir
2. Dupla B: quandoogar, observa se recebe o último valor de A
3. Desligar USB e ligar de novo: o contador do broker foi mantido?

**Verificação (opcional, se houver tempo):**
- MQTT Explorer no celular/computador: `http://test.mosquitto.org:1880`
- Ou comando `mosquitto_sub`:
  ```bash
  mosquitto_sub -h test.mosquitto.org -t "ifsp-capivari/ciclos/#" -v
  ```

### 40-45 min: Apresentações Rápidas

Cada dupla mostra:
1. Serial Monitor com contador incrementando
2. Explain: conecta → recebe → incrementa → publica → dorme

---

## 📦 Materiais por Dupla

### Aula 2
- NodeMCU ESP8266 + cabo micro USB
- Protoboard + jumpers
- Botão push (ou usar botão FLASH do NodeMCU — GPIO0)
- Resistor 10kΩ (pull-up para RST)
- Fio D0 → RST (OBRIGATÓRIO!)

### Aula 3
- Tudo da Aula 2
- + LittleFS.begin() já configurado no código base

### Aula 4
- NodeMCU ESP8266 + cabo micro USB
- Rede WiFi do laboratório
- Acesso ao broker `test.mosquitto.org:1883`

---

## 🎯 Rúbrica de Avaliação

| Critério | Peso | Descrição |
|----------|------|-----------|
| Deep Sleep funcionando | 20% | Acorda e dorme corretamente |
| Wake por botão | 15% | Botão funciona para acordar manualmente |
| RTC Memory | 20% | Contador persiste entre resets |
| LittleFS Persistência | 20% | Dados persistem entre power-off |
| NTP Inteligente | 15% | Sincroniza 1x, calcula depois sem Wi-Fi |
| MQTT (Aula 4) | 10% | Contador funciona via MQTT |

---

## 🔌 Pinagem de Referência

### Wake por Botão
```
3.3V ─── 10kΩ ──── RST
                  │
             Botão push
                  │
                 GND

D0 (GPIO16) ────── RST    ← OBRIGATÓRIO para timer wake
```

### Wake por Transistor (LDR + KSP2222A)
```
3.3V ─── LDR ──────┬─────── Base do KSP2222A (via resistor 10kΩ)
                   │
              Trimpot
                   │
                  GND

Coletor (C) ──────── RST
Emissor (E) ─────── GND
```

### KSP2222A Pinout (vista de frente)
```
      ┌──────────────┐
      │  B    C      │
      │  │    │      │
      └──│────│──────┘
         │    │
         E    └──→ RST
         │
         └──→ GND
```

---

*Criado em: 22/04/2026*
*Versão seguindo Roteiro_resumido.md — sequência: contexto → exemplos → solução → 2 hands-on*
