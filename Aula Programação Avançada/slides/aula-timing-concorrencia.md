# 📡 Módulo: Programação Avançada em IoT
## Aula: Relógios, NTP, Temporizadores e Osciladores

**Professor:** Caio Hamamura  
**Disciplina:** IoT - 4º ano Técnico Integrado em Informática  
**IFSP Capivari**  
**Data:** [DATA DA AULA]

---

## 🎯 Objetivos da Aula

Ao final desta aula, os alunos serão capazes de:

1. **Entender** que microcontroladores possuem clock interno
2. **Compreender** o problema do uso excessivo de `delay()`
3. **Executar** tarefas simultâneas no ESP8266
4. **Aplicar** `millis()` para concorrência
5. **Utilizar** bibliotecas de Timer
6. **Introduzir** o conceito de Interrupts
7. **Conectar** à internet para sincronizar hora (NTP)

---

## ⏱️ Parte 1: O Clock do Microcontrolador

### Pergunta provocativa:
> "Como o microcontrolador sabe quanto tempo passou?"

---

## O que é Clock?

- Todo microcontrolador possui um **oscilador interno**
- Define a velocidade de execução das instruções
- Medido em **Hertz (Hz)** - ciclos por segundo

---

## Exemplo: NodeMCU ESP8266

```
ESP8266 → 80 MHz (ou 160 MHz)
Cristal externo → 40 MHz
```

**Traduzindo:**
- 1 MHz = 1 milhão de ciclos por segundo
- 40 MHz = 40 milhões de ciclos por segundo

---

## Tudo depende do Clock!

- WiFi 📶
- `delay()` ⏳  
- `millis()` 🕐
- Timers ⏲️
- Interrupts ⚡️

**Analogia:** Pense no clock como o coração do microcontrolador!

---

## 🚫 Parte 2: O Problema do `delay()`

### Código básico que todos conhecem:

```cpp
void loop() {
  digitalWrite(LED_BUILTIN, HIGH);
  delay(1000);
  digitalWrite(LED_BUILTIN, LOW);
  delay(1000);
}
```

**Funciona perfeitamente... até agora!**

---

## E se quisermos fazer duas coisas?

### Desafio:
> "Piscar um LED **E** tocar um buzzer com ritmos diferentes"

---

## Tentativa ingênua:

```cpp
void loop() {
  digitalWrite(LED_BUILTIN, HIGH);
  delay(1000);           // LED aceso
  
  tone(buzzer, 1000);
  delay(500);           // Buzzer toca
  noTone(buzzer);
  
  digitalWrite(LED_BUILTIN, LOW);
  delay(1000);           // LED apagado
}
```

---

## O Problema na prática

**DEMONSTRAÇÃO:**  
Vejam o que acontece:

💥 **LED para** enquanto buzzer toca  
💥 **Buzzer para** enquanto LED espera  
💥 **Nada acontece simultaneamente**

---

## 💡 Parte 3: Introdução à Concorrência

### Verdade dura:
> Microcontroladores não fazem **multitarefa real**

### Mas podemos simular com:
- Alternação rápida de tarefas
- Concorrência cooperativa

---

## Exemplo do mundo real:

Imagine o ESP8266 fazendo tudo "ao mesmo tempo":
- LED piscando
- WiFi conectado  
- Sensor lendo temperatura
- Buzzer tocando alerta

**Como isso é possível?**

---

## 🛠️ Parte 4: Solução 1 - `millis()`

### O que é `millis()`?
Retorna os **milissegundos** desde que o microcontrolador ligou.

```cpp
unsigned long tempoAtual = millis();  // Ex: 12345 ms
```

---

## Substituindo `delay()` por `millis()`

```cpp
unsigned long ultimoPisca = 0;
unsigned long intervalo = 1000;

void loop() {
  if (millis() - ultimoPisca > intervalo) {
    ultimoPisca = millis();
    digitalWrite(LED_BUILTIN, !digitalRead(LED_BUILTIN));
  }
}
```

**Agora o loop continua rodando!**

---

## Adicionando o buzzer:

```cpp
unsigned long ultimoPisca = 0;
unsigned long ultimoBip = 0;

void loop() {
  // LED (1 segundo)
  if (millis() - ultimoPisca > 1000) {
    ultimoPisca = millis();
    digitalWrite(LED_BUILTIN, !digitalRead(LED_BUILTIN));
  }
  
  // Buzzer (0,5 segundos)
  if (millis() - ultimoBip > 500) {
    ultimoBip = millis();
    tone(buzzer, 1000, 100);  // Toca por 100ms
  }
}
```

✅ **Agora funciona simultaneamente!**

---

## ⏲️ Parte 5: Solução 2 - `Timer.h` (Ticker)

### Conceito:
Timers executam funções **automaticamente** em intervalos fixos.

---

## Exemplo com Ticker:

```cpp
#include <Ticker.h>

Ticker timerLED;

void piscar() {
  digitalWrite(LED_BUILTIN, !digitalRead(LED_BUILTIN));
}

void setup() {
  pinMode(LED_BUILTIN, OUTPUT);
  timerLED.attach(1, piscar);  // A cada 1 segundo
}

void loop() {
  // Vazio! O timer cuida de tudo
}
```

