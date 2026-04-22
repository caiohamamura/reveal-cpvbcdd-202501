# 📊 RESUMO EXECUTIVO
## "RTC, Deep Sleep e Autonomia no ESP8266"

### Contexto
- **Módulo:** Programação Avançada em IoT (Aula 2)
- **Sequência:** Depois de Timing/NTP → Antes de Máquina de Estados
- **Foco:** Economia de energia + persistência de dados + interrupt por luz

### 🎯 Objetivos
1. Entender **por que** deep sleep é essencial em IoT de campo
2. Implementar deep sleep com despertar por **timer** e por **interrupt (transistor)**
3. Usar **LittleFS + ArduinoJson** para persistir dados (solução ESP8266!)
4. Manter hora correta sem Wi-Fi (NTP + cálculo local)
5. Criar um sistema **solar-powered** que só trabalha de dia

### 🆕 Diferencial: Interrupt por Luz
Em vez de acordar por timer, o projeto usa:
- **LDR + Trimpot + Transistor KSP2222A**
- Durante o dia: transistor liga → ESP acorda
- Durante a noite: transistor desliga → ESP dorme
- **Ideal para climas tropicais com ciclos claros de 12h!**

### 🆕 Diferencial: LittleFS em vez de RTC_DATA_ATTR
- `RTC_DATA_ATTR` só funciona **corretamente** no ESP32
- No ESP8266: é limitado e **não persiste em power-off**
- **Solução:** LittleFS (filesystem) + ArduinoJson
- Vantagens: persiste em power-off, estruturas dinâmicas, funciona em ambos

### 📁 Arquivos criados

```
Aula RTC e Deep Sleep/
├── slides/
│   └── slides-rtc-deep-sleep.md     # 31 slides
├── materiais/
│   ├── roteiro-aula-detalhado.md    # Timing minuto a minuto
│   └── resumo-executivo.md          # Este arquivo
├── codigos/
│   ├── 1-pisca-dorme.ino            # Hello World do deep sleep
│   ├── 2-acorda-luz-transistor.ino  # Demo: interrupt por luz
│   ├── 3-littlefs-persistencia.ino  # LittleFS + ArduinoJson
│   ├── 4-sincronizacao-ntp.ino      # NTP inteligente
│   └── 5-projeto-estacao-solar.ino  # Projeto completo
└── projeto/
    └── checklist-projeto.md          # Rubrica + autoavaliação
```

### 🔑 Conceitos-chave
- **Deep Sleep:** 20 μA vs 80 mA = 4000x economia
- **D0→RST:** Conexão obrigatória para acordar
- **KSP2222A:** Transistor NPN como interruptor controlado por luz
- **LittleFS + ArduinoJson:** Persistência que funciona no ESP8266
- **NTP inteligente:** Sincroniza 1 vez, calcula depois
- **Autonomia solar:** 3000 mAh → ~517 dias (1 leitura/hora)

### 🔌 Hardware Especial (além do usual)
- **Transistor KSP2222A** (NPN)
- **LDR** (Light Dependent Resistor)
- **Trimpot** 10kΩ ou 100kΩ
- **Resistor** 10kΩ (para base do transistor)

### 📅 Estrutura (4 aulas × 45 min)

| Aula | Tema | Tipo |
|------|------|------|
| 1 | Engajamento + Teoria | Expositiva + Exercício |
| 2 | Hands-on: pisca-dorme + interrupt luz | Prática |
| 3 | LittleFS + NTP Inteligente | Prática |
| 4 | Projeto Integrador — Estação Solar | Projeto em duplas |

### 📝 Gancho para próxima aula
> "E se ao acordar, o sensor precisasse tomar DECISÕES? → **Máquina de Estados Finitos (FSM)**"

---
*Criado em: 22/04/2026*
*Atualizado para LittleFS + interrupt por luz*
