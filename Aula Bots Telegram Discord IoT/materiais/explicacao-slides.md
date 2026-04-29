# Explicação da Aula: Bots Telegram e Discord para IoT com ESP8266

*Material de apoio para alunos — acompanhe antes, durante e depois da aula*

---

## 📌 O que você vai aprender hoje

Hoje vamos aprender a fazer seu NodeMCU ESP8266 "conversar" com você pelo celular! Você vai criar bots no Telegram e Discord que:

- **Envia dados** do sensor (temperatura, umidade) para seu celular
- **Permite controlar** LEDs e atuadores apenas mandando uma mensagem

---

## 📖 Glossário de Termos Técnicos

Antes de começar, aqui estão os termos que você vai encontrar:

| Termo | O que é | Analogia |
|-------|---------|----------|
| **Token** | Chave de autenticação do bot (como uma senha API) | Chave do portão eletrônico |
| **GPIO** | General Purpose Input/Output - pinos físicos do microcontrolador | Tomadas na parede |
| **D0, D1, D2...** | Labels no NodeMCU que mapeiam para GPIOs | Etiquetas nas tomadas |
| **JSON** | Formato de dados texto para trocar informações | Caixa de correio com formato padrão |
| **HTTP POST** | Método de enviar dados para um servidor | Colocar uma carta no correio |
| **HTTP GET** | Método de pedir dados a um servidor | Pedir informações por telefone |
| **Polling** | Técnica de "perguntar" repetidamente se há novas mensagens | Ligar pra empresa perguntando "chegou?" |
| **Webhook** | Técnica de receber notificações push (o servidor avisa você) | Notificação no celular quando chega msg |
| **Pull-up resistor** | Resistor que mantém um sinal em HIGH quando nenhum dispositivo está ativo | Sprinkler que mantém pressão na tubulação |
| **WiFiClientSecure** | Cliente que se conecta via HTTPS (SSL/TLS) | Carta com selo e envelope fechado |
| **setInsecure()** | Aceita certificados não verificados (para testes) | Confiar em qualquer pessoa (não faça em produção!) |
| **DHT22** | Sensor de temperatura e umidade digital | Termômetro inteligente |
| **isnan()** | "is Not A Number" - verifica se valor é inválido | "Isso é um número válido?" |
| **Servidor** | Programa que fica esperando requests e serve dados | Restaurante 24h |
| **Cliente** | Programa que faz requests a um servidor | Você pedindo delivery |

---

## 🏠 Cliente vs Servidor — Quem é quem?

```
┌─────────────────────────────────────────────────────────────────────┐
│                    CLIENTE vs SERVIDOR                                │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  SERVIDOR = "O cara que fica esperando e servindo"                   │
│             - Fica ligado 24h                                       │
│             - Espera requests (pedidos)                              │
│             - Exemplo: Telegram, Google, Discord                    │
│                                                                      │
│  CLIENTE  = "O cara que pede coisas ao servidor"                    │
│             - Só conecta quando precisa                             │
│             - Faz perguntas (GET) ou envia dados (POST)              │
│             - Exemplo: Seu navegador, seu ESP8266                    │
│                                                                      │
│  ┌──────────┐          request          ┌──────────┐               │
│  │  CLIENTE  │ ───────────────────────►│ SERVIDOR │                 │
│  │  (você)   │                           │ (Telegram)│                 │
│  │          │◄─────────────────────── │          │                 │
│  └──────────┘          response         └──────────┘                 │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

**No nosso projeto:**
- **ESP8266 = Cliente** (você programa ele)
- **Telegram/Discord = Servidor** (eles já existem)

---

## 🔌 GPIO vs D4 — Qual a diferença?

```
┌─────────────────────────────────────────────────────────────────────┐
│                    NodeMCU ESP8266 - Nomenclatura                    │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  GPIO = General Purpose Input/Output                                 │
│         ├─ São os pinos físicos do chip                             │
│         └─ Cada GPIO tem um número (0, 1, 2, 3, 4...)               │
│                                                                      │
│  D0, D1, D2... = Labels no NodeMCU (mapeamento físico)              │
│         ├─ D0 = GPIO16                                              │
│         ├─ D1 = GPIO5                                               │
│         ├─ D2 = GPIO4                                               │
│         ├─ D3 = GPIO0                                               │
│         ├─ D4 = GPIO2 (com LED interno!)                            │
│         └─ RX = GPIO3, TX = GPIO1                                   │
│                                                                      │
│  ⚠️ No código Arduino, use GPIO numbers (0, 2, 4...)               │
│     Os labels D* são só para referência visual no hardware            │
│                                                                      │
│  Tabela rápida:                                                     │
│  ┌────────┬────────┐                                                  │
│  │ Label  │ GPIO   │                                                  │
│  ├────────┼────────┤                                                  │
│  │ D0     │ 16     │                                                  │
│  │ D1     │ 5      │                                                  │
│  │ D2     │ 4      │                                                  │
│  │ D3     │ 0      │                                                  │
│  │ D4     │ 2      │                                                  │
│  │ D5     │ 14     │                                                  │
│  │ D6     │ 12     │                                                  │
│  │ D7     │ 13     │                                                  │
│  │ D8     │ 15     │                                                  │
│  └────────┴────────┘                                                  │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 1. Arquitetura do Sistema — Como tudo se conecta?

