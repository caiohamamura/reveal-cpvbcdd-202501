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
3. Implementar **interrupt por luz** usando transistor KSP2222A + LDR
4. Usar **LittleFS + ArduinoJson** para persistir dados (solução ESP8266!)
5. Projetar um sistema IoT **solar-powered** que opera durante o dia

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

#### 5-25 min: EXEMPLOS DO MUNDO REAL — "Quem dorme, vive mais" 🌍

**Apresentar 7 exemplos reais:**

1. **🏠 Estação meteorológica na fazenda**
   - Mede temperatura/umidade a cada 30 minutos
   - **Sem deep sleep:** 1 dia de bateria. **Com deep sleep:** 8 meses

2. **🌾 Irrigação inteligente no campo**
   - Acorda, mede, decide se irriga, volta a dormir
   - **Consumo:** de 80mA para 20μA (4.000x menos!)

3. **☀️ Monitoramento solar (NOVO!)**
   - Acorda só quando há luz
   - Transistor + LDR como sensor
   - **Perfeito para clima tropical!**

4. **🚨 Sensor de intrusão em galpão**
   - Acorda por interrupt (não por timer)
   - **Autonomia:** 1 ano com bateria 18650

5. **🐟 Tanque de peixes (aquicultura)**
   - Monitora pH, oxigênio e temperatura
   - **Sem deep sleep:** bateria dura 2 dias

6. **🌳 Sensor de queimada na floresta**
   - Local remoto na Amazônia
   - **Crítico:** não pode trocar bateria todo mês

7. **🗑️ Lixeira inteligente da cidade**
   - Acorda 4x ao dia, envia para a prefeitura

**Pergunta de reflexão:**
> "Qual desses projetos vocês acham que seria mais legal implementar aqui no IFSP?"

#### 25-35 min: TEORIA — Como o ESP8266 dorme 💤

**Slide/Quadro: Os 3 modos de sleep do ESP8266**

| Modo | Consumo | Acordar com | Uso típico |
|------|---------|-------------|------------|
| **Modem Sleep** | ~15mA | Timer automático | Wi-Fi desligado entre transmissões |
| **Light Sleep** | ~0.4mA | Timer ou GPIO | CPU pausada, RAM mantida |
| **Deep Sleep** | ~20μA (0.02mA) | GPIO 16 (RST) | Tudo desligado, só RTC funciona |

**Ponto crucial — o pino RST:**
- GPIO 16 deve ser conectado ao RST
- **Sem esse fio, o ESP8266 dorme para sempre**

#### 35-42 min: DEMONSTRAÇÃO — "Pisca-Dorme" ao Vivo

```cpp
void setup() {
  Serial.begin(115200);
  Serial.println("Acordei!");
  for(int i=0; i<3; i++) {
    digitalWrite(LED_PIN, LOW);
    delay(200);
    digitalWrite(LED_PIN, HIGH);
    delay(200);
  }
  ESP.deepSleep(10e6);  // 10 segundos
}
```

**Pergunta-chave:**
> "Se o ESP reinicia do zero, como ele lembra que horas são? Que dados já leu?"

→ Resposta: **LittleFS + ArduinoJson** (não RTC_DATA_ATTR!)

#### 42-45 min: EXERCÍCIO RÁPIDO — "Calculadora de Autonomia"

| Cenário | Sem Sleep | Com Sleep | Ganho |
|---------|-----------|-----------|-------|
| LED piscando (contínuo) | 15h | - | — |
| Leitura a cada 1 hora (5s acordado) | 15h | 517 dias | 827x |

---

### AULA 2: MÃO NA MASSA — INTERRUPT POR LUZ (45 min)

#### 0-5 min: RECAPITULAÇÃO RÁPIDA
1. "Qual o consumo do deep sleep?" (~20μA)
2. "Qual pino precisa ser conectado ao RST?" (GPIO 16 / D0)
3. "O que acontece com o código ao acordar?" (Reinicia do zero)
4. "RTC_DATA_ATTR funciona no ESP8266?" (⚠️ NÃO! LittleFS!)

#### 5-15 min: O PROBLEMA DO RTC_DATA_ATTR — "Não Funciona no ESP8266!"

