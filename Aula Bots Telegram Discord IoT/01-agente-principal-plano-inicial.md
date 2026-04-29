# Plano de Aula: Bots Telegram e Discord para Comunicação com Dispositivos IoT

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

---

## 3. Conteúdo Programático

### 3.1 Arquitetura do Sistema (15 min)
- Visão geral: ESP8266 ↔ Internet ↔ Bot ↔ Usuário
- Comparação Telegram vs Discord para IoT
- Quando usar cada plataforma

### 3.2 Bot Telegram com ESP8266 (45 min)
- Criar bot via @BotFather
- Obter token de autenticação
- Biblioteca Universal Telegram Bot (Arduino)
- Comandos básicos: /status, /ledon, /ledoff, /temp
- Enviar dados de sensores para o chat
- Webhook vs Polling

### 3.3 Bot Discord com ESP8266 (45 min)
- Criar aplicação Discord no Developer Portal
- Configurar bot e obter token
- Usar biblioteca DiscordWebhook
- Webhooks Discord para envio de dados
- Comandos com prefixo "!"

### 3.4 Prática: Controlando LED via Telegram (30 min)
- Montar circuito LED no Protoboard
- Carregar código Arduino com bot Telegram
- Testar comandos via smartphone

### 3.5 Prática: Enviando dados de sensor para Discord (30 min)
- Conectar sensor DHT22 (temperatura/umidade)
- Configurar webhook Discord
- Visualizar dados em canal do Discord

### 3.6 Projeto Integrador (15 min)
- Descrição do projeto: Sistema de monitoramento ambiental completo
- Requisitos:ESP8266 + DHT22 + LED + Bot Telegram/Discord
- Entrega: código funcional + documentação

---

## 4. Recursos Necessários

### Hardware
- NodeMCU ESP8266 (1 por dupla)
- LED (1 por dupla)
- Sensor DHT22 (temperatura/umidade) - 1 por dupla
- Protoboard
- Resistores 220Ω
- Jumpers

### Software
- Arduino IDE com placas ESP8266
- Biblioteca Universal Telegram Bot
- Biblioteca DHT sensor
- Conta Telegram (para criar bot)
- Conta Discord (para criar webhook)

### Materiais de Apoio
- Slides disponíveis em: `reveal-cpvbcdd-202501/`
- Código fonte: `codigos/`

---

## 5. Metodologia

1. **Aula expositiva-dialogada** com demonstrações práticas
2. **Aprendizagem baseada em projetos** com problema real
3. **Trabalho em duplas** para maior interação
4. **Coffee break** de 10 min no meio da aula

---

## 6. Avaliação

- Participação nas atividades práticas (2 pontos)
- Entrega do projeto integrador funcionando (5 pontos)
- Documentação do código (3 pontos)

---

## 7. Cronograma

| Tempo | Atividade |
|-------|-----------|
| 0:00 - 0:15 | Apresentação da arquitetura e objetivos |
| 0:15 - 1:00 | Telegram Bot - teoria e demonstração |
| 1:00 - 1:10 | Coffee break |
| 1:10 - 1:55 | Discord Bot - teoria e demonstração |
| 1:55 - 2:25 | Prática Telegram - LED |
| 2:25 - 2:55 | Prática Discord - Sensor DHT |
| 2:55 - 3:10 | Projeto integrador e encerramento |

---

## 8. Referências

- [Universal Telegram Bot Library](https://github.com/witnessmenow/Universal-Arduino-Telegram-Bot)
- [Discord Webhooks Guide](https://discord.com/developers/docs/resources/webhook)
- [ESP8266 Telegram Bot Tutorial](https://randomnerdtutorials.com/telegram-control-esp32/)
- NodeMCU ESP8266 datasheet

---

*Plano criado em: 2026-04-29*
*Agente: Aria (Orchestrator)*