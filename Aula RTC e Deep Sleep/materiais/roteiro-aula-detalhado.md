# 📋 ROTEIRO DETALHADO DA AULA
## "RTC, Deep Sleep e Autonomia no ESP8266"

### 📍 CONTEXTO
- **Módulo:** Programação Avançada em IoT
- **Aula:** 2 do módulo (continuação de Timing/NTP)
- **Duração:** 4 aulas de 45 minutos (180 min total)
- **Pré-requisitos:** millis(), Ticker, NTP (aula anterior)

---

## 🎯 OBJETIVOS DE APRENDIZAGEM

Ao final da aula, o aluno será capaz de:
1. Explicar **por que** economia de energia é crítica em IoT
2. Implementar **Deep Sleep** no ESP8266 com despertar por timer
3. Manter a **hora correta** sem internet (RTC por software)
4. Calcular a **autonomia** de um projeto com baterias
5. Projetar um sistema IoT que opera por **meses** com bateria

---

## ⏰ CRONOGRAMA MINUTO A MINUTO

---

### AULA 1: "POR QUE DORMIR?" (45 min)
*Aulão de engajamento — o objetivo é que os alunos sintam o problema na pele*

#### 0-5 min: ABERTURA — "O Desafio da Bateria" 🔋

**Ação:** Professor mostra uma pilha AA e um NodeMCU ligado com LED piscando.

**Fala sugerida:**
> "Quanto tempo esse ESP8266 com LED piscando dura com essa pilha AA? Chutem."

Deixe os alunos tentarem. Anote os palpites na lousa.

**Resposta:** ~12 horas. Agora pergunte:
> "E se eu precisasse que ele ficasse na fazenda do meu tio monitorando a temperatura do galinheiro por 6 meses? Sem tomada, sem solar. O que a gente faz?"

**Gancho:** "Hoje vocês vão aprender a fazer um ESP8266 durar **meses** com uma pilha."

#### 5-20 min: EXEMPLOS DO MUNDO REAL — "Quem dorme, vive mais" 🌍

**Apresentar 8 exemplos reais** (projetar no slide ou contar como história):

1. **🏠 Estação meteorológica na fazenda**
   - Mede temperatura/umidade a cada 30 minutos
   - Envia via Wi-Fi para um dashboard
   - Local sem energia elétrica → painel solar + bateria
   - **Sem deep sleep:** 1 dia de bateria. **Com deep sleep:** 8 meses

2. **🌾 Irrigação inteligente no campo**
   - Sensor de umidade do solo no plantio
   - Acorda, mede, decide se irriga, volta a dormir
   - Cada ciclo: 5 segundos acordado, 1 hora dormindo
   - **Consumo:** de 80mA para 20μA (4.000x menos!)

3. **🚨 Sensor de intrusão em galpão**
   - Acelerômetro detecta vibração na porta
   - Acorda por interrupt (não por timer)
   - Manda alerta Telegram e volta a dormir
   - **Autonomia:** 1 ano com bateria 18650

4. **🐝 Monitoramento de colmeias**
   - Peso + temperatura + som da colmeia
   - Apiário no meio do mato, sem Wi-Fi → LoRa + ESP8266
   - Acorda a cada hora, transmite, dorme
   - Projeto real da Embrapa

5. **🗑️ Lixeira inteligente da cidade**
   - Ultrassom mede nível de enchimento
   - Acorda 4x ao dia, envia para a prefeitura
   - Roteiriza a coleta de lixo (economia de diesel)
   - Projeto real em várias cidades brasileiras

6. **🐟 Tanque de peixes (aquicultura)**
   - Monitora pH, oxigênio e temperatura
   - Se oxigênio baixo → aciona aerador
   - Acorda a cada 15 minutos, verifica, dorme
   - **Sem deep sleep:** bateria dura 2 dias

