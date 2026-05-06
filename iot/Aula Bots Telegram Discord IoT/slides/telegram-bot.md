<!DOCTYPE html>
<html lang="pt-BR">

<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no" />

  <title>IoT - Bots Telegram com ESP8266</title>

  <link rel="stylesheet" href="../../dist/reset.css" />
  <link rel="stylesheet" href="../../dist/reveal.css" />
  <link rel="stylesheet" href="../../dist/theme/dracula.css" />
  <link rel="stylesheet" href="../../dist/custom.css" />
  <link rel="stylesheet" href="../../plugin/highlight/monokai.css" />
</head>

<body>

  <div id="app" class="reveal">
    <div class="slides">


      <!-- SLIDE 1: CAPA -->
      <section data-auto-animate>
        <header1 aula="12" curso="Internet das Coisas" title-size="24" title="Bots Telegram com ESP8266">
          <p style="color: #8be9fd; font-size: 18pt;">NodeMCU v2</p>
        </header1>
      </section>

      <!-- SLIDE 2: O QUE E UM BOT -->
      <section data-auto-animate>
        <h2>O que e um Bot Telegram?</h2>
        <ul style="font-size: 20pt;">
          <li style="margin-bottom: 15px;">Programa que se comunica via Telegram automaticamente</li>
          <li style="margin-bottom: 15px;">Responde a comandos iniciados com <code>/</code></li>
          <li style="margin-bottom: 15px;">Pode enviar e receber mensagems de usuarios</li>
          <li style="margin-bottom: 15px;">Interage com hardware atraves da API HTTP do Telegram</li>
        </ul>
        <highlight-box>
          <p>Bots sao como assistentes virtuais que vivem dentro do Telegram e podem controlar dispositivos IoT</p>
        </highlight-box>
      </section>


      <!-- SECAO: COMO FUNCIONA -->
      <section>

        <!-- SLIDE 3: Secao - Como Funciona -->
        <section data-auto-animate>
          <h2 style="color: #8be9fd;">Como Funciona</h2>
        </section>

        <!-- SLIDE 4: Diagrama de Arquitetura -->
        <section data-auto-animate>
          <h2>Arquitetura do Sistema</h2>
          <div class="mermaid" data-id="architecture" style="width: 100%;">
            <pre>
%%init%% {"theme": "dark", "themeVariables": {"fontSize": "16px"}}
graph LR
  A["Usuario"] --|"comandos"| B["Telegram Bot API"]
  B --|"polling"| C["ESP8266"]
  C --|GP*| D["LED"]
  C --|GP*| E["DHT22"]

  style A fill:#44475a,color:#f8f8f2
  style B fill:#bd93f9,color:#282a36
  style C fill:#50fa7b,color:#282a36
  style D fill:#ff5555,color:#282a36
  style E fill:#ffb86c,color:#282a36
            </pre>
          </div>
        </section>

      </section><!-- fim Como Funciona -->


      <!-- SECAO: COMPONENTES NECESSARIOS -->
      <section>
        <!-- SLIDE 5: Secao - Componentes Necessarios -->
        <section data-auto-animate>
          <h2 style="color: #ff79c6;">Componentes Necessarios</h2>
        </section>

        <!-- SLIDE 6: Hardware e Software -->
        <section data-auto-animate>
          <h2>Hardware e Software</h2>
          <multi-col style="gap: 30px;">
            <div style="flex: 1;">
              <h4 style="color: #50fa7b;">Hardware</h4>
              <ul style="font-size: 18pt;">
                <li>NodeCMU ESP8266 v2</li>
                <li>Sensor DHT22</li>
                <li>LED</li>
                <li>Resistor 220 ohm</li>
                <li>Protoboard + jumpers</li>
              </ul>
            </div>
            <div style="flex: 1;">
              <h4 style="color: #bd93f9;">Software</h4>
              <ul style="font-size: 18pt;">
                <li>PlatformIO</li>
                <li>UniversalTelegramBot</li>
                <li>Telegram App</li>
                <li>BotFather</li>
              </ul>
            </div>
          </multi-col>
        </section>
      </section><!-- fim -->


      <!-- SECAO: CODIGO DO PROJETO -->
      <section>
        <!-- SLIDE 7: Secao - Codigo do Projeto -->
        <section data-auto-animate>
          <h2 style="color: #50fa7b;">Codigo do Projeto</h2>
        </section>

        <!-- SLIDE 8: platformio.ini -->
        <section data-auto-animate>
          <h2>platformio.ini</h2>
          <code-block lang="ini" data-trim>
          <textarea>
