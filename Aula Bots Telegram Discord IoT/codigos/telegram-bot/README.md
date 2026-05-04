# 🤖 Bot Telegram para NodeMCU ESP8266 v5

Bot Telegram para controle de LED e leitura de sensor DHT22 via Wi-Fi.
Usa **AsyncTelegram2** com inline keyboards para controle interativo.

## 📋 Comandos e Botões

| Comando/Botão | Descrição |
|----------------|-----------|
| `/start` | Mensagem de boas-vindas com teclado inline |
| `/help` | Lista de comandos |
| `/status` | Lê temperatura e umidade do DHT22 |
| 💡 LED ON | Liga o LED (botão inline) |
| ⚫ LED OFF | Desliga o LED (botão inline) |
| 📊 Status | Mostra status (botão inline) |

## 🔧 Hardware Necessário

- NodeMCU ESP8266 v2 (ou compatível)
- Sensor DHT22 (temperatura e umidade)
- LED embutido (GPIO2 - já disponível no NodeMCU)

## ⚙️ Bibliotecas (via PlatformIO)

```ini
[env:esp8266]
platform = espressif8266
board = nodemcuv2
framework = arduino

build_flags =
    -Og
    -Wall -Wextra
    -D LED_BUILTIN=2
    -I include

lib_deps =
    cotestatnt/AsyncTelegram2@^2.3.4
    bblanchon/ArduinoJson@^7.3.1
    adafruit/DHT sensor library@^1.4.6

monitor_speed = 115200
```

## 🔐 Configuração

### 1. Token do Bot Telegram

Crie o arquivo `src/secrets.h`:

```cpp
#define TELEGRAM_BOT_TOKEN "SEU_TOKEN_AQUI"

const char* WIFI_SSID = "LAB6";
const char* WIFI_PASSWORD = "";
```

### 2. Certificado TLS

O arquivo `include/tg_certificate.h` já está incluído. Ele contém o certificado
TLS do Telegram necessário para conexões seguras.

### 3. Obter Token do Bot

1. Abra o Telegram e busque por **@BotFather**
2. Envie `/newbot`
3. Siga as instruções e copie o token

## 📁 Estrutura do Projeto

```
telegram-bot/
├── platformio.ini          # Configuração do projeto
├── include/
│   └── tg_certificate.h   # Certificado TLS do Telegram
├── src/
│   ├── main.cpp           # Código principal
│   └── secrets.h          # Token e credenciais (criar)
└── README.md              # Este arquivo
```

## 🏃 Compilar e Gravar

```bash
# Compilar
pio run

# Compilar e gravar
pio run --target upload

# Monitor Serial
pio device monitor
```

## ⚠️ Notas Importantes

1. **AsyncTelegram2** - Biblioteca async, não bloqueia o loop
2. **Inline Keyboards** - Botões no Telegram para controle interativo
3. **TLS Obrigatório** - O certificado é necessário para conexão segura
4. **NTP Sync** - Sincronização de hora para validar certificado TLS
5. **Wi-Fi Direto** - Sem WiFiManager, credenciais no código

## 🔄 Diferenças do UniversalTelegramBot

| Feature | AsyncTelegram2 | UniversalTelegramBot |
|---------|-----------------|----------------------|
| Bloqueante | Não (async) | Sim |
| Inline Keyboards | Sim + callbacks | Sim (básico) |
| TLS Certificate | Obrigatório | Opcional (setInsecure) |
| NTP Sync | Necessário | Não |
| Velocidade | Mais rápido | Mais lento |