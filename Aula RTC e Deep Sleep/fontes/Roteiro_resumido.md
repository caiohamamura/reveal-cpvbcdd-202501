# 📊 RESUMO EXECUTIVO
## "RTC, Deep Sleep e Autonomia no ESP8266"

### Contexto
- **Módulo:** Programação Avançada em IoT (Aula 11)
- **Sequência:** Depois de Timing/NTP → Antes de Máquina de Estados
- **Foco:** Economia de energia + persistência de dados + interrupt por luz

### 🎯 Objetivos
1. Entender **por que** deep sleep é essencial em IoT de campo
2. Implementar deep sleep com despertar por **timer** e por **interrupt (transistor)**
3. Usar **LittleFS + ArduinoJson** para persistir dados (solução ESP8266!)
4. Implementar na prática um interrupt utilizando transistor.

### Roteiro Geral

Contexto:

- Para projetos a bateria precisamos economizar energia

Solução:

- Podemos criar projetos que funcionam ligando e desligando em intervalos
- Ou ainda, o ESP8266 permite acordar baseado em um sinal como veremos

O `ESP.deepSleep()` na verdade desliga ESP, mas você pode configurar um tempo para que o pino D0 envie um pulso LOW após um tempo em microsegundos de no máximo 70 minutos.

Esquema de funcionamento do código:

- O código não usa mais `loop()`, tudo acontece no `setup()`, terminando um com um `ESP.deepSleep()`
  - Ao retomar, o `setup()` será executado desde o início novamente como se tivesse acabado de iniciar
- LittleFS e ArduinoJSON podem ser usados para gravar e restaurar estado
- Outra forma é usar o `ESP.rtcUserMemoryWrite()` e `ESP.rtcUserMemoryRead()`.
- Se for uma estação: um arquivo pode apenas receber novas linhas (leituras de sensor, por exemplo).


### 🔑 Conceitos-chave
- **Deep Sleep:** 20 μA vs 80 mA = 4000x economia
- **Acorda:** por tempo ou por sinal
- **D0→RST:** Conexão para acordar
- **KSP2222A:** Transistor NPN como interruptor controlado por luz
- **LittleFS + ArduinoJson:** Persistência que funciona no ESP8266

### 🔌 Hardware Especial (além do usual)
- **Transistor KSP2222A** (NPN)
- **LDR** (Light Dependent Resistor)
- **Trimpot** 10kΩ
- **Resistor** 10kΩ (para base do transistor)
- **Capacitor** 1μF (gerar pulso)
- **Botão Switch** 



### 📅 Estrutura (4 aulas × 45 min)

| Aula | Tema | Tipo |
|------|------|------|
| 1 | Engajamento + Teoria | Expositiva + Exercício |
| 2 | Hands-on: Pisca LED -> dorme -> interrupt manual botão -> acorda Pisca LED -> dorme -> ... | Prática |
| 3 | LittleFS + NTP Inteligente | Prática |
| 4 | Projeto contador de flashes | Projeto em duplas |

### Projeto contador de flashes

O projeto de contador de flashes é simples e tem dois atores.

#### Parte 1: o NodeMCU ESP8266

1. Ligar via MQTT (marvinroger/async-mqtt-client) ao emqx.io e verificar a última mensagem persistente (deve ser uma contagem), se não tiver inicia em 0
2. Incrementa o valor em 1 e envia a mensagem persistente ao MQTT com o novo valor
3. Faz deep sleep



---
*Criado em: 22/04/2026*
