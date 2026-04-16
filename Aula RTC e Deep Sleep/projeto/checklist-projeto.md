# ✅ CHECKLIST DO PROJETO — Estação Autônoma de Monitoramento

## Nome do Grupo: _______________
## Integrantes: _______________, _______________

---

## 📋 Requisitos Obrigatórios (100 pontos)

### Deep Sleep (25 pontos)
- [ ] Fio D0 → RST conectado (3 pts)
- [ ] ESP acorda e dorme corretamente (5 pts)
- [ ] Intervalo de sleep configurável (5 pts)
- [ ] LED pisca como feedback visual ao acordar (5 pts)
- [ ] Contador de ciclos funciona via RTC memory (7 pts)

### Leitura de Sensor (20 pontos)
- [ ] DHT11 conectado e funcionando (5 pts)
- [ ] Temperatura lida corretamente (5 pts)
- [ ] Umidade lida corretamente (5 pts)
- [ ] Tratamento de erro (isnan) implementado (5 pts)

### RTC Memory (20 pontos)
- [ ] Variáveis declaradas com RTC_DATA_ATTR (5 pts)
- [ ] Dados persistem entre ciclos de sleep (5 pts)
- [ ] Contador de ciclos não reseta ao acordar (5 pts)
- [ ] NTP sincronizado apenas na primeira vez (5 pts)

### Timestamp Correto (15 pontos)
- [ ] NTP sincroniza com sucesso (5 pts)
- [ ] Hora calculada corretamente sem Wi-Fi (5 pts)
- [ ] Formato legível (dd/mm/aaaa hh:mm:ss) (5 pts)

### Código e Documentação (10 pontos)
- [ ] Código bem comentado (3 pts)
- [ ] README no GitHub com descrição do projeto (4 pts)
- [ ] Print do Serial Monitor com 5+ ciclos (3 pts)

### Funcionamento Geral (10 pontos)
- [ ] Wi-Fi desligado após uso (3 pts)
- [ ] Sistema estável (não trava após 10+ ciclos) (4 pts)
- [ ] Autonomia calculada no código ou README (3 pts)

---

## 🚀 Desafios Extras (+10 pontos cada, máx 30)

### Desafio 1: Envio MQTT
- [ ] Dados enviados para broker MQTT local
- [ ] Tópico organizado (ex: estacao/temp, estacao/umid)
- [ ] Conexão MQTT + envio + desconexão rápida

### Desafio 2: Histórico de Leituras
- [ ] Array circular de 10 leituras na RTC memory
- [ ] Histórico impresso a cada N ciclos
- [ ] Dados ordenados por timestamp

### Desafio 3: Re-sincronização Automática
- [ ] NTP re-sincroniza a cada 100 ciclos
- [ ] Drift corrigido automaticamente
- [ ] Log de re-sincronização no Serial

### Desafio 4: Alerta por Temperatura
- [ ] Alerta visual (LED piscando rápido) se temp > 30°C
- [ ] Mensagem de alerta no Serial
- [ ] Limiar configurável no código

### Desafio 5: Medição Real de Consumo
- [ ] Medir consumo com multímetro em deep sleep
- [ ] Comparar com consumo acordado
- [ ] Calcular autonomia real vs teórica

---

## 📝 Autoavaliação

| Pergunta | Nota (1-5) |
|----------|------------|
| Entendi o conceito de deep sleep? | ___ |
| Consigo explicar RTC memory para um colega? | ___ |
| Sei calcular autonomia de bateria? | ___ |
| O código está funcionando corretamente? | ___ |
| Meu projeto está bem documentado? | ___ |

---

## 🔧 Problemas Comuns e Soluções

| Problema | Causa Provável | Solução |
|----------|----------------|---------|
| ESP dorme e não acorda | Fio D0→RST não conectado | Ligar D0 ao RST |
| DHT11 retorna NaN | Sensor não estabilizou | Aguardar 2s após begin() |
| NTP não sincroniza | Wi-Fi 5GHz ou firewall | Usar rede 2.4GHz |
| Hora errada após horas | Drift do millis() | Re-sincronizar NTP periodicamente |
| Serial mostra lixo | Baud rate errado | Confirmar 115200 no Monitor |
| Ciclo reseta contador | Não usou RTC_DATA_ATTR | Declarar com RTC_DATA_ATTR |

---

## 📊 Nota Final

| Categoria | Pontos |
|-----------|--------|
| Deep Sleep | ___ / 25 |
| Sensor | ___ / 20 |
| RTC Memory | ___ / 20 |
| Timestamp | ___ / 15 |
| Código/Docs | ___ / 10 |
| Funcionamento | ___ / 10 |
| **Subtotal** | **___ / 100** |
| Desafios extras | ___ / 30 |
| **TOTAL** | **___ / 130** |

---

*Avaliação formativa — o objetivo é aprender, não apenas pontuar!*
