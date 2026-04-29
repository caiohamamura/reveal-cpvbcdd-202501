# Plano de Aula v2 — Bots Telegram e Discord para IoT com ESP8266

*Versão atualizada com base nas avaliações pedagógicas e tecnológicas*

## Mudanças Implementadas

### Pedagógicas (Professor Especialista)
1. ✅ Adicionado objetivo actitudinal
2. ✅ Adicionada micro-demo穿插 na teoria
3. ✅ Adicionada seção de segurança (tokens, validação)
4. ✅ Adicionado checkpoint de progresso
5. ✅ Adicionado diagrama de arquitetura

### Tecnológicas (Consultor Moderno)
1. ✅ WiFiManager para autoconfiguração
2. ✅ Error handling com retry para Discord
3. ✅ Tokens via platformio.ini (não hardcoded)
4. ✅ Código de exemplo testado

---

## 1. Identificação

- **Tema:** Bots Telegram e Discord para comunicação com dispositivos IoT na prática com NodeMCU ESP8266
- **Disciplina:** IoT - Internet das Coisas
- **Curso:** Técnico Integrado em Informática para Internet
- **Duração:** 3 horas (aula prática)
- **Pré-requisitos:** Conhecimento básico de Arduino, noções de comunicação HTTP/MQTT, NodeMCU ESP8266

---

## 2. Objetivos

### Objetivo Geral
Capacitar os alunos a criar bots de Telegram e Discord que se comunicam com dispositivos IoT baseados em NodeMCU ESP8266, permitindo monitoramento e controle remoto em tempo real.

### Objetivos Específicos
1. Compreender a arquitetura de bots Telegram e Discord para IoT
2. Configurar um bot Telegram usando a Bot API
3. Configurar um bot Discord usando a Discord API
4. Implementar comunicação bidirecional entre ESP8266 e bots
5. Criar um dashboard básico de monitoramento via chat
6. Integrar sensores e atuadores com comandos de chat

### Objetivos Atitudinais
7. Desenvolver autonomia para resolver problemas de comunicação IoT
8. Praticar boas práticas de segurança no armazenamento de tokens e credenciais

---

## 3. Diagrama da Arquitetura

```
┌─────────────┐     WiFi      ┌─────────────┐     HTTPS      ┌─────────────┐
│  NodeMCU    │◄────────────►│   Internet  │◄────────────►│  Telegram/  │
│  ESP8266    │              │             │              │  Discord    │
│             │              │             │              │   Server    │
│  Sensores   │              │             │              │             │
│  - DHT22    │              │             │              │             │
│  - LED      │              │             │              │             │
└─────────────┘              └─────────────┘              └─────────────┘
                                                              │
                                                              ▼
                                                      ┌─────────────┐
                                                      │   Usuário   │
                                                      │  (Chat App) │
                                                      └─────────────┘
```

---

## 4. Conteúdo Programático

### 4.1 Arquitetura do Sistema (15 min)
- Visão geral: ESP8266 ↔ Internet ↔ Bot ↔ Usuário
- Comparação Telegram vs Discord para IoT
- Quando usar cada plataforma
- Diagrama de arquitetura no quadro

### 4.2 Segurança em Bots IoT (10 min) ⭐ NOVO
- **NUNCA** exponha tokens no código versionado
- Usar WiFiManager para credenciais WiFi
- Tokens da API em arquivo separado (platformio.ini ou secrets.h)
- Validação de comandos recibidos

### 4.3 Bot Telegram com ESP8266 (40 min)
- Criar bot via @BotFather
- Obter token de autenticação
- Biblioteca Universal Telegram Bot (Arduino)
- Comandos básicos: /start, /status, /ledon, /ledoff, /temp
- **Demo ao vivo**: Professor mostra bot respondendo
- Webhook vs Polling (explicar diferenças)
- **WiFiManager**: autoconfiguração de rede

### 4.4 Bot Discord com ESP8266 (40 min)
- Criar aplicação Discord no Developer Portal
- Configurar webhook e obter URL
- Enviar dados via Webhook Discord (HTTP POST)
- Comandos com prefixo "!"
- **Error handling**: retry 3x com intervalo 1s
- **Demo ao vivo**: Professor envia temperatura para canal Discord

### 4.5 Coffee Break (10 min)