**Explicação:**
> "Muita gente usa `RTC_DATA_ATTR` no ESP32. Mas aqui no ESP8266, essa memória NÃO persiste em power-off! O que significa que se a bateria morrer, você perde tudo."

**Solução: LittleFS + ArduinoJson**
- Funciona no ESP8266 ✅
- Persiste em power-off ✅
- Estruturas dinâmicas ✅

#### 15-30 min: HANDS-ON 1 — "Acorda por Luz" 💡

**Montar o circuito do transistor KSP2222A:**

```
   3.3V ─── LDR ──── ◬─── Base do KSP2222A (via resistor 10kΩ)
                      │
                 Trimpot
                      │
                     GND
                     
   Coletor (C) ──── RST do ESP8266
   Emissor (E) ──── GND
```

**Código 2: Demo do interrupt por luz**

```cpp
// Carregar e estudiar o Código 2: 2-acorda-luz-transistor.ino
// Este código fica ACORDADO esperando o interrupt funcionar
// Cobre/descovered o LDR para ver o transistor ligar/desligar
```

**Teste:**
1. Carregar código
2. Observar LED piscando
3. Cobrir LDR → LED para de piscar? (transistor OFF)
4. Iluminar LDR → LED volta a piscar? (reset simula wake-up)

#### 30-40 min: HANDS-ON 2 — "LittleFS Persistência"

**Código 3: 3-littlefs-persistencia.ino**

```cpp
// concepts:
// - LittleFS.begin()
// - File file = LittleFS.open("/dados.json", "w");
// - StaticJsonDocument<512> doc;
// - serializeJson() / deserializeJson()
// - Persistência que sobrevive a power-off!
```

**Desafio:** Modificar para salvar a leitura do LDR e recuperar ao reiniciar.

#### 40-45 min: DISCUSSÃO — "Solar vs Timer"

| Aspecto | Timer | Solar (Luz) |
|---------|-------|-------------|
| Acorda | A cada X segundos | Quando há luz |
| Economia | Boa | Excelente (só de dia) |
| Ideal para | Indoor | Outdoor com sol |
| Noite | Continua gastando | Dorme de graça |

---

### AULA 3: NTP INTELIGENTE + LITTLEFS (45 min)

#### 0-5 min: O PROBLEMA — "Preciso conectar Wi-Fi toda vez?"

**Demonstrar:**
> "Conectar Wi-Fi = 5 segundos a 80mA = MUITA energia!"
> "Solução: conecta UMA vez, calcula depois!"

#### 5-20 min: TEORIA — NTP Inteligente

```cpp
// Primeira vez: conecta, sincroniza, salva
epochBase = timeClient.getEpochTime();
millisBase = millis();

// Ciclos seguintes: calcula sem Wi-Fi!
agora = epochBase + (millis() - millisBase) / 1000;
```

**Código 4: 4-sincronizacao-ntp.ino**

#### 20-30 min: HANDS-ON — Testar NTP + LittleFS

**Código completo:**
```cpp
// - Carrega estado do arquivo JSON
// - Se não tem NTP, sincroniza
// - Se já tem, usa cálculo local
// - Salva antes de dormir
```

#### 30-40 min: COMPARAÇÃO — RTC_DATA_ATTR vs LittleFS

| Critério | RTC_DATA_ATTR | LittleFS + JSON |
|----------|---------------|-----------------|
| ESP8266 | ⚠️ Funciona mal | ✅ Perfeito |
| Power-off | ❌ Perde | ✅ Mantém |
| Estruturas | Apenas primitivos | ✅ JSON completo |
| EEPROM | — | ✅ Usa flash |
| Código | Simples | ⭐ Um pouco mais |

#### 40-45 min: DESAFIO

**Guardar histórico de 10 leituras na flash:**
- Array circular de structs Leitura
- Salvar em `/leituras.json`
- Carregar e imprimir ao acordar

---

### AULA 4: PROJETO INTEGRADOR — "Estação Solar" ☀️ (45 min)

#### 0-5 min: BRIEFING DO PROJETO

