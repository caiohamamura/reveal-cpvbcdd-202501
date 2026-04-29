# Bot Telegram para NodeMCU ESP8266

## Descrição
Este projeto implementa um bot Telegram que controla um NodeMCU ESP8266, permitindo:
- Ligar/desligar LED via comandos de chat
- Verificar temperatura e umidade do sensor DHT22
- Autoconfiguração WiFi via WiFiManager

## Hardware Necessário
- NodeMCU ESP8266
- LED (ou LED embutido do NodeMCU)
- Sensor DHT22 (opcional, para temperatura/umidade)
- Protoboard e jumpers

## Configuração

### 1. Criar Bot Telegram
1. Abra o Telegram e procure por `@BotFather`
2. Envie `/newbot`
3. Siga as instruções e obtenha o **token do bot**

### 2. Configurar o Projeto
1. Copie `src/secrets.h.example` para `src/secrets.h`
2. Edite `src/secrets.h` e cole seu token:
```cpp
#define TELEGRAM_BOT_TOKEN "123456789:ABCdefGHIjklMNOpqrSTUvwxyz"
```

### 3. Compilar e Carregar
```bash
# Usando PlatformIO
pio run
pio run --target upload
pio monitor
```

## Comandos do Bot
| Comando | Descrição |
|---------|-----------|
| `/start` | Mensagem de boas-vindas |
| `/help` | Mostrar ajuda |
| `/status` | Ver temperatura e umidade |
| `/ledon` | Ligar LED |
| `/ledoff` | Desligar LED |

## Autoconfiguração WiFi
Na primeira vez que o ESP8266 iniciar, ele criará um **access point** chamado `IoT-Bot-Config`.
1. Conecte-se a esta rede via smartphone
2. Abra o navegador e acesse `192.168.4.1`
3. Selecione sua rede WiFi e informe a senha
4. O dispositivo reiniciará e conectará automaticamente

## Arquivos
```
telegram-bot/
├── platformio.ini
├── src/
│   ├── main.cpp
│   └── secrets.h.example
└── README.md
```

## Segurança
⚠️ **NUNCA** exponha o token em código versionado!
- O arquivo `secrets.h` já está no `.gitignore`
- Use WiFiManager para evitar hardcoding de credenciais

## Licença
MIT License