[env:nodemcvv2]
platform = espressif8266
board = nodemcuv2
framework = arduino

lib_deps =
    witnessmenow/Universal Arduino Telegram Bot
    bblanchon/ArduinoJson
    adafuit

monitor_speed = 115200
          </textarea>
          </code-block>
        </section>


        <!-- SLIDE 9: Codigo - Conexao WiFi e Definicoes -->
        <section data-auto-animate>
          <h2>Codigo: Conexao WiFi e Definicoes</h2>
          <code-block lang="cpp" data-line-numbers="1-21|1-4|6-10|12-14|16-21" data-fragment-index="1">
          <textarea>
#include &lt;Arduino.h&gt;
#include &lt;WiFiClientSecure.h&gt;
#include &lt;UniversalTelegramBot.h&gt;
#include &lt;DHT.h&gt;

#define WIFI_SSID "SUA_REDE"
#define WIFI_PASS "SUASENHA"
#define BOT_TOKEN "SEU_TOKEN"
#define LED_PIN 2
#define DHT_PIN D5
#define DHT_TYPE DHT22

WiFiClientSecure client;
UniversalTelegramBot bot(BOT_TOKEN, client);
DHT dht(DHT_PIN, DHT_TYPE);

void connectWiFi() {
  WiFi.begin(WIFI_SSID, WIFI_PASS);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println(" WiFi conectado!");
}
          </textarea>
          </code-block>
        </section>

        <!-- SLIDE 10: Codigo - handleNewMessages -->
        <section data-auto-animate>
          <h2>Codigo: handleNewMessages</h2>
          <code-block lang="cpp" data-line-numbers="1-23|2-5|6-8|9-12|13-16|17-22" data-fragment-index="1">
          <textarea>
void handleNewMessages(int numNewMessages) {
  for (int i = 0; i &lt; numNewMessages; i++) {
    String chat_id = bot.messages[i].chat_id;
    String text = bot.messages[i].text;

    if (text == "/start") {
      bot.sendMessage(chat_id,
        "Ola! Comandos: /ledon /ledoff /status");
    } else if (text == "/ledon") {
      digitalWrite(LED_PIN, HIGH);
      bot.sendMessage(chat_id, "LED ligado!");
    } else if (text == "/ledoff") {
      digitalWrite(LED_PIN, LOW);
      bot.sendMessage(chat_id, "LED desligado!");
    } else if (text == "/status") {
      float t = dht.readTemperature();
      float h = dht.readHumidity();
      String msg = "Temp: " + String(t) +
        " C | Umid: " + String(h) + "%";
      bot.sendMessage(chat_id, msg);
    }
  }
}
          </textarea>
          </code-block>
        </section>

        <!-- SLIDE 11: Codigo - setup e loop -->
        <section data-auto-animate>
          <h2>Codigo: setup() e loop()</h2>
          <code-block lang="cpp" data-trim data-line-numbers="1-16|2-6|8-16" data-fragment-index="1">
          <textarea>
void setup() {
  Serial.begin(115200);
  pinMode(LED_PIN, OUTPUT);
  dht.begin();
  client.setInsecure();
  connectWiFi();
}