**O projeto:** Estação solar de monitoramento que:
1. Acorda por luz (transistor KSP2222A + LDR)
2. Lê temperatura e umidade (DHT11)
3. Timestamp correto (NTP inteligente)
4. Dados persistem via LittleFS + ArduinoJson
5. Só trabalha durante o dia!
6. Deep sleep entre ciclos

#### 5-35 min: IMPLEMENTAÇÃO EM DUPLAS

**Código 5: 5-projeto-estacao-solar.ino**

**Checklist do projeto:**

- [ ] Conexão D0 → RST para deep sleep funcionar
- [ ] Circuito do transistor + LDR montado
- [ ] Trimpot ajustado para limiar de luz
- [ ] LED pisca como feedback visual ao acordar
- [ ] DHT11 lendo corretamente
- [ ] LittleFS salvando dados (estado.json + leituras.json)
- [ ] NTP sincroniza na primeira vez
- [ ] Hora mantida corretamente entre ciclos
- [ ] Leituras com timestamp formatado no Serial
- [ ] Deep sleep configurado
- [ ] Contador de ciclos persiste entre ciclos

**Testes:**
1. Cubra o LDR → ESP deveria dormir
2. Ilumine o LDR → ESP deveria acordar
3. Observe os ciclos no Serial Monitor

#### 35-40 min: APRESENTAÇÕES RÁPIDAS (2 min por dupla)
- Mostrar o Serial Monitor com os ciclos
- Explicar o circuito do transistor
- Ajustar o trimpot para mostrar limiar

#### 40-45 min: ENCERRAMENTO + GANCHO

**Resumo:**
1. Deep Sleep = 4000x menos consumo
2. LittleFS + ArduinoJson = persistência no ESP8266
3. Transistor + LDR = interrupt por luz
4. NTP = conecta 1 vez, lê depois
5. Solar = só trabalha de dia!

**Gancho para próxima aula:**
> "Hoje nosso sensor dorme sozinho. Mas e se ele precisasse tomar DECISÕES? Tipo: 'se a temperatura passou de 30°C, liga o cooler'. Isso é uma **Máquina de Estados**!"

---

## 📦 MATERIAIS NECESSÁRIOS (por dupla)

- [ ] NodeMCU ESP8266
- [ ] Cabo micro USB
- [ ] 1x DHT11 (sensor de temperatura/umidade)
- [ ] 1x LED (qualquer cor)
- [ ] 1x resistor 220Ω (para o LED)
- [ ] 1x **LDR** (sensor de luz)
- [ ] 1x **Transistor KSP2222A** (NPN)
- [ ] 1x **Trimpot** 10kΩ ou 100kΩ
- [ ] 1x **Resistor** 10kΩ
- [ ] Jumpers variados
- [ ] Protoboard
- [ ] **Fio D0 → RST** (obrigatório!)

## 🔌 Pinagem do KSP2222A (vista de frente)

```
      ┌──────────────┐
      │  B    C      │
      │  │    │      │
      └──│────│──────┘
         │    │
         E    └──────────→ RST do ESP8266
         │
         └────── GND
```

## ⚠️ PONTOS DE ATENÇÃO

1. **D0→RST obrigatório:** Sem esse fio o deep sleep é permanente
2. **Transistor não satura?**: Verifique resistor de base (10kΩ)
3. **Trimpot:** Ajuste fino do limiar de luz
4. **LittleFS.format():** Se corromper, formate antes de begin()
5. **Wi-Fi.mode(WIFI_OFF):** Só desligue DEPOIS de sincronizar NTP
6. **NTP demora:** Primeira sincronização pode levar 5-10 segundos

## 🎯 RÚBRICA DE AVALIAÇÃO

| Critério | Peso | Descrição |
|----------|------|-----------|
| Deep Sleep funcionando | 20% | Acorda e dorme corretamente |
| Interrupt por luz | 25% | Transistor + LDR + trimpot funcionando |
| LittleFS Persistência | 20% | Dados persistem entre ciclos |
| Leitura de sensor | 15% | DHT11 lendo dados válidos |
| Timestamp correto | 10% | NTP + cálculo de hora local |
| Código organizado | 10% | Comentado, limpo |

---

*Tempo estimado de preparação do professor: 30 min (testar circuito do transistor!)*