7. **🅿️ Vaga de estacionamento inteligente**
   - Sensor magnético detecta carro na vaga
   - Acorda quando o campo magnético muda
   - Dura 3 anos com 2 pilhas AA
   - Usado em shopping centers

8. **🌳 Sensor de queimada na floresta**
   - Gás + temperatura + umidade
   - Local remoto na Amazônia, satélite ou LoRa
   - Acorda a cada 2 horas, transmite, dorme
   - **Crítico:** não pode trocar bateria todo mês

**Pergunta de reflexão para a turma:**
> "Qual desses projetos vocês acham que seria mais legal implementar aqui no IFSP ou na cidade de Capivari?"

#### 20-35 min: TEORIA — Como o ESP8266 dorme 💤

**Slide/Quadro: Os 3 modos de sleep do ESP8266**

| Modo | Consumo | Acordar com | Uso típico |
|------|---------|-------------|------------|
| **Modem Sleep** | ~15mA | Timer automático | Wi-Fi desligado entre transmissões |
| **Light Sleep** | ~0.4mA | Timer ou GPIO | CPU pausada, RAM mantida |
| **Deep Sleep** | ~20μA (0.02mA) | Apenas GPIO 16 (RST) | Tudo desligado, só RTC funciona |

**Analogia para explicar:**
> "Deep Sleep é como o celular desligado — nada roda, mas o despertador (RTC) continua contando. Quando chega a hora, ele te acorda. A diferença é que o ESP8266 'acorda' do zero, como se ligasse do botão."

**Ponto crucial — o pino RST:**
- GPIO 16 deve ser conectado ao RST
- É isso que "cutuca" o ESP8266 para acordar
- **Sem esse fio, o ESP8266 dorme para sempre** (até reset manual)
- Mostrar no protoboard a conexão

**Demonstração ao vivo:**
```cpp
#include <ESP8266WiFi.h>

void setup() {
  Serial.begin(115200);
  Serial.println("Acordei! Vou trabalhar...");
  delay(2000); // simula "trabalho"
  Serial.println("Terminou. Indo dormir por 10 segundos...");
  ESP.deepSleep(10e6); // 10 segundos em microssegundos
}

void loop() {
  // NUNCA chega aqui após deep sleep!
  // O ESP8266 reinicia do zero
}
```

**Demonstrar:** o ESP8266 acorda, imprime, dorme, acorda de novo... ciclo infinito.

**Pergunta-chave:**
> "Se o ESP reinicia do zero, como ele lembra que hora são? Que dados já leu?"

→ Resposta: **RTC memory** (próxima aula)

#### 35-45 min: EXERCÍCIO RÁPIDO — "Calculadora de Autonomia"

**Distribuir folha ou projetar:**

Dado:
- Bateria 18650: 3000 mAh
- ESP8266 acordado (com Wi-Fi): 80 mA
- ESP8266 em deep sleep: 0.02 mA
- Ciclo: acorda a cada 30 min, fica 5 seg acordado

Perguntas:
1. Quantos ciclos por dia? (48 ciclos)
2. Tempo acordado por dia? (48 × 5s = 240s = 4 min)
3. Carga consumida acordado/dia? (80mA × 4/60h = 5.3 mAh)
4. Carga consumida dormindo/dia? (0.02mA × 23.93h = 0.48 mAh)
5. **Total por dia?** (~5.8 mAh)
6. **Autonomia?** (3000 / 5.8 ≈ **517 dias!**)

**Momento "mind blow":**
> "Sem deep sleep seriam 3000/80 = 37 horas. Com deep sleep: **517 dias**. É 330x mais!"

---

### AULA 2: MÃO NA MASSA — IMPLEMENTANDO DEEP SLEEP (45 min)

#### 0-5 min: RECAPITULAÇÃO RÁPIDA
- 3 perguntas orais sobre a aula anterior:
  1. "Qual o consumo do deep sleep?" (~20μA)
  2. "Qual pino precisa ser conectado ao RST?" (GPIO 16 / D0)
  3. "O que acontece com o código ao acordar?" (Reinicia do zero, roda setup() novamente)

