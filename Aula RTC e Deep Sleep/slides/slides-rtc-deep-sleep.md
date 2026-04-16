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
# 🚨 Sensor de Intrusão
- Acelerômetro na porta do galpão
- Acorda por **movimento** (não por timer!)
- Manda alerta no Telegram
- **1 ano** com bateria 18650

---

## Slide 8 — Exemplo 4
# 🐝 Monitoramento de Colmeias
- Peso + temperatura + som
- Projeto real da **Embrapa**
- Apiário no meio do mato
- Acorda a cada hora, transmite, dorme

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
# 🅿️ Vaga Inteligente
- Sensor magnético detecta carro
- Acorda quando campo magnético muda
- **3 anos com 2 pilhas AA!**

---

## Slide 12 — Exemplo 8
# 🌳 Sensor de Queimada
- Gás + temperatura + umidade
- Floresta Amazônica, local remoto
- **Não pode trocar bateria todo mês**
- Deep sleep é questão de viabilidade

---

## Slide 13 — Pausa para Reflexão
# 🤔 Qual projeto vocês fariam?
> "Qual desses seria mais legal implementar aqui no IFSP ou em Capivari?"

---

## Slide 14 — Os 3 Modos de Sleep
# 💤 Como o ESP8266 Dorme

| Modo | Consumo | Acordar com |
|------|---------|-------------|
| **Modem Sleep** | ~15 mA | Timer |
| **Light Sleep** | ~0,4 mA | Timer ou GPIO |
| **Deep Sleep** | ~20 μA | GPIO 16 (RST) |

---

## Slide 15 — Deep Sleep em Detalhe
# 💤 Deep Sleep
- **Tudo** é desligado (CPU, Wi-Fi, RAM)
- Só o **RTC** continua rodando
- Consome apenas **20 μA** (0,02 mA)
- Acorda como se tivesse sido **ligado do zero**
- Roda `setup()` novamente

> **Analogia:** É como desligar o celular. O despertador continua, mas tudo mais reinicia.

---

## Slide 16 — O Pino Mágico
# ⚡ GPIO 16 → RST
- **Conexão obrigatória:** D0 (GPIO 16) → RST
- É o RTC que "cutuca" o RST para acordar
- **Sem esse fio:** o ESP dorme **para sempre**
- Com resistor de 10kΩ entre RST e 3.3V (pull-up) é mais estável

> ⚠️ Primeira coisa a verificar: "Meu ESP não acorda?" → Verifique o fio D0→RST!

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

## Slide 21 — Acordar por Botão
# 🔘 Deep Sleep com Interrupt
```cpp
void setup() {
  Serial.begin(115200);
  Serial.println("Acordei por botão!");
  delay(3000);
  Serial.println("Voltando a dormir...");
  ESP.deepSleep(0);  // "infinito" — só botão
}

void loop() {}
```
- Botão entre **RST** e **GND**
- `deepSleep(0)` = só acorda por RST externo
- Aplicação: sensor de porta, alerta de movimento

---

## Slide 22 — O Problema da Memória
# 🕐 "Que horas são?"
- Deep sleep reinicia TUDO
- Variáveis normais são **perdidas**
- Hora, contadores, dados... tudo some!

> **Como lembrar que horas são sem Wi-Fi?**

---

## Slide 23 — RTC Memory
# 📝 O "Post-it" do ESP8266
- **512 bytes** que sobrevivem ao deep sleep
- Declarado com `RTC_DATA_ATTR`
- Rápido como RAM (sem desgaste de flash)
- **Não** sobrevive a desconexão de energia

```cpp
RTC_DATA_ATTR int contador = 0;  // Persiste!
RTC_DATA_ATTR float ultimaTemperatura = 0;
```

---

## Slide 24 — Comparação de Memórias
# 🧠 O Que Sobrevive?

| Tipo | Deep Sleep? | Power-off? | Velocidade |
|------|-------------|------------|------------|
| RAM normal | ❌ | ❌ | Rápida |
| **RTC memory** | ✅ | ❌ | Rápida |
| EEPROM | ✅ | ✅ | Média |
| SPIFFS | ✅ | ✅ | Lenta |

---

## Slide 25 — NTP Inteligente
# ⏰ Conecta Uma Vez, Lempra Para Sempre
1. **Primeira vez:** Conecta Wi-Fi → sincroniza NTP → salva epoch
2. **Depois:** Calcula hora via `millis() - millisBase + epochBase`
3. **Economia:** Não conecta Wi-Fi a cada ciclo!

> 5 segundos de Wi-Fi = 5 segundos de 80mA. Sem Wi-Fi = só 5ms a 20mA!

---

## Slide 26 — Código: NTP + RTC Memory
```cpp
RTC_DATA_ATTR bool ntpOk = false;
RTC_DATA_ATTR time_t epochBase = 0;
RTC_DATA_ATTR unsigned long millisBase = 0;

void setup() {
  if (!ntpOk) {
    WiFi.begin(ssid, senha);
    // ... sincroniza NTP ...
    epochBase = time(nullptr);
    millisBase = millis();
    ntpOk = true;
    WiFi.disconnect(true);
  }
  
  time_t agora = epochBase + (millis() - millisBase) / 1000;
  Serial.printf("Hora: %s", ctime(&agora));
  
  ESP.deepSleep(300e6);  // 5 min
}
```

---

## Slide 27 — Sensor com Timestamp
# 🌡️ Logger Completo
- DHT11 lê temperatura e umidade
- RTC memory guarda hora da sincronização
- Cada leitura tem **timestamp correto**
- Sem Wi-Fi na maioria dos ciclos

---

## Slide 28 — Projeto Integrador
# 🚀 Estação Autônoma de Monitoramento
**Requisitos:**
1. ✅ Acorda a cada 5 minutos
2. ✅ Lê DHT11 (temperatura + umidade)
3. ✅ Timestamp correto em cada leitura
4. ✅ NTP sincroniza só 1 vez
5. ✅ RTC memory para contadores e hora
6. ✅ Deep sleep entre leituras

**Desafio extra:** Enviar via MQTT

---

## Slide 29 — Checklist do Projeto
- [ ] Fio D0 → RST conectado
- [ ] LED pisca ao acordar (feedback)
- [ ] DHT11 lendo dados válidos
- [ ] NTP sincroniza na primeira vez
- [ ] Hora correta entre ciclos
- [ ] Timestamps no Serial
- [ ] Deep sleep de 5 minutos
- [ ] Contador de ciclos funciona
- [ ] Wi-Fi desligado após uso
- [ ] Código limpo e comentado

---

## Slide 30 — Resumo da Aula
# ✅ O Que Aprendemos Hoje
1. Deep Sleep reduz consumo em **~4000x**
2. Conexão **D0→RST** é obrigatória
3. **RTC memory** persiste dados entre ciclos
4. NTP só precisa **1 vez** — depois calcula local
5. Autonomia depende de: **tempo acordado × intervalo**

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
