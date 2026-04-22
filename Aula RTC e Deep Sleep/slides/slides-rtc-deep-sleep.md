# 📊 SLIDES — "RTC, Deep Sleep e Autonomia no ESP8266"

---

## Slide 1 — Capa
# 💤 RTC, Deep Sleep e Autonomia
## Como fazer seu ESP8266 durar meses com uma pilha
**Módulo: Programação Avançada em IoT**
IFSP Capivari — 4º ano

---

## Slide 2 — O Desafio
# 🔋 Quanto tempo dura?
- ESP8266 ligado = **~80 mA**
- Pilha AA alcalina = **~2500 mAh**
- Autonomia: 2500 / 80 = **~31 horas**

> **E se eu precisasse de 6 meses no meio do mato?**

---

## Slide 3 — A Resposta
# 💤 Deep Sleep = ~20 μA
- De 80 mA → 0,02 mA
- **4.000x menos consumo!**
- Autonomia: de 31 horas → **anos**

> O segredo: **dormir mais, acordar menos**

---

## Slide 4 — Quem dorme, vive mais
# 🌍 Exemplos do Mundo Real

---

## Slide 5 — Exemplo 1
# 🏠 Estação Meteorológica na Fazenda
- Mede temperatura a cada 30 min
- Envia para dashboard via Wi-Fi
- Local sem energia elétrica
- **Sem sleep:** 1 dia | **Com sleep:** 8 meses

---

## Slide 6 — Exemplo 2
# 🌾 Irrigação Inteligente
- Sensor de umidade do solo
- Acorda → mede → decide → dorme
- 5 seg acordado, 1 hora dormindo
- **4.000x menos consumo**

---

## Slide 7 — Exemplo 3
# ☀️ Monitoramento Solar
- Acorda só quando há sol
- Transistor + LDR como sensor de luz
- Bateria durante o dia, descansa à noite
- **Perfeito para clima tropical!**

---

## Slide 8 — Exemplo 4
# 🚨 Sensor de Intrusão
- Acelerômetro na porta do galpão
- Acorda por **movimento** (não por timer!)
- Manda alerta no Telegram
- **1 ano** com bateria 18650

---

## Slide 9 — Exemplo 5
# 🗑️ Lixeira Inteligente
- Ultrassom mede nível de enchimento
- Acorda 4x ao dia
- Prefeitura roteiriza coleta
- **Economia de diesel e rotas otimizadas**

---

## Slide 10 — Exemplo 6
# 🐟 Aquicultura
- pH, oxigênio, temperatura do tanque
- Se oxigênio baixo → aciona aerador
- Acorda a cada 15 minutos
- **Sem sleep:** bateria dura 2 dias

---

## Slide 11 — Exemplo 7
# 🌳 Sensor de Queimada
- Gás + temperatura + umidade
- Floresta Amazônica, local remoto
- **Não pode trocar bateria todo mês**
- Deep sleep é questão de viabilidade

---

## Slide 12 — Pausa para Reflexão
# 🤔 Qual projeto vocês fariam?
> "Qual desses seria mais legal implementar aqui no IFSP ou em Capivari?"

---

## Slide 13 — Os 3 Modos de Sleep
# 💤 Como o ESP8266 Dorme

| Modo | Consumo | Acordar com |
|------|---------|-------------|
| **Modem Sleep** | ~15 mA | Timer |
| **Light Sleep** | ~0,4 mA | Timer ou GPIO |
| **Deep Sleep** | ~20 μA | GPIO 16 (RST) |

---

## Slide 14 — Deep Sleep em Detalhe
# 💤 Deep Sleep
- **Tudo** é desligado (CPU, Wi-Fi, RAM)
- Só o **RTC** continua rodando
- Consome apenas **20 μA** (0,02 mA)
- Acorda como se tivesse sido **ligado do zero**
- Roda `setup()` novamente

> **Analogia:** É como desligar o celular. O despertador continua, mas tudo mais reinicia.

---

## Slide 15 — O Pino Mágico
# ⚡ GPIO 16 → RST
- **Conexão obrigatória:** D0 (GPIO 16) → RST
- É o RTC que "cutuca" o RST para acordar
- **Sem esse fio:** o ESP dorme **para sempre**
- Com resistor de 10kΩ entre RST e 3.3V (pull-up) é mais estável