#### 5-15 min: HANDS-ON 1 — "Pisca-Dorme" 💡

**Objetivo:** Fazer o LED piscar 3 vezes, dormir 10 segundos, repetir.

```cpp
#define LED_PIN 2  // LED onboard do NodeMCU (ativo em LOW)

void setup() {
  Serial.begin(115200);
  delay(100);
  
  Serial.println("\n=== Acordei! ===");
  
  // Pisca LED 3 vezes
  for (int i = 0; i < 3; i++) {
    digitalWrite(LED_PIN, LOW);   // liga
    delay(200);
    digitalWrite(LED_PIN, HIGH);  // desliga
    delay(200);
  }
  
  Serial.println("Trabalho feito. Dormindo 10s...");
  ESP.deepSleep(10e6);  // 10 segundos
}

void loop() {
  // Nunca executa!
}
```

**Desafio rápido:** Mudar para piscar 5 vezes e dormir 30 segundos.

**⚠️ Problema comum:** Se o ESP dorme e não acorda → falta o fio D0→RST!

#### 15-30 min: HANDS-ON 2 — "Sensor que Dorme" 🌡️

**Objetivo:** Ler temperatura do DHT11, enviar via Serial, dormir 30 segundos.

```cpp
#include <ESP8266WiFi.h>
#include <DHT.h>

#define DHT_PIN D4
#define DHT_TYPE DHT11

DHT dht(DHT_PIN, DHT_TYPE);

void setup() {
  Serial.begin(115200);
  delay(100);
  
  dht.begin();
  
  Serial.println("\n=== Leitura do Sensor ===");
  
  float temp = dht.readTemperature();
  float umid = dht.readHumidity();
  
  if (isnan(temp) || isnan(umid)) {
    Serial.println("ERRO: Falha ao ler o DHT11!");
  } else {
    Serial.printf("Temperatura: %.1f°C\n", temp);
    Serial.printf("Umidade: %.1f%%\n", umid);
    
    // Aqui entraria o envio via MQTT/HTTP
    // Por enquanto só imprimimos
  }
  
  Serial.println("Dormindo 30s...");
  ESP.deepSleep(30e6);
}

void loop() {}
```

**Extensão para adiantados:** Adicionar Wi-Fi + enviar para ThingSpeak.

#### 30-40 min: HANDS-ON 3 — "Acordar por Botão" 🔘

**Objetivo:** Acordar o ESP8266 por interrupt externo (botão), não por timer.

**Conceito:** Deep sleep pode acordar por:
- Timer: `ESP.deepSleep(tempo)` 
- External: pino RST puxado para LOW (botão, sensor, outro ESP)

```cpp
void setup() {
  Serial.begin(115200);
  delay(100);
  
  Serial.println("\n=== Acordei por botão! ===");
  Serial.println("Quem me acordou? Foi você apertando o botão.");
  Serial.println("Fazendo trabalho rápido...");
  
  digitalWrite(2, LOW);  // Liga LED
  delay(3000);           // Fica ligado 3 segundos
  digitalWrite(2, HIGH); // Desliga LED
  
  Serial.println("Voltando a dormir. Aperte o botão de novo!");
  
  // Deep sleep "infinito" — só acorda por RST (botão)
  ESP.deepSleep(0);
}

void loop() {}
```

**Circuito:** Botão entre RST e GND (sem resistor, o pull-up interno do NodeMCU resolve).

**Aplicação real:** Sensor de porta de galpão — quando a porta abre (imã se afasta do reed switch), RST vai LOW → ESP acorda → manda alerta.

#### 40-45 min: DISCUSSÃO — "Quanto tempo a gente ganha?"

Projetar na lousa:

