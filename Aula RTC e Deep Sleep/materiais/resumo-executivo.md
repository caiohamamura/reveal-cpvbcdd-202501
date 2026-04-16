# 📊 RESUMO EXECUTIVO
## "RTC, Deep Sleep e Autonomia no ESP8266"

### Contexto
- **Módulo:** Programação Avançada em IoT (Aula 2)
- **Sequência:** Depois de Timing/NTP → Antes de Máquina de Estados
- **Foco:** Economia de energia + persistência de dados entre ciclos de sono

### Objetivos
1. Entender **por que** deep sleep é essencial em IoT de campo
2. Implementar deep sleep com despertar por timer e por botão
3. Usar **RTC memory** para persistir dados entre ciclos
4. Manter hora correta sem Wi-Fi (NTP + cálculo local)
5. Calcular autonomia de bateria para projetos reais

### Estrutura (4 aulas × 45 min)

| Aula | Tema | Tipo |
|------|------|------|
| 1 | Engajamento + Teoria (exemplos reais, modos de sleep, calculadora) | Expositiva + Exercício |
| 2 | Hands-on (pisca-dorme, sensor dorme, acorda por botão) | Prática |
| 3 | RTC Memory + NTP Inteligente | Prática |
| 4 | Projeto Integrador — Estação Autônoma | Projeto em duplas |

### Diferencial desta aula
**8 exemplos do mundo real** para engajamento:
1. 🏠 Estação meteorológica na fazenda
2. 🌾 Irrigação inteligente
3. 🚨 Sensor de intrusão em galpão
4. 🐝 Monitoramento de colmeias (Embrapa)
5. 🗑️ Lixeira inteligente da cidade
6. 🐟 Aquicultura (tanque de peixes)
7. 🅿️ Vaga de estacionamento inteligente
8. 🌳 Sensor de queimada na floresta

### Arquivos criados

```
Aula RTC e Deep Sleep/
├── slides/
│   └── slides-rtc-deep-sleep.md     # 31 slides
├── materiais/
│   └── roteiro-aula-detalhado.md    # Timing minuto a minuto
├── codigos/
│   ├── 1-pisca-dorme.ino            # Hello World do deep sleep
│   ├── 2-sensor-dorme.ino           # DHT11 + deep sleep
│   ├── 3-acorda-botao.ino           # Despertar por botão/RST
│   ├── 4-relogio-rtc-ntp.ino        # NTP + RTC memory
│   └── 5-projeto-estacao-autonoma.ino # Projeto completo
└── projeto/
    └── checklist-projeto.md          # Rubrica + autoavaliação
```

### Conceitos-chave
- **Deep Sleep:** 20 μA vs 80 mA = 4000x economia
- **D0→RST:** Conexão obrigatória para acordar
- **RTC memory:** 512 bytes que sobrevivem ao deep sleep
- **NTP inteligente:** Sincroniza 1 vez, calcula depois
- **Autonomia:** 3000 mAh → ~517 dias (1 leitura/hora)

### Gancho para próxima aula
> "E se ao acordar, o sensor precisasse tomar DECISÕES? → **Máquina de Estados Finitos (FSM)**"

---
*Criado em: 16/04/2026*