> ⚠️ Primeira coisa a verificar: "Meu ESP não acorda?" → Verifique o fio D0→RST!

---

## Slide 16 — Como Acordar
# ⏰ Três Formas de Acordar

| Forma | Como | Uso |
|-------|------|-----|
| **Timer** | `ESP.deepSleep(10e6)` | Acorda a cada X segundos |
| **Botão** | Pulso em RST | Wake-up manual |
| **Transistor** | RST puxado LOW pelo transistor | **Sensor externo (luz, PIR, etc)** |

> Hoje: Vamos usar **transistor** para acordar com luz!

---

## Slide 17 — Primeiro Código
# 👋 "Olá, Acordei!"
```cpp
void setup() {
  Serial.begin(115200);
  Serial.println("Acordei!");
  delay(2000);
  Serial.println("Dormindo 10s...");
  ESP.deepSleep(10e6);  // microssegundos
}

void loop() {
  // NUNCA executa após deep sleep!
}
```

---

## Slide 18 — Tempo em Microssegundos
# ⏱️ Matemática do Sleep
- `ESP.deepSleep()` recebe **microssegundos**
- 1 segundo = `1e6` (1.000.000 μs)
- 10 segundos = `10e6`
- 1 minuto = `60e6`
- 5 minutos = `300e6`
- 1 hora = `3600e6`

---

## Slide 19 — Calculadora de Autonomia
# 🔢 Quanto tempo dura?
**Dados:**
- Bateria: 3000 mAh
- Acordado (Wi-Fi): 80 mA por 5 segundos
- Dormindo: 0,02 mA
- Ciclo: a cada 30 minutos

**Cálculo:**
- Ciclos/dia: 48
- Tempo acordado/dia: 4 minutos
- Carga acordado: 80 × 4/60 = **5,3 mAh**
- Carga dormindo: 0,02 × 23,93 = **0,48 mAh**
- **Total/dia: ~5,8 mAh**
- **Autonomia: 3000 / 5,8 ≈ 517 dias!** 🤯

---

## Slide 20 — Comparação Visual
# 📊 Com vs Sem Deep Sleep

| Intervalo | Sem Sleep | Com Sleep | Ganho |
|-----------|-----------|-----------|-------|
| Contínuo | 37h | — | — |
| A cada 1 min | 37h | 35 dias | 23x |
| A cada 10 min | 37h | 280 dias | 181x |
| A cada 1 hora | 37h | 517 dias | 335x |

---

## Slide 21 — Acordar por Transistor
# 💡 Interrupt Externo via KSP2222A
```cpp
// Transistor KSP2222A:
// - Emissor → GND
// - Base → LDR + Trimpot (divisor de tensão)
// - Coletor → RST do ESP8266

// No escuro: transistor OFF → ESP dorme
// Na luz: transistor ON → RST LOW → ESP ACORDA!
```
- **Luz alta** → LDR resistência baixa → transistor satura → RST LOW → **ACORDA**
- **Luz baixa** → transistor corta → ESP **DORME**

> 🌞 Projeto solar: só trabalha durante o dia!

---

## Slide 22 — O Problema da Memória
# 🕐 "Que horas são?"
- Deep sleep reinicia TUDO
- Variáveis normais são **perdidas**
- Hora, contadores, dados... tudo some!

> **Como lembrar que horas são sem Wi-Fi?**

---

## Slide 23 — O Problema do ESP32 vs ESP8266
# ⚠️ RTC_DATA_ATTR Só Funciona no ESP32!
- `RTC_DATA_ATTR` é uma feature do **ESP32**
- No **ESP8266**: `RTC_DATA_ATTR` existe mas é limitado
- **Solução para ESP8266**: LittleFS + ArduinoJson

| Solução | ESP32 | ESP8266 | Persiste Power-off? |
|---------|-------|---------|---------------------|
| `RTC_DATA_ATTR` | ✅ Sim | ⚠️ Limitado | ❌ Não |
| **LittleFS + ArduinoJson** | ✅ Sim | ✅ Sim | ✅ Sim |

---