| Cenário | Sem Sleep | Com Sleep | Ganho |
|---------|-----------|-----------|-------|
| LED piscando (contínuo) | 15h | - | — |
| Leitura a cada 1 min (5s acordado) | 15h | 35 dias | 56x |
| Leitura a cada 10 min (5s acordado) | 15h | 280 dias | 448x |
| Leitura a cada 1 hora (5s acordado) | 15h | 517 dias | 827x |

**Reflexão final da aula 2:**
> "Notem que o segredo não é só dormir — é dormir **bem**. Acordar por pouco tempo é tão importante quanto dormir muito."

---

### AULA 3: RTC MEMORY + NTP INTELIGENTE (45 min)

#### 0-5 min: O PROBLEMA — "Esqueci que horas são!" 🕐

**Demonstração do problema:**
- Rodar o código do DHT com deep sleep
- Mostrar no Serial que o ESP perdeu a hora ao acordar
- "Se ele reinicia do zero, como sabemos QUANDO a leitura foi feita?"

**A analogia:**
> "É como se você fosse dormir com amnésia — acorda sem saber que dia é. Precisa de um 'post-it na geladeira' para lembrar."

#### 5-15 min: TEORIA — RTC Memory do ESP8266

**Conceito:**
- O ESP8266 tem **RTC memory** (512 bytes)
- Sobrevive ao deep sleep (mas NÃO ao power-off/desconexão)
- Funciona como um "post-it" — guarda dados entre ciclos de sono

```cpp
// Declarando variável na RTC memory
RTC_DATA_ATTR int contador = 0;  // Sobrevive ao deep sleep!
RTC_DATA_ATTR time_t ultimaSincronizacao = 0;
```

**Comparação:**

| Tipo de Memória | Sobrevive ao Deep Sleep? | Sobrevive ao Power-off? |
|-----------------|--------------------------|-------------------------|
| Variável normal (RAM) | ❌ Perde | ❌ Perde |
| `RTC_DATA_ATTR` | ✅ Mantém | ❌ Perde |
| EEPROM / Flash | ✅ Mantém | ✅ Mantém |
| SPIFFS / LittleFS | ✅ Mantém | ✅ Mantém |

**Quando usar cada uma:**
- RTC memory: contadores, timestamps, estados simples (rápido, limitado a 512B)
- EEPROM: configurações calibradas, pequenos dados persistentes
- SPIFFS: arquivos, logs, páginas HTML (lento, usa flash)

#### 15-30 min: HANDS-ON 4 — "Relógio que Não Esquece" ⏰

**Objetivo:** Sincronizar hora via NTP uma vez, manter correta via RTC memory.

```cpp
#include <ESP8266WiFi.h>
#include <WiFiUdp.h>
#include <NtpClientLib.h>

RTC_DATA_ATTR bool horaSincronizada = false;
RTC_DATA_ATTR unsigned long ultimoNTP = 0;
RTC_DATA_ATTR time_t epochSincronizado = 0;
RTC_DATA_ATTR unsigned long millisSincronizado = 0;
RTC_DATA_ATTR int ciclos = 0;

const char* ssid = "NOME_DA_REDE";
const char* senha = "SENHA_DA_REDE";

void setup() {
  Serial.begin(115200);
  delay(100);
  
  ciclos++;
  Serial.printf("\n=== Ciclo #%d ===\n", ciclos);
  
  if (!horaSincronizada) {
    // Primeira vez ou perdeu RTC — conectar e sincronizar
    Serial.println("Primeira vez! Conectando WiFi...");
    WiFi.begin(ssid, senha);
    
    int tentativas = 0;
    while (WiFi.status() != WL_CONNECTED && tentativas < 20) {
      delay(500);
      Serial.print(".");
      tentativas++;
    }
    
    if (WiFi.status() == WL_CONNECTED) {
      Serial.println("\nWiFi conectado!");
      
      NTP.begin("pool.ntp.org", -3);  // GMT-3 Brasil
      NTP.waitSet();
      
      epochSincronizado = time(nullptr);
      millisSincronizado = millis();
      horaSincronizada = true;
      
      Serial.printf("NTP sincronizado: %s", ctime(&epochSincronizado));
      
      // Desliga Wi-Fi para economizar
      WiFi.disconnect(true);
      WiFi.mode(WIFI_OFF);
    }
  }
  
  // Calcular hora atual
  if (horaSincronizada) {
    time_t agora = epochSincronizado + (millis() - millisSincronizado) / 1000;
    Serial.printf("Hora atual (sem WiFi): %s", ctime(&agora));
  }
  
  // Se passou muito tempo sem sincronizar (ex: drift), marcar para re-sincronizar
  // Deep sleep por 5 minutos
  Serial.println("Dormindo 5 minutos...");
  ESP.deepSleep(300e6);  // 5 min
}

void loop() {}
```