### O fluxo completo:
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
                                                      │   Você!    │
                                                      │  (celular) │
                                                      └─────────────┘
```

### Traduzindo para o português:

1. **ESP8266** lê sensores (ex: temperatura do DHT22)
2. **ESP8266** se conecta ao Wi-Fi e manda dados para a Internet
3. **Servidor do Telegram/Discord** recebe e mostra no seu celular
4. **Você** pode enviar comandos de volta (ex: "liga LED")

### Analogia do restaurante:

Pense como se fosse um **restaurante delivery**:
- Você (cliente) = seu celular
- Restaurante = servidor Telegram/Discord
- Entregador = Internet
- Cozinha = ESP8266 com sensores

Você liga pro restaurante pedindo info sobre a comida (pedido). O restaurante comunica com a cozinha, que prepara e devolve. Você também pode pedir para modificar algo.

---

## 2. Segurança em Bots IoT — ⚠️ MUITO IMPORTANTE!

### ❌ O que NÃO fazer:

```cpp
// ❌ NUNCA FAÇA ISSO!
const char* botToken = "1234567890:ABCdefGHIjklMNOpqrsTUVwxyz";
const char* wifiPassword = "minhasenha123";
```

**Problemas:**
1. Se você commitar esse código no GitHub, qualquer pessoa verá seu token
2. Bots podem ser usados por outros (e você paga a conta!)
3. Credenciais expostas = acesso não autorizado

### ✅ O que FAZER:

**1. Usar arquivo separado (secrets.h):**
```cpp
// secrets.h - NUNCA commitar este arquivo!
#define BOT_TOKEN "1234567890:ABCdefGHIjkl"
#define WIFI_SSID "MinhaRede"
#define WIFI_PASS "minhasenha123"
```

**2. No .gitignore:**
```
secrets.h
```

**3. Usar WiFiManager (mais prático):**
- Na primeira vez, o ESP8266 cria um Wi-Fi "ESP8266-Config"
- Você conecta, abre o navegador, e coloca a senha do Wi-Fi
- Ele salva e conecta automaticamente depois

---

## 3. Bot Telegram — Criando seu primeiro bot

### Passo a passo:

#### 3.1 Criar o bot no Telegram:

1. Abra o Telegram e pesquise: **@BotFather**
2. Mande: `/newbot`
3. Dê um nome: `MeuIoT_Bot`
4. Dê um username (tem que acabar em "bot"): `meu_iot_caio_bot`
5. **IMPORTANTE**: Copie o token que ele mostrar!

#### 3.2 Bibliotecas necessárias:

```
Universal Telegram Bot Library
WiFiManager
DHT sensor library
ArduinoJson (para processar mensagens)
```

#### 3.3 Comandos básicos:

| Comando | O que faz |
|---------|-----------|
| `/start` | Inicia a conversa |
| `/status` | Mostra status do ESP8266 |
| `/ledon` | Liga o LED |
| `/ledoff` | Desliga o LED |
| `/temp` | Envia temperatura atual |

#### 3.4 Código simplificado:

```cpp
#include <UniversalTelegramBot.h>
#include <WiFiClientSecure.h>

// Seu token do BotFather
#define BOT_TOKEN "SEU_TOKEN_AQUI"

