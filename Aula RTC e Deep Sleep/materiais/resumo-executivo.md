# 📊 RESUMO EXECUTIVO
## "RTC, Deep Sleep e Autonomia no ESP8266"
### Versão Professor Caio — 22/04/2026

---

## 📍 Contexto
- **Módulo:** Programação Avançada em IoT (Aula 11)
- **Sequência:** Depois de Timing/NTP → Antes de Máquina de Estados
- **Foco:** Economia de energia + persistência de dados + interrupt por botão/MQTT

---

## 🎯 Objetivos de Aprendizagem

1. Entender **por que** deep sleep é essencial em IoT de campo
2. Implementar deep sleep com despertar por **timer** e por **botão**
3. Implementar persistência com **RTC Memory** (reset) e **LittleFS + ArduinoJson** (power-off)
4. Criar um projeto integrador com **MQTT + deep sleep**

---

## 📅 Estrutura da Aula (4 × 45 min)

| Aula | Tema | Tipo | Duração |
|------|------|------|---------|
| **1** | Engajamento + Teoria + Pisca-Dorme demo | Expositiva + Demo | 45 min |
| **2** | Hands-on 1 (guiado): Pisca → Sleep → Botão wake | Prática guiada | 45 min |
| **3** | Hands-on 2 (base a ajustar): LittleFS + NTP + RTC Memory | Prática mandiri | 45 min |
| **4** | Projeto: Contador de flashes via MQTT | Projeto em duplas | 45 min |

---

## 🔑 Conceitos-Chave

| Conceito | Detalhe |
|----------|---------|
| **Deep Sleep** | 20 µA vs 80 mA = **4000x economia** |
| **Wake por timer** | D0 (GPIO16) → RST após `ESP.deepSleep(tempo)` |
| **Wake por botão** | Botão push entre RST e GND (pull-up 10kΩ) |
| **Máximo deep sleep** | ~71 minutos (2³² µs) |
| **RTC Memory** | `ESP.rtcUserMemoryWrite/Read` — 512 bytes, persiste reset |
| **LittleFS** | Filesystem interno — persiste power-off |
| **NTP Inteligente** | Conecta 1x, calcula localmente depois |
| **MQTT** | Pub/sub com broker (test.mosquitto.org) |

---

## 📦 Hardware Necessário (por dupla)

### Aula 2
- NodeMCU ESP8266 + cabo micro USB
- Protoboard + jumpers
- Botão push (ou usar FLASH/GPIO0 do NodeMCU)
- Resistor 10kΩ (pull-up RST)
- Fio D0 → RST

### Aula 4 (projeto)
- NodeMCU ESP8266 + cabo USB
- Rede WiFi do laboratório
- Acesso a `test.mosquitto.org:1883`

---

## 🏗️ Estrutura Pedagógica

Siguiendo `Roteiro_resumido.md`:

```
Abertura (contexto)
    ↓
Exemplos reais (engajamento)
    ↓
Teoria (3 modos de sleep, como acordar)
    ↓
Solução (deep sleep + persistência)
    ↓
Hands-on 1 (guiado — código completo entregue)
    ↓
Hands-on 2 (base a ajustar — alunos completam TODOs)
    ↓
Projeto (MQTT + deep sleep — integração)
```

---

## 📝 Projeto Integrador: "Contador de Flashes via MQTT"

**Fluxo:**
1. ESP8266 conecta ao Wi-Fi
2. Conecta ao broker MQTT `test.mosquitto.org:1883`
3. Inscreve-se em `ifsp-capivari/ciclos/[NOME_DA_DUPLA]`
4. Recebe último valor (ou 0)
5. Incrementa e publica
6. Deep sleep
7. Repete

**Por que MQTT?**
- Demonstra comunicação machine-to-machine
- Broker mantém estado (persistência via cloud)
- Única plataforma que combina Wi-Fi + deep sleep + comunicação em tempo real

---

## ⚠️ Pontos de Atenção

1. **D0→RST obrigatório** para wake por timer (senão deep sleep é permanente)
2. **Pull-up 10kΩ no RST** é necessário para o botão de wake funcionar
3. **RTC Memory NÃO sobrevive a power-off** — só a reset! Para persistência real, usar LittleFS
4. **LittleFS.format()** se o filesystem ficar corrompido
5. **Wi-Fi.mode(WIFI_OFF)** após NTP para economizar energia
6. **MQTT usa porta 1883** — verificar se rede não bloqueia

---

## 🎯 Rúbrica de Avaliação

| Critério | Peso |
|----------|------|
| Deep Sleep funcionando | 20% |
| Wake por botão | 15% |
| RTC Memory | 20% |
| LittleFS Persistência | 20% |
| NTP Inteligente | 15% |
| MQTT (Aula 4) | 10% |

---

## 📁 Arquivos Gerados

```
Aula RTC e Deep Sleep/
├── codigos/
│   ├── 1-pisca-dorme.ino              # Demo deep sleep básico
│   ├── 2-botao-wake.ino               # Hands-on 1 (completo)
│   ├── 3-rtc-memory.ino               # RTC memory (completo)
│   ├── 4-littlefs-ntp-skeleton.ino   # Hands-on 2 (com TODOs)
│   └── 5-mqtt-contador.ino            # Projeto MQTT (completo)
├── materiais/
│   ├── roteiro-aula-detalhado.md      # Este roteiro
│   └── resumo-executivo.md            # Este arquivo
├── projeto/
│   └── checklist-projeto.md           # Checklist do projeto MQTT
└── slides/
    └── slides-rtc-deep-sleep.md       # Apresentação (31 slides)
```

---

*Criado em: 22/04/2026*
*Atualizado para seguir Roteiro_resumido.md*