**Discussão:**
> "Notem: conectamos ao Wi-Fi só na PRIMEIRA vez. Depois, calculamos a hora matematicamente. Isso economiza o tempo (e energia) da conexão Wi-Fi em cada ciclo!"

#### 30-40 min: HANDS-ON 5 — "Logger com Timestamp" 📊

**Objetivo:** Ler sensor DHT11 e registrar com hora correta, usando RTC memory.

```cpp
#include <ESP8266WiFi.h>
#include <DHT.h>
#include <time.h>

#define DHT_PIN D4
DHT dht(DHT_PIN, DHT11);

RTC_DATA_ATTR bool ntpOk = false;
RTC_DATA_ATTR time_t epochBase = 0;
RTC_DATA_ATTR unsigned long millisBase = 0;
RTC_DATA_ATTR int leituras = 0;

const char* ssid = "NOME_DA_REDE";
const char* senha = "SENHA_DA_REDE";

void sincronizarNTP() {
  // ... (mesmo código anterior de sincronização)
}

time_t horaAtual() {
  return epochBase + (millis() - millisBase) / 1000;
}

void setup() {
  Serial.begin(115200);
  delay(100);
  dht.begin();
  
  leituras++;
  
  // Sincroniza NTP se necessário (só na primeira vez)
  if (!ntpOk) {
    sincronizarNTP();  // função definida acima
  }
  
  // Lê sensor
  float temp = dht.readTemperature();
  float umid = dht.readHumidity();
  
  // Timestamp
  time_t agora = horaAtual();
  struct tm* t = localtime(&agora);
  char timestamp[20];
  strftime(timestamp, sizeof(timestamp), "%d/%m/%Y %H:%M:%S", t);
  
  Serial.printf("[%s] Leitura #%d: %.1f°C, %.1f%%\n", 
                timestamp, leituras, temp, umid);
  
  // Aqui enviaria via MQTT/HTTP...
  
  Serial.println("Dormindo 1 minuto...");
  ESP.deepSleep(60e6);
}

void loop() {}
```

#### 40-45 min: DESAFIO — "Acumulador de Leituras"

**Desafio para os rápidos:**
Guardar as últimas 10 leituras (temp + timestamp) na RTC memory e imprimir todas quando completar.

**Dica:** Usar um struct na RTC memory:
```cpp
struct Leitura {
  time_t timestamp;
  float temperatura;
  float umidade;
};

RTC_DATA_ATTR Leitura historico[10];
RTC_DATA_ATTR int posHistorico = 0;
```

---

### AULA 4: PROJETO INTEGRADOR — "Estação Autônoma" 🚀 (45 min)

#### 0-5 min: BRIEFING DO PROJETO

**O projeto:** Estação de monitoramento autônoma que:
1. Acorda a cada 5 minutos
2. Lê temperatura e umidade (DHT11)
3. Registra o timestamp de cada leitura
4. Sincroniza NTP apenas na primeira vez (ou a cada 100 leituras)
5. Mostra tudo no Serial com timestamps corretos
6. Entra em deep sleep
7. **Desafio extra:** Enviar dados via MQTT quando acordar

#### 5-35 min: IMPLEMENTAÇÃO EM DUPLAS