// Códigos dos comandos
void handleNewMessages(TBOTMessage messages[]) {
  for (int i = 0; i < messages[i].text != ""; i++) {
    String chat_id = messages[i].chat_id;
    String text = messages[i].text;
    
    if (text == "/ledon") {
      digitalWrite(LED_PIN, HIGH);
      bot.sendMessage(chat_id, "LED ligado! 💡");
    }
    else if (text == "/ledoff") {
      digitalWrite(LED_PIN, LOW);
      bot.sendMessage(chat_id, "LED desligado! 🔴");
    }
    else if (text == "/temp") {
      float temp = dht.readTemperature();
      bot.sendMessage(chat_id, "Temperatura: " + String(temp) + "°C");
    }
  }
}
```

### Webhook vs Polling:

| Método | Como funciona | Quando usar |
|--------|---------------|-------------|
| **Polling** | ESP8266 "pergunta" ao Telegram a cada X segundos | Simples, funciona sempre |
| **Webhook** | Telegram avisa quando há mensagem | Mais eficiente, precisa URL pública |

**Nosso projeto usa Polling** (mais fácil para testes em sala).

---

## 🤔 HTTP POST vs GET — Como enviar dados?

Você já sabe que o ESP8266 se comunica via HTTP. Mas existem diferentes "tipos" de comunicação:

```
┌─────────────────────────────────────────────────────────────────────┐
│                         ANALOGIA CORREIO                             │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  GET  = Pedir uma carta (você pede, servidor devolve)              │
│         "Quero saber a temperatura atual" → servidor responde      │
│                                                                      │
│  POST = Enviar uma carta (você envia dados, servidor recebe)       │
│         "Aqui está a temperatura: 25°C" → servidor registra          │
│                                                                      │
│  PUT  = Atualizar algo existente                                    │
│         "Atualize o LED para LIGADO" → servidor atualiza           │
│                                                                      │
│  DELETE = Remover algo                                              │
│         "Apague o registro" → servidor remove                      │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

**No nosso projeto:**
- Telegram usa GET (para verificar mensagens) e POST (para enviar respostas)
- Discord usa apenas POST (para enviar dados para o webhook)

### Por que o Discord usa POST?

Porque você está **"enviando"** dados para o Discord, não pedindo. O Discord não tem como "perguntar" pro seu ESP, então seu ESP é quem empurra os dados.

---

## 🔄 Polling vs Webhook — Duas formas de receber mensagens

```
┌─────────────────────────────────────────────────────────────────────┐
│                         POLLING (nosso projeto)                      │
├─────────────────────────────────────────────────────────────────────┤
│  ESP8266                          Telegram Server                   │
│    │                                  │                              │
│    │ ─────── "Tem mensagem?" ────────►│                              │
│    │◄─────── "Não"                    │                              │
│    │                                  │                              │
│    │ (repete a cada 1 segundo)       │                              │
│    │                                  │                              │
│    │ ─────── "Tem mensagem?" ────────►│                              │
│    │◄─────── "SIM! /ledon"            │                              │
│    │                                  │                              │
│    │ (processa comando)               │                              │
└─────────────────────────────────────────────────────────────────────┘

✅ Vantagens: Funciona em redes NAT, não precisa IP público
❌ Desvantagens: Delay de até 1s, gasta mais energia Wi-Fi
```

```
┌─────────────────────────────────────────────────────────────────────┐
│                         WEBHOOK (alternativa)                       │
├─────────────────────────────────────────────────────────────────────┤
│  ESP8266                          Telegram Server                   │
│    │                                  │                              │
│    │◄─── "Nova mensagem: /ledon" ─────│  (Telegram avisa você!)      │
│    │                                  │                              │
│    │ (precisa URL pública ou ngrok)  │                              │
└─────────────────────────────────────────────────────────────────────┘

✅ Vantagens: Resposta instantânea, menor consumo de energia
❌ Desvantagens: Precisa URL pública, configuração mais complexa
```

**Por que usamos Polling?**
- Mais simples de implementar
- Funciona na rede do IFSP (sem IP público)
- Biblioteca pronta (UniversalTelegramBot)

---

## 📊 Comparação: Telegram vs Discord para IoT

