# Discord Webhook para NodeMCU ESP8266

## Descrição
Este projeto implementa um sistema de envio de dados de sensores para um canal Discord usando **webhooks** (não requer bot). O NodeMCU ESP8266 envia periodicamente leituras de temperatura e umidade para o Discord.

## Hardware Necessário
- NodeMCU ESP8266
- Sensor DHT22 (temperatura/umidade)
- Protoboard e jumpers

## Configuração

### 1. Criar Webhook Discord
1. Abra Discord e vá para **Server Settings** > **Integrations** > **Webhooks**
2. Clique em "Create Webhook"
3. Copie a **URL do webhook**

### 2. Configurar o Projeto
1. Copie `src/secrets.h.example` para `src/secrets.h`
2. Edite `src/secrets.h` e cole sua URL:
```cpp
#define DISCORD_WEBHOOK_URL "https://discord.com/api/webhooks/xxxxxxx/yyyyyyy"
```

### 3. Compilar e Carregar
```bash
# Usando PlatformIO
pio run
pio run --target upload
pio monitor
```

## Como Funciona
- A cada **30 segundos**, o ESP8266 lê o sensor DHT22
- Os dados são enviados via HTTP POST para o webhook Discord
- Você verá uma mensagem no canal com as leituras

## Exemplo de Mensagem
```
📊 Dados do Sensor IoT
🌡️ Temp: 25.3°C
💧 Umidade: 68.5%
```

## Autoconfiguração WiFi
Na primeira vez que o ESP8266 iniciar, ele criará um **access point** chamado `IoT-Discord-Config`.
1. Conecte-se a esta rede via smartphone
2. Abra o navegador e acesse `192.168.4.1`
3. Selecione sua rede WiFi e informe a senha
4. O dispositivo reiniciará e conectará automaticamente

## Robustez
- O código implementa **retry 3x** em caso de falha de envio
- Intervalo de 1 segundo entre tentativas
- Log detalhado no Serial Monitor

## Arquivos
```
discord-webhook/
├── platformio.ini
├── src/
│   ├── main.cpp
│   └── secrets.h.example
└── README.md
```

## Segurança
⚠️ **NUNCA** exponha a URL do webhook em código versionado!
- O arquivo `secrets.h` já está no `.gitignore`

## Licença
MIT License