**Checklist do projeto:**

- [ ] Conexão D0 → RST para deep sleep funcionar
- [ ] LED pisca ao acordar (feedback visual)
- [ ] DHT11 lendo corretamente
- [ ] NTP sincroniza na primeira vez
- [ ] Hora mantida corretamente entre ciclos (RTC memory)
- [ ] Leituras com timestamp formatado no Serial
- [ ] Deep sleep configurado para 5 minutos
- [ ] Contador de ciclos funciona (não reseta)
- [ ] Wi-Fi desligado após uso (economia)
- [ ] Código limpo e comentado

**Desafio extra (para quem terminar cedo):**
- [ ] Enviar dados via MQTT para broker local
- [ ] Guardar histórico de 10 leituras na RTC memory
- [ ] Re-sincronizar NTP a cada 100 ciclos (corrigir drift)
- [ ] Calcular autonomia estimada da bateria

#### 35-40 min: APRESENTAÇÕES RÁPIDAS (2 min por dupla)
- Mostrar o Serial Monitor com os ciclos
- Explicar uma dificuldade que tiveram
- Compartilhar algo que descobriram

#### 40-45 min: ENCERRAMENTO + GANCHO PARA PRÓXIMA AULA

**Resumo do que aprenderam:**
1. Deep Sleep reduz consumo em ~4000x
2. RTC memory guarda dados entre ciclos de sono
3. NTP só precisa uma vez — depois calcula localmente
4. A conexão D0→RST é essencial
5. Autonomia depende de: tempo acordado × intervalo de sono

**Gancho para a próxima aula:**
> "Hoje nosso sensor dorme sozinho. Mas e se ele precisasse tomar DECISÕES ao acordar? Tipo: 'se a temperatura passou de 30°C, liga o cooler; se não, volta a dormir'. Isso é uma **Máquina de Estados** — e é o tema da próxima aula!"

---

## 📦 MATERIAIS NECESSÁRIOS (por dupla)

- [ ] NodeMCU ESP8266
- [ ] Cabo micro USB + fonte/bateria
- [ ] 1x DHT11 (sensor de temperatura/umidade)
- [ ] 1x LED (qualquer cor)
- [ ] 1x resistor 220Ω (para o LED)
- [ ] 1x botão push-button
- [ ] Jumpers variados
- [ ] Protoboard
- [ ] **Opcional:** Bateria 18650 + suporte (para testar autonomia real)
- [ ] **Opcional:** Multímetro (para medir consumo real)

## ⚠️ PONTOS DE ATENÇÃO

1. **D0→RST obrigatório:** Sem esse fio o deep sleep é permanente. Testar antes da aula!
2. **DHT11 precisa de tempo:** Após `dht.begin()`, aguardar 2 segundos antes da primeira leitura
3. **Buzzer no deep sleep:** Buzzer ativo consome mesmo em sleep — usar transistor para cortar
4. **WiFi.mode(WIFI_OFF):** Só desligar DEPOIS de usar. E conectar ANTES de desligar.
5. **NTP demora:** Primeira sincronização pode levar 5-10 segundos. Paciência.
6. **Drift do RTC:** Após horas, o relógio via millis() pode ter segundos de diferença. Re-sincronizar periodicamente.

## 🎯 RÚBRICA DE AVALIAÇÃO

| Critério | Peso | Descrição |
|----------|------|-----------|
| Deep Sleep funcionando | 25% | Acorda e dorme corretamente |
| Leitura de sensor | 20% | DHT11 lendo dados válidos |
| RTC Memory | 20% | Contador e dados persistem entre ciclos |
| Timestamp correto | 15% | NTP + cálculo de hora local |
| Código organizado | 10% | Comentado, limpo, no GitHub |
| Desafio extra | 10% | MQTT, histórico, ou re-sincronização |

---

*Tempo estimado de preparação do professor: 30 min (testar todos os códigos antes)*