### 4.6 Prática: Controlando LED via Telegram (25 min)
- Montar circuito LED no Protoboard
- Configurar WiFi via WiFiManager
- Carregar código com bot Telegram
- Testar comandos via smartphone
- **Checkpoint**: Cada dupla demonstra /ledon e /ledoff funcionando

### 4.7 Prática: Enviando dados de sensor para Discord (25 min)
- Conectar sensor DHT22 (temperatura/umidade)
- Configurar webhook Discord
- Visualizar dados em canal do Discord
- **Checkpoint**: Cada dupla demonstra mensagem no Discord

### 4.8 Projeto Integrador (15 min)
- Descrição: Sistema de monitoramento ambiental completo
- Requisitos:
  - ESP8266 + DHT22 + LED
  - Bot Telegram para controle (liga/desliga LED)
  - Bot Discord para monitoramento (envia temperatura a cada 30s)
  - WiFiManager para configuração
- **Entrega**: código funcional + documentação no README.md

---

## 5. Recursos Necessários

### Hardware (1 kit por dupla)
- NodeMCU ESP8266 (1 por dupla)
- LED (1 por dupla)
- Sensor DHT22 (temperatura/umidade)
- Protoboard
- Resistores 220Ω
- Jumpers

### Software
- Arduino IDE ou PlatformIO
- Biblioteca Universal Telegram Bot
- Biblioteca DHT sensor
- Biblioteca WiFiManager
- Conta Telegram (para criar bot)
- Conta Discord (para criar webhook)

### Materiais de Apoio
- Slides: `reveal-cpvbcdd-202501/bots-telegram-discord-iot.html`
- Código fonte: `codigos/telegram-bot/` e `codigos/discord-webhook/`

---

## 6. Checklist de Segurança ⚠️

Antes de começar, verificar com os alunos:
- [ ] Tokens NÃO estão no código fonte
- [ ] WiFi credentials via WiFiManager
- [ ] Código compila sem warnings

---

## 7. Metodologia

1. **Aula expositiva-dialogada** com demonstrações práticas ao vivo
2. **Aprendizagem baseada em projetos** com problema real
3. **Trabalho em duplas** para maior interação
4. **Checkpoint de progresso** ao final de cada prática
5. **Coffee break** de 10 min no meio da aula

---

## 8. Avaliação

| Item | Pontos |
|------|--------|
| Participação nas atividades práticas | 2 pts |
| Checkpoint Telegram (LED funcionando) | 1.5 pts |
| Checkpoint Discord (DHT enviando dados) | 1.5 pts |
| Entrega do projeto integrador | 3 pts |
| Documentação (README.md) | 2 pts |
| **Total** | **10 pts** |

---

## 9. Cronograma

| Tempo | Atividade | Responsável |
|-------|-----------|-------------|
| 0:00 - 0:10 | Apresentação + diagrama arquitetura | Professor |
| 0:10 - 0:20 | Segurança em bots IoT | Professor |
| 0:20 - 1:00 | Telegram Bot - teoria + demo | Professor |
| 1:00 - 1:10 | Coffee break | - |
| 1:10 - 1:50 | Discord Bot - teoria + demo | Professor |
| 1:50 - 2:15 | Prática Telegram - LED | Alunos |
| 2:15 - 2:20 | **Checkpoint Telegram** | Professor |
| 2:20 - 2:45 | Prática Discord - Sensor DHT | Alunos |
| 2:45 - 2:50 | **Checkpoint Discord** | Professor |
| 2:50 - 3:10 | Projeto integrador + encerramento | Professor |

---

## 10. Código Fonte (PlatformIO)

### Estrutura de diretórios
```
codigos/
├── telegram-bot/
│   ├── platformio.ini
│   ├── src/
│   │   ├── main.cpp
│   │   └── secrets.h.example
│   └── README.md
└── discord-webhook/
    ├── platformio.ini
    ├── src/
    │   ├── main.cpp
    │   └── secrets.h.example
    └── README.md
```

---

## 11. Referências

- [Universal Telegram Bot Library](https://github.com/witnessmenow/Universal-Arduino-Telegram-Bot)
- [Discord Webhooks Guide](https://discord.com/developers/docs/resources/webhook)
- [WiFiManager Library](https://github.com/tzapu/WiFiManager)
- [ESP8266 Telegram Bot Tutorial](https://randomnerdtutorials.com/telegram-control-esp32/)
- NodeMCU ESP8266 datasheet

---

*Plano v2 criado em: 2026-04-29*
*Atualizações: Avaliações pedagógicas + tecnológicas incorporadas*