## Slide 24 — LittleFS: O Filesystem do ESP8266
# 📂 LittleFS é Melhor que SPIFFS!
- **LittleFS**: mais novo, mais eficiente, wear-leveling melhor
- **Funciona no ESP8266 e ESP32**
- Resiste a **power-off** (dados persistem!)
- Arquivos JSON = estruturas **dinâmicas**

```cpp
#include <LittleFS.h>
#include <ArduinoJson.h>

// Salvar dados
File file = LittleFS.open("/dados.json", "w");
StaticJsonDocument<512> doc;
doc["ciclos"] = 42;
serializeJson(doc, file);
file.close();
```

---

## Slide 25 — Comparação de Memórias
# 🧠 O Que Sobrevive?

| Tipo | Deep Sleep? | Power-off? | Velocidade | ESP8266? |
|------|-------------|------------|------------|----------|
| RAM normal | ❌ | ❌ | Rápida | ✅ |
| `RTC_DATA_ATTR` | ✅ | ❌ | Rápida | ⚠️ |
| **LittleFS** | ✅ | ✅ | Média | ✅ |
| EEPROM | ✅ | ✅ | Lenta | ✅ |

> **LittleFS = o melhor dos dois mundos!**

---

## Slide 26 — NTP Inteligente
# ⏰ Conecta Uma Vez, Lê Para Sempre
1. **Primeira vez:** Conecta Wi-Fi → sincroniza NTP → salva epoch no JSON
2. **Depois:** Calcula hora via `millis() - millisBase + epochBase`
3. **Economia:** Não conecta Wi-Fi a cada ciclo!

> 5 segundos de Wi-Fi = 5 segundos de 80mA. Sem Wi-Fi = só 5ms a 20mA!

---

## Slide 27 — Projeto Integrador
# 🚀 Estação Solar de Monitoramento
**Requisitos:**
1. ✅ Acorda por luz (transistor KSP2222A + LDR)
2. ✅ Lê DHT11 (temperatura + umidade)
3. ✅ Timestamp correto via NTP inteligente
4. ✅ **LittleFS + ArduinoJson** para persistência
5. ✅ Deep sleep entre ciclos
6. ✅ Só trabalha durante o dia!

**Hardware especial:**
- LDR + Trimpot + Transistor KSP2222A
- Sem timer — desperta por interrupt!

---

## Slide 28 — Circuito do Sensor de Luz
# 💡 Como Funciona o Interrupt por Luz

```
   3.3V ─── LDR ──── ◬─── Base do KSP2222A
                      │
                 Trimpot
                      │
                     GND
                     
   Coletor (C) ──── RST do ESP8266
   Emissor (E) ──── GND
```

**Ajuste do trimpot:**
- Mais para LDR → acorda com menos luz (amanhecer cedo)
- Mais para GND → só acorda com sol forte

---

## Slide 29 — Checklist do Projeto
- [ ] Fio D0 → RST conectado
- [ ] LED pisca ao acordar (feedback)
- [ ] DHT11 lendo dados válidos
- [ ] NTP sincroniza na primeira vez
- [ ] Hora correta entre ciclos
- [ ] LittleFS salvando dados na flash
- [ ] Transistor + LDR funcionando
- [ ] Deep sleep entre ciclos
- [ ] Contador de ciclos persiste
- [ ] Wi-Fi desligado após uso

---

## Slide 30 — Resumo da Aula
# ✅ O Que Aprendemos Hoje
1. Deep Sleep reduz consumo em **~4000x**
2. Conexão **D0→RST** é obrigatória
3. **LittleFS + ArduinoJson** para persistência no ESP8266
4. Transistor KSP2222A + LDR = **interrupt por luz**
5. NTP só precisa **1 vez** — depois calcula local
6. Projeto solar: só trabalha durante o **dia**

> "Sem deep sleep, IoT em campo é **impossível**."

---

## Slide 31 — Próxima Aula
# 🔮 Máquinas de Estado
> "E se ao acordar, o sensor precisasse **decidir** o que fazer?"
> - Temperatura > 30°C → liga cooler
> - Umidade < 40% → liga irrigação
> - Senão → volta a dormir

**Isso é uma Máquina de Estados Finitos (FSM)!**

---

*Total: 31 slides*