| Feature | Telegram Bot | Discord Webhook |
|---------|--------------|----------------|
| **Biblioteca Arduino** | ✅ UniversalTelegramBot | ❌ Manual (HTTP) |
| **Receber comandos** | ✅ Nativo (/comando) | ⚠️ Parcial (prefixo !) |
| **Enviar notificações** | ✅ Nativo | ✅ Nativo |
| **Autenticação** | ✅ chat_id validation | ❌ Qualquer pessoa com URL |
| **Rate limit** | 30 msg/segundo | 30 requests/60s por webhook |
| **Custo** | Grátis | Grátis |
| **Facilidade setup** | Médio | Fácil |
| **Melhor para** | **Controle interativo** | **Notificações simples** |

**Quando usar cada um:**
- **Telegram**: Quando você quer **controlar** dispositivos (mandar comandos)
- **Discord**: Quando você só quer **monitorar** (ver dados no canal)

---

## 4. Bot Discord — Enviando dados para um canal

### Vantagens do Discord para IoT:

- **Gratuito** e sem limite de mensagens
- **Visual bonito** com embeds自动格式化
- **Grupos** para organizar projetos
- **Notificações** no celular

### Passo a passo:

#### 4.1 Criar webhook no Discord:

1. Abra Discord > Server Settings > Webhooks
2. Crie novo webhook: `IoT_Sensores`
3. Copie a **Webhook URL**

#### 4.2 Enviar dados via HTTP POST:

```cpp
#include <ESP8266HTTPClient.h>

// URL do webhook (substitua pelo seu)
String discordWebhookURL = "https://discord.com/api/webhooks/SEU_WEBHOOK";

void sendToDiscord(String message) {
  HTTPClient http;
  http.begin(httpRequest);
  http.addHeader("Content-Type", "application/json");
  
  // Formato JSON para Discord
  String payload = "{\"content\": \"" + message + "\"}";
  int httpCode = http.POST(payload);
  
  // Error handling: retry 3x
  if (httpCode != 200) {
    delay(1000); // espera 1s
    httpCode = http.POST(payload); // tenta de novo
  }
  
  http.end();
}

// Uso:
sendToDiscord("🌡️ Temperatura: 25.3°C | Umidade: 65%");
```

### Error Handling (tratar erros):

```cpp
void sendToDiscord(String message) {
  HTTPClient http;
  http.begin(discordWebhookURL);
  http.addHeader("Content-Type", "application/json");
  
  String payload = "{\"content\": \"" + message + "\"}";
  
  // Retry 3 vezes
  int httpCode = -1;
  for (int retry = 0; retry < 3; retry++) {
    httpCode = http.POST(payload);
    if (httpCode == 200) break;
    delay(1000); // espera 1s entre tentativas
  }
  
  if (httpCode != 200) {
    Serial.println("Falha ao enviar: " + String(httpCode));
  }
  
  http.end();
}
```

---

## 5. WiFiManager — Diga adeus às senhas hardcoded

### O problema:

Todo mundo já passou raiva configurando Wi-Fi em projetos IoT:
- "E se eu mudar de rede?"
- "E se拿去 para outra sala?"
- "Preciso reprogramar só pra trocar a senha?"

### A solução: WiFiManager

Com o WiFiManager, na primeira vez:
1. ESP8266 inicia como **access point** (cria um Wi-Fi)
2. Você conecta do celular/computador
3. Abre um portal web e digita a senha do Wi-Fi
4. ESP8266 salva e conecta automaticamente!

### Código:

```cpp
#include <ESP8266WiFi.h>
#include <WiFiManager.h>

void setup() {
  Serial.begin(115200);
  
  // WiFiManager: cria portal de configuração
  WiFiManager wifiManager;
  
  // Tenta conectar. Se não conseguir, cria portal.
  if (!wifiManager.autoConnect("ESP8266_IoT")) {
    Serial.println("Falha ao conectar. Portal criado!");
    // Reset ESP8266
    ESP.reset();
  }
  
  Serial.println("Wi-Fi conectado!");
}
```

### Fluxo visual:

```
┌─────────────────────────────────────────────┐
│  Primeira vez:                              │
│  1. ESP8266 não conecta → cria AP           │
│  2. "ESP8266_IoT" aparece no celular         │
│  3. Você conecta e abre portal              │
│  4. Digita: rede "MinhaCasa" + senha        │
│  5. ESP8266 salva e conecta! ✅             │
├─────────────────────────────────────────────┤
│  Próximas vezes:                            │
│  1. ESP8266 conecta automaticamente! ✅     │
└─────────────────────────────────────────────┘
```