---

## Adicionando buzzer com Ticker:

```cpp
#include <Ticker.h>

Ticker timerLED;
Ticker timerBuzzer;

void piscar() {
  digitalWrite(LED_BUILTIN, !digitalRead(LED_BUILTIN));
}

void bip() {
  tone(buzzer, 1000, 100);
}

void setup() {
  timerLED.attach(1, piscar);      // 1 segundo
  timerBuzzer.attach(0.5, bip);    // 0,5 segundos
}
```

---

## ⚡️ Parte 6: Solução 3 - Interrupts

### O que é um Interrupt?
> "Algo **interrompe** o microcontrolador para executar uma função especial"

---

## Exemplos de Interrupts:
- Botão pressionado
- Timer expirou
- Dado recebido
- Sensor ativado

---

## Interrupt com Timer:

```cpp
#include <Ticker.h>

Ticker timer;

void ICACHE_RAM_ATTR noTimer() {
  digitalWrite(LED_BUILTIN, !digitalRead(LED_BUILTIN));
}

void setup() {
  pinMode(LED_BUILTIN, OUTPUT);
  timer.attach(1, noTimer);  // Interrupt a cada 1s
}
```

---

## ⚠️ Cuidado com Interrupts!

**NÃO USE dentro de interrupts:**
- `delay()`
- `Serial.print()`
- Funções WiFi
- Qualquer coisa lenta!

**Motivo:** Interrupts devem ser **RÁPIDOS**!

---

## 📊 Parte 7: Comparação dos Métodos

| Método      | Fácil | Preciso | Seguro | Flexível | Uso recomendado |
|-------------|-------|---------|--------|----------|-----------------|
| `delay()`   | ⭐️⭐️⭐️⭐️⭐️ | ❌      | ❌     | ❌       | Testes rápidos |
| `millis()`  | ⭐️⭐️⭐️⭐️ | ⭐️⭐️⭐️ | ⭐️⭐️⭐️⭐️ | ⭐️⭐️⭐️⭐️ | Projetos gerais |
| `Timer.h`   | ⭐️⭐️⭐️ | ⭐️⭐️⭐️⭐️ | ⭐️⭐️⭐️ | ⭐️⭐️⭐️ | Tarefas fixas |
| `Interrupt` | ⭐️⭐️ | ⭐️⭐️⭐️⭐️⭐️ | ⭐️⭐️ | ⭐️⭐️   | Tempo crítico |

---

## 🌍 Parte 8: Introdução ao NTP

### Problema:
> `millis()` sabe quanto tempo passou, mas não sabe **que horas são**!

---

## Network Time Protocol (NTP)

- Protocolo para sincronizar relógios pela internet
- Microcontrolador pergunta: "Que horas são?"
- Servidor NTP responde com hora precisa

---

## Código NTP básico:

```cpp
#include <NTPClient.h>
#include <WiFiUdp.h>

WiFiUDP ntpUDP;
NTPClient timeClient(ntpUDP);

void setup() {
  Serial.begin(115200);
  WiFi.begin("SSID", "senha");
  
  timeClient.begin();
  timeClient.setTimeOffset(-10800);  // GMT-3 (Brasil)
}

void loop() {
  timeClient.update();
  Serial.println(timeClient.getFormattedTime());
  delay(1000);
}
```

---

## 🎯 Parte 9: Projeto da Aula

### Relógio IoT com LED Indicador

**Requisitos:**
1. Conectar ao WiFi
2. Sincronizar hora via NTP
3. LED pisca a cada 1 segundo
4. Buzzer toca a cada 1 minuto
5. Mostrar hora no Serial Monitor

---

## 🏆 Desafio Extra (opcional):

**Implemente:**
- LED verde = WiFi conectado
- LED amarelo = Sincronizando NTP  
- LED azul = Hora sincronizada
- Buzzer diferente para horas cheias

---

## 🔮 Parte 10: Gancho para Próxima Aula

### Pergunta final:
> "Mas e se eu quiser saber a hora **mesmo sem WiFi**?"

---

## Próxima aula: RTC + Baixo Consumo

**Temas:**
- Relógio em Tempo Real (RTC)
- Modo Sleep (Deep Sleep)
- Acordar por alarme
- Economia de energia
- Baterias e autonomia

---

## 📚 Recursos da Aula

**Materiais disponíveis:**
- Códigos completos no GitHub
- Diagramas de conexão
- Checklist do projeto
- Exercícios de fixação

**GitHub:** [link do repositório]

---

## ❓ Dúvidas?

**Contato:**
- Email: [seu-email]
- GitHub: [seu-github]
- Discord: [canal do curso]

**Próxima aula:** RTC e Gerenciamento de Energia

---

## 👏 Obrigado!

> "Programação concorrente não é magia - é entender como o hardware funciona!"

**Bom trabalho e até a próxima!** 🚀