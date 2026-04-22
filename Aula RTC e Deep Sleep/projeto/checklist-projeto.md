# ✅ CHECKLIST DO PROJETO — Estação Solar de Monitoramento

## Nome do Grupo: _______________
## Integrantes: _______________, _______________

---

## 📋 Requisitos Obrigatórios (100 pontos)

### Interrupt por Luz — Transistor KSP2222A (25 pontos)
- [ ] Fio D0 → RST conectado (3 pts)
- [ ] Transistor KSP2222A montado corretamente (E→GND, C→RST, B→divisor) (5 pts)
- [ ] LDR conectado no divisor de tensão (3 pts)
- [ ] Trimpot ajustável para regular limiar de luz (3 pts)
- [ ] Resistor 10kΩ na base do transistor (3 pts)
- [ ] LED pisca como feedback visual ao acordar (3 pts)
- [ ] ESP acorda quando LDR é iluminado (5 pts)

### Deep Sleep (20 pontos)
- [ ] ESP entra em deep sleep corretamente (5 pts)
- [ ] Ciclo repetir quando LDR iluminado novamente (5 pts)
- [ ] ESP fica dormindo quando LDR coberto (escuro) (5 pts)
- [ ] Contador de ciclos implementado (5 pts)

### LittleFS + ArduinoJson (20 pontos)
- [ ] LittleFS inicializado corretamente (3 pts)
- [ ] Arquivo `/estado.json` salvo e carregado (5 pts)
- [ ] Estrutura `Estado` persistida (4 pts)
- [ ] Histórico de leituras em `/leituras.json` (5 pts)
- [ ] Array circular de leituras funcionando (3 pts)

### Leitura de Sensor (15 pontos)
- [ ] DHT11 conectado e funcionando (4 pts)
- [ ] Temperatura lida corretamente (4 pts)
- [ ] Umidade lida corretamente (4 pts)
- [ ] Tratamento de erro (isnan) implementado (3 pts)

### Timestamp e NTP (10 pontos)
- [ ] NTP sincroniza com sucesso (3 pts)
- [ ] Hora calculada corretamente sem Wi-Fi (4 pts)
- [ ] Formato legível (dd/mm/aaaa hh:mm:ss) (3 pts)

### Código e Documentação (10 pontos)
- [ ] Código bem comentado (3 pts)
- [ ] README no GitHub com descrição e fotos (4 pts)
- [ ] Print do Serial Monitor com 5+ ciclos (3 pts)

---

## 🚀 Desafios Extras (+10 pontos cada, máx 30)

### Desafio 1: Medição de Autonomia Real
- [ ] Medir consumo com multímetro em deep sleep
- [ ] Comparar com consumo acordado
- [ ] Calcular autonomia real vs teórica
- [ ] Ajustar intervalos para autonomia > 100 dias

### Desafio 2: Alerta Visual por Temperatura
- [ ] LED piscando rápido se temperatura > 30°C
- [ ] Mensagem de alerta no Serial
- [ ] Limiar configurável

### Desafio 3: DashboardThingSpeak
- [ ] Enviar dados para ThingSpeak
- [ ] Gráfico de temperatura/umidade
- [ ] Mostrar timestamps corretos

### Desafio 4: MQTT
- [ ] Enviar dados para broker MQTT
- [ ] Tópico organizado (ex: estacao/temp)
- [ ] Conexão rápida + envio + desconexão

### Desafio 5: Configuração Wi-Fi via AP
- [ ] Cria Wi-Fi hotspot se não conectar
- [ ] Página web para configurar SSID/senha
- [ ] Salva configuração na flash

---

## 📝 Autoavaliação

| Pergunta | Nota (1-5) |
|----------|------------|
| Entendi o conceito de deep sleep? | ___ |
| Consigo explicar o circuito do transistor? | ___ |
| Sei por que usamos LittleFS em vez de RTC_DATA_ATTR? | ___ |
| O código está funcionando corretamente? | ___ |
| Meu projeto está bem documentado? | ___ |

---

## 🔧 Problemas Comuns e Soluções

| Problema | Causa Provável | Solução |
|----------|----------------|---------|
| ESP dorme e não acorda | Fio D0→RST não conectado | Ligar D0 ao RST |
| Transistor não desliga | Resistor de base muito baixo | Usar 10kΩ |
| Transistor não liga | LDR ou trimpot mal conectado | Verificar circuito divisor |
| LittleFS não inicializa | Filesystem corrompido | `LittleFS.format()` antes de begin() |
| NTP não sincroniza | Wi-Fi 5GHz ou senha errada | Usar rede 2.4GHz |
| Hora errada após horas | Drift do millis() | Re-sincronizar periodicamente |
| JSON parse error | Arquivo corrompido | Apagar e recriar com `LittleFS.format()` |

---

## 📊 Nota Final

| Categoria | Pontos |
|-----------|--------|
| Interrupt por Luz | ___ / 25 |
| Deep Sleep | ___ / 20 |
| LittleFS + ArduinoJson | ___ / 20 |
| Sensor | ___ / 15 |
| Timestamp/NTP | ___ / 10 |
| Código/Docs | ___ / 10 |
| **Subtotal** | **___ / 100** |
| Desafios extras | ___ / 30 |
| **TOTAL** | **___ / 130** |

---

## 🔌 Circuito de Referência — Interrupt por Luz

```
    NodeMCU ESP8266
    ┌─────────────────────────────────────────┐
    │                                         │
    │   3.3V ────────────────────────────┐    │
    │                                    │    │
    │   RST ◄──────────────────┐        │    │
    │                           │        │    │
    │   D0/GPIO16 ──────────────┼────────┘    │
    │                           │             │
    │   A0 (debug) ─────────────┤             │
    │                           │             │
    │   D4 ──────────────────────┤             │
    │   (DHT11)                  │             │
    │                           │             │
    │   2 ───────────────────────┤             │
    │   (LED)                    │             │
    │                           │             │
    │   GND ─────────────────────┴─────────────┤
    │                                         │
    └─────────────────────────────────────────┘
    
    KSP2222A Circuit:
    
         3.3V ──── LDR ──── ◬─── Base (via R 10kΩ)
                            │
                       Trimpot
                            │
                           GND
                           
         Coletor (C) ──── RST do ESP8266
         Emissor (E) ──── GND
```

---

*Avaliação formativa — o objetivo é aprender, não apenas pontuar!*