---

## 6. Prática 1 — Controlando LED via Telegram

### Componentes necessários:

| Componente | Pino no ESP8266 |
|------------|-----------------|
| LED | D4 (GPIO 2) |
| Resistor 220Ω | - |
| Protoboard | - |

### Circuito:

```
ESP8266          Protoboard
  D4 ──── jumper ──── resistor 220Ω ──── LED ──── GND
```

### Verificação no checkpoint:

Você vai demonstrar para o professor:
1. Mandar `/ledon` → LED acende
2. Mandar `/ledoff` → LED apaga
3. Mandar `/status` → Mostra IP e status

---

## 7. Prática 2 — Enviando dados de sensor para Discord

### Componentes necessários:

| Componente | Pino no ESP8266 |
|------------|-----------------|
| DHT22 (temperatura/umidade) | D3 (GPIO 0) |
| Resistor 10KΩ (pull-up) | entre DATA e VCC |

### Circuito DHT22:

```
ESP8266          DHT22
  3.3V  ──── VCC (1)
  GND   ──── GND (4)
  D3    ──── DATA (2)
              │
         resistor 10KΩ
              │
         VCC (1)
```

### Código básico:

```cpp
#include <DHT.h>
#define DHT_PIN 0 // GPIO 0 = D3
#define DHT_TYPE DHT22
DHT dht(DHT_PIN, DHT_TYPE);

void loop() {
  float temp = dht.readTemperature();
  float humidity = dht.readHumidity();
  
  if (!isnan(temp)) {
    String msg = "🌡️ Temp: " + String(temp) + "°C";
    msg += " | 💧 Umidade: " + String(humidity) + "%";
    sendToDiscord(msg);
  }
  
  delay(30000); // a cada 30 segundos
}
```

### Verificação no checkpoint:

Você vai demonstrar para o professor:
1. Mensagem aparecendo no canal Discord
2. Dados de temperatura e umidade
3. Intervalo de 30 segundos funcionando

---

## 8. Projeto Integrador — Desafio final!

### Requisitos obrigatórios:

- [ ] ESP8266 + DHT22 + LED
- [ ] Bot Telegram para controle (liga/desliga LED)
- [ ] Bot Discord para monitoramento (envia temperatura a cada 30s)
- [ ] WiFiManager para configuração de rede
- [ ] Código comentado e documentado no README.md

### Estrutura do projeto:

```
projeto-integrador/
├── platformio.ini          # Configurações PlatformIO
├── src/
│   ├── main.cpp           # Código principal
│   └── secrets.h         # Tokens (NÃO commitar!)
├── README.md             # Documentação
└── .gitignore            # Ignorar secrets.h
```

### Funcionalidades esperadas:

| Funcionalidade | Comando/Comportamento |
|----------------|----------------------|
| Liga LED | `/ledon` via Telegram |
| Desliga LED | `/ledoff` via Telegram |
| Ver temperatura | `/temp` via Telegram |
| Ver status | `/status` via Telegram |
| Envio automático | A cada 30s para Discord |

---

## 9. Erros Comuns e Como Resolver

Esta é a seção mais importante da aula! Se der problema, volte aqui primeiro.

| Erro | Sintoma | Solução |
|------|---------|---------|
| **Bot não responde** | Manda `/start` e nada acontece | 1) Verificar token está correto 2) Verificar Wi-Fi conectado 3) Mandar `/start` novamente 4) Verificar Serial Monitor |
| **LED não acende** | Comando enviado mas nada acontece | 1) Verificar GPIO correto no código 2) Verificar LED com polaridade certa (perna longa = +) 3) Verificar resistor 220Ω 4) Testar LED direto no 3.3V |
| **Discord não recebe mensagem** | Webhook parece não funcionar | 1) Verificar URL do webhook está completa 2) Verificar formato JSON 3) Verificar permissões do canal 4) Testar com curl ou Postman |
| **DHT22 retorna NaN** | Sensor não lê nada | 1) Verificar conexões VCC(3.3V), GND, DATA(D3) 2) Adicionar resistor 10K entre DATA e VCC 3) Trocar por DHT11 pra testar 4) Verificar biblioteca instalada |
| **WiFiManager não cria AP** | ESP não aparece como rede Wi-Fi | 1) Pressionar botão RST 2) Verificar biblioteca WiFiManager instalada 3) Abrir Serial Monitor (115200) 4) Aguardar 10s |
| **ESP reseta sozinho** | Reinicia inesperadamente | 1) Verificar fonte (5V 500mA mínimo) 2) Verificar regulator de voltagem 3) Cabo USB com qualidade 4) Desconectar e reconectar |
| **setInsecure() erro** | Erro de certificado SSL | Para testes: usar `setInsecure()` (confia qualquer certificado) Produção: usar certificado válido |
| **Rate limit Discord** | Mensagens param de chegar | 1) Aguardar 60 segundos 2) Implementar buffer/agregador 3) Reduzir frequência de envio |
| **"Wi-Fi desconectado"** | ESP para de funcionar | 1) Verificar sinal Wi-Fi 2) Implementar lógica de reconnection 3) Verificar SSID e senha |
| **Código não compila** | Erros no Arduino IDE | 1) Selecionar placa "NodeMCU 1.0" 2) Verificar bibliotecas instaladas 3) Verificar platformio.ini |

### Checklist de Debugging (seguir em ordem):

```
1. Wi-Fi
   ├─ [ ] ESP está conectado? (Serial Monitor mostra IP)
   └─ [ ] Sinal Wi-Fi está forte?

2. Telegram Bot
   ├─ [ ] Token está correto?
   ├─ [ ] Bot recebeu `/start`?
   └─ [ ] `/status` retorna algo?

3. Discord Webhook
   ├─ [ ] URL do webhook está completa?
   ├─ [ ] Canal ainda existe?
   └─ [ ] Testou manualmente?

4. Hardware
   ├─ [ ] LED funciona (teste direto)?
   ├─ [ ] DHT22 conectado corretamente?
   └─ [ ] Cabos jumpers OK?
```

---

## 10. Dúvidas Comuns (Rápido)

### "O bot não responde!"
1. Verifique se o token está correto
2. Verifique se o ESP8266 está conectado ao Wi-Fi
3. Teste:mandar `/start` novamente

### "Mensagem não aparece no Discord!"
1. Verifique se a webhook URL está correta
2. Teste manualmente pelo Discord (Settings > Webhooks > View Webhooks)
3. Verifique se o canal existe e você tem permissão

### "DHT22 não lê temperatura!"
1. Verifique as conexões (VCC, GND, DATA)
2. Adicione resistor pull-up de 10K entre DATA e VCC
3. Teste com código simples primeiro

### "WiFiManager não cria a rede!"
1. Reset ESP8266 (pressione o botão RST)
2. Verifique se a biblioteca está instalada
3. Verifique serial monitor (115200 baud)

---

## 10. Referências e Links Úteis

### Documentação:
- [Universal Telegram Bot Library](https://github.com/witnessmenow/Universal-Arduino-Telegram-Bot)
- [WiFiManager Library](https://github.com/tzapu/WiFiManager)
- [Discord Webhooks Guide](https://discord.com/developers/docs/resources/webhook)
- [ESP8266 Arduino Core](https://arduino-esp8266.readthedocs.io/)

### Tutoriais:
- [Random Nerd Tutorials - Telegram ESP32](https://randomnerdtutorials.com/telegram-control-esp32/)
- [Random Nerd Tutorials - ESP8266 DHT22](https://randomnerdtutorials.com/esp8266-dht11-dht22-temperature-humidity-arduino/)

### Playground:
- [BotFather Telegram](https://t.me/botfather)
- [Discord Developer Portal](https://discord.com/developers/applications)

---

## Resumo Rápido (para revisão antes da prova)

| Conceito | O que faz |
|----------|-----------|
| **Telegram Bot** | Recebe comandos e envia respostas via chat |
| **Discord Webhook** | Envia dados para canal automaticamente |
| **WiFiManager** | Permite configurar Wi-Fi via portal web |
| **Polling** | ESP8266 pergunta ao servidor se há mensagens |
| **secrets.h** | Arquivo seguro para tokens e senhas |

---

*Material criado para acompanhar os slides da aula.*
*Última atualização: 2026-04-29*