void loop() {
  int numNewMessages = bot.getUpdates(
    bot.last_message_received + 1);
  while (numNewMessages) {
    handleNewMessages(numNewMessages);
    numNewMessages = bot.getUpdates(
      bot.last_message_received + 1);
  }
  delay(1000);
}
          </textarea>
          </code-block>
        </section>

      </section><!-- fim -->


      <!-- SLIDE 12: COMANDOS DO BOT -->
      <section data-auto-animate>
        <h2>Comandos do Bot</h2>
        <table style="font-size: 16pt; width: 100%;">
          <thead>
            <tr style="background: #44475a;">
              <th>Comando</th><th>Descricao</th><th>Acao</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td><code style="color: #50fa7b;">/start</code></td>
              <td>Inicia conversa</td>
              <td>Mensagem de boas-vindas</td>
            </tr>
            <tr>
              <td><code style="color: #50fa7b;">/status</code></td>
              <td>Status do dispositivo</td>
              <td>Temperatura e umidade</td>
            </tr>
            <tr>
              <td><code style="color: #50fa7b;">/ledon</code></td>
              <td>Liga LED</td>
              <td>GPIO2 HIGH</td>
            </tr>
            <tr>
              <td><code style="color: #50fa7b;">/ledoff</code></td>
              <td>Desliga LED</td>
              <td>GPIO2 LOW</td>
            </tr>
            <tr>
              <td><code style="color: #50fa7b;">/help</code></td>
              <td>Ajuda</td>
              <td>Lista de comandos</td>
            </tr>
          </tbody>
        </table>
        <copy-btn></copy-btn>
      </section>


      <!-- SLIDE 13: ATIVIDADE -->
      <section data-auto-animate>
        <h2>Atividade: Teste seu Bot!</h2>
        <ls-u font-size="18pt">
          <li>Crie um bot no Telegram via @BotFather (/newbot)</li>
          <li>Copie o token gerado pelo BotFather</li>
          <li>Configure platformio.ini com as bibliotecas necessarias</li>
          <li>Substitua WIFI_SSID, WIFI_PASS e BOT_TOKEN no codigo</li>
          <li>Monte o circuito: LED no GPIO2, DHT22 no D5</li>
          <li>Compile e envie o codigo para o NodeMCU</li>
          <li>Abra o Telegram e teste: /start, /ledon, /ledoff, /status</li>
        </ls-u>
      </section>

      <!-- SLIDE 14: RESUMO -->
      <section data-auto-animate>
        <h2>Resumo da Aula</h2>
        <ul style="font-size: 18pt;">
          <li style="margin-bottom: 10px;">Bots Telegram se comunicam via HTTP polling</li>
          <li style="margin-bottom: 10px;">ESP8266 usa WiFiClientSecure para conexao segura</li>
          <li style="margin-bottom: 10px;">UniversalTelegramBot simplifica a integracao</li>
          <li style="margin-bottom: 10px;">Comandos /ledon, /ledoff controlam GPIO</li>
          <li style="margin-bottom: 10px;">Sensor DHT22 envia dados via /status</li>
        </ul>
        <highlight-box>
          <p>Conceito-chave: O ESP8266 faz polling periodico ao Telegram Bot API para receber e processar mensagens dos usuarios</p>
        </highlight-box>
      </section>


    </div>
  </div>

  <script src="../../dist/reveal.js"></script>
  <script src="../../plugin/notes/notes.js"></script>
  <script src="../../plugin/math/math.js"></script>
  <script src="../../plugin/markdown/markdown.js"></script>
  <script src="../../plugin/highlight/highlight.js"></script>
  <script src="../../plugin/zoom/zoom.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/reveal.js-mermaid-plugin@49.2.2/plugin/mermaid/mermaid.js"></script>
  <script src="../../plugin/leader-line.min.js"></script>
  <script src="../../dist/vue.js"></script>
  <script src="../../slides_template/header1.js"></script>
  <script src="../../components/components.js"></script>
  <script src="../../slides_template/init.js"></script>

  <script>
    window.app = mountSlideApp();
  </script>

</body>
</html>
