How can I add external button to wake up esp8266? Do I need a capacitor so that it creates just a pulse?

Mostrar maisMostrar menos

  

You don’t need to overcomplicate this—waking an ESP8266 from deep sleep is actually very simple, but it _is_ a bit constrained.

⚡ The key limitation
--------------------

The ESP8266 can **only wake from deep sleep via the RESET pin (RST)**. There’s no true external interrupt wake like on ESP32.

* * *

🔌 Basic wiring (external button)
---------------------------------

![](https://images.openai.com/static-rsc-4/xdIBeoMXiS-2rEu3N5Y9q-qnyCncGOD7cD-d_HPNzH3AA9Siel8FnUTe2_cv65k4RGqwi4zW40BM72zLrhCo80Iuq-NJnx3sIio0XmYht6Am9yCQpnsqMuIvIRbc-6nZYNYxDK8DcJUiwQqAgIv5tU2XPVohH4B2VeAPkmBQzYk?purpose=inline)

![](https://images.openai.com/static-rsc-4/TkcoVJuCLMuxbTbNJNSUXbENRWPaPOfzEoKe5Z6bxfDJxEwE1FsxG_G-4J4CsoWc8mdiJtHNeAsL3s65LZ3crbmYqP5kH1zEt-xiiu0mnOUXmf4KoJC_j4M8mHk6uz1hUIVNaeR-Fq-PNjpBqL4FdAcfhxLNbFprLfWGxNrhNGE?purpose=inline)

![](https://images.openai.com/static-rsc-4/5hoE7Yr3Ggt9DCIy6XK1R9aXaicDmjOn8mxTkVsmBDJWrWGgxBKiO9KVl6VV3i2cpTtDF7jbmVg8OHd4HcApKug9U-7ZXlb_hmJHFZQTwk5WOkilf3YbFS9QtLxt2UNQ4nLx_AAHGgyvqXLKYC0LX8cK4jDXZomsSmLnH1s6FU4?purpose=inline)

6

### What you do:

*   Connect a **push button between RST and GND**
    
*   Add a **pull-up resistor (~10kΩ)** from RST to VCC (3.3V)
    

### What happens:

*   Pressing the button pulls RST **LOW**
    
*   This **resets the ESP8266**, which effectively “wakes” it
    

* * *

🤔 Do you need a capacitor (for pulse)?
---------------------------------------

Short answer: **No, not for a button.**

### Why:

*   A push button already creates a short pulse (human press ≈ tens of ms)
    
*   The reset circuit only needs a brief LOW signal
    

### When a capacitor _is_ used:

You _might_ add one if:

*   You’re using a **sensor or circuit that holds the line LOW too long**
    
*   You want **debouncing hardware**
    
*   You’re generating reset from a **digital signal that might stay LOW**
    

Typical optional setup:

*   Small capacitor (e.g., 100nF) between RST and GND for stability
    

But again → **not required for a manual button**

* * *

🔁 Important: Deep sleep auto wake
----------------------------------

If you're also using timed wake:

![](https://images.openai.com/static-rsc-4/5rg9sAhN1ru2U0poTRYlK0Pq2xyx5DSXoKg7KyvR3hW-ClfB1ed7Xjhfeciks4NMLueSBbNrcKPKsT0AgTAJ3ApuzlYMztt1PJZYMgABwaXV_WtWbRcifRx4Wr60Atf-o-ANyRDc9F59tD08zRnlihkr8m6nMvNgqo0VNT1MWJA?purpose=inline)

![](https://images.openai.com/static-rsc-4/rSl6TpF23eW8-JeMcjI87NU9Po8vj6pOlt4UtzkYl8TQ4NI2TjQE0TyoaG3Hr5tIMaF8y_JOb1LAFwimTV1umWP4O_KRFgr_luga5l41fjKP5fVzRO1xPMDpgLyAH-pudxx1Uz5ydBkbw2ohqHh4wv7BN8DgBnfrck0td9lUmyQ?purpose=inline)

![](https://images.openai.com/static-rsc-4/ehE_GK7eA8ysShPzRqxnE0_327313_DUabLs0yWFKaASVGSY8oX0uTZzHX4GaQHMjr8_u68tBkMV611izu78k7J4aumIl6ScnwXwxjA_NfIuQd4kQOEmfpNgnnO_5XTEyNQk4SgUfN8T5nI7c7W33Bu35pruqXOssqYsE5aBZF8?purpose=inline)

5

*   Connect **GPIO16 (D0) → RST**
    
*   This allows wake after `ESP.deepSleep(time)`
    

👉 You can **combine both**:

*   Button (manual wake)
    
*   GPIO16 (timer wake)
    

* * *

⚠️ Common pitfalls
------------------

*   **No pull-up resistor on RST** → random resets
    
*   Holding button too long → repeated reboot loop (normal behavior)
    
*   Expecting GPIO interrupt wake → ❌ not supported on ESP8266
    

* * *

🧠 Summary
----------

*   ✅ Button between **RST and GND**
    
*   ✅ 10k pull-up to 3.3V
    
*   ❌ No capacitor needed for button
    
*   ✅ GPIO16 → RST if using timed wake
    

* * *

If you want, I can show a version using a **transistor or MOSFET** so another device can wake the ESP8266 cleanly without risking holding RST low.

  

#### O ChatGPT disse:

Segue o circuito em **formato de tabela de ligação** (incluindo LDR + NPN + trimpot + pulso para RST + wake por D0):

* * *

🔌 Ligações — ESP8266 + botão/LDR wake
--------------------------------------

### 🧠 Alimentação básica

| Origem | Destino | Observação |
| --- | --- | --- |
| 3.3V | VCC ESP8266 | Alimentação |
| GND | GND ESP8266 | Terra comum |

* * *

🔁 Reset / Wake (núcleo do circuito)
------------------------------------

| Origem | Destino | Componente | Observação |
| --- | --- | --- | --- |
| RST | 3.3V | Resistor 10kΩ | Pull-up obrigatório |
| GPIO16 (D0) | RST | Direto | Wake por deep sleep |
| RST | Coletor NPN | Capacitor 100nF–1µF (em série) | Gera pulso |
| RST | GND | (opcional) Resistor 100kΩ | Ajuda descarga do capacitor |

* * *

🌞 Sensor de luz (LDR + ajuste)
-------------------------------

| Origem | Destino | Componente | Observação |
| --- | --- | --- | --- |
| 3.3V | LDR | — | Início do divisor |
| LDR | Base do NPN | — | Sinal de luz |
| Base do NPN | GND | Resistor 10k–100k | Limita corrente |
| Base do NPN | Trimpot (pino central) | — | Ajuste de limiar |
| Trimpot (uma ponta) | GND | — | Referência |
| Trimpot (outra ponta) | 3.3V | — | Referência |

* * *

🔧 Transistor NPN (ex: 2N2222, BC547)
-------------------------------------

| Origem | Destino | Observação |
| --- | --- | --- |
| Emissor | GND | Referência |
| Base | Divisor LDR/trimpot | Via resistor |
| Coletor | Capacitor → RST | Puxa LOW em pulso |

* * *

🔘 Botão manual (opcional)
--------------------------

| Origem | Destino | Observação |
| --- | --- | --- |
| RST | Botão | — |
| Botão | GND | Reset manual |

* * *

🧩 Resumo funcional
-------------------

*   **Pull-up (10k)** mantém RST alto
    
*   **GPIO16 → RST** permite wake automático
    
*   **NPN + capacitor** gera **pulso curto** (evita reset infinito)
    
*   **LDR + trimpot** define o nível de luz que dispara
    
*   **Botão** permite reset manual
    

* * *

Se quiser, posso te mandar uma versão **mínima (menos componentes)** ou uma versão **com histerese (anti-flicker)** que fica bem mais estável com variação de luz.

  

#### Você disse:

Qual o tempo máximo do deepsleep?

Mostrar maisMostrar menos

  

#### O ChatGPT disse:

O tempo máximo de **deep sleep** no ESP8266 não é infinito — ele é limitado por um contador interno de 32 bits.

* * *

⏱️ Tempo máximo
---------------

O valor passado para:

```


C++

ESP.deepSleep(tempo\_em\_microsegundos);








```

tem limite de:

👉 **≈ 4.294.967.295 µs (2³² − 1)**

Convertendo:

*   ≈ **4.29 × 10⁹ µs**
    
*   ≈ **4.294 segundos × 10³**
    
*   ≈ **71,5 minutos**
    
*   ≈ **1 hora e 11 minutos**
    

* * *

⚠️ Na prática
-------------

Por segurança (overflow / bugs), muita gente usa:

👉 **máx seguro ≈ 60–70 minutos**

* * *

🔁 Como dormir mais tempo que isso
----------------------------------

Você precisa fazer ciclos:

### Exemplo: dormir 6 horas

```


C++

const  uint64\_t  SLEEP\_TIME = 60  \*  60  \*  1000000ULL; // 1 hora  
  
ESP.deepSleep(SLEEP\_TIME);








```

E acumular:

*   Contador em RTC memory
    
*   Ou contador em flash (menos recomendado)
    

* * *

🧠 Estratégia comum
-------------------

1.  Acorda
    
2.  Incrementa contador
    
3.  Se ainda não atingiu tempo total → volta a dormir
    
4.  Se atingiu → executa tarefa
    

* * *

⚠️ Detalhe importante
---------------------

*   O tempo do deep sleep **não é super preciso**
    
*   Pode ter drift (erro de alguns segundos/minutos ao longo de horas)
    

Se precisar precisão real:

*   Use NTP (internet)
    
*   Ou um RTC externo
    

* * *

✅ Resumo
--------

*   ⏱️ Máximo: **~71 minutos**
    
*   🔁 Para mais tempo: **loops de deep sleep**
    
*   🎯 Precisão: **limitada**
    

* * *

Se quiser, posso te montar um código com **RTC memory + contador persistente**, que funciona bem com seu circuito de wake por luz.

  

#### Você disse:

O ESP.rtcUserMemoryRead sobrevive ao reset?

Mostrar maisMostrar menos

  

#### O ChatGPT disse:

Sim — **com uma ressalva importante**.

✅ Sobrevive a quê?
------------------

A memória RTC do ESP8266 **sobrevive a resets**, incluindo:

*   Reset por **RST** (botão, LDR, transistor, etc.)
    
*   Reset por **GPIO16 (D0)** após `deepSleep()`
    
*   Reset por software (`ESP.restart()`)
    

👉 Ou seja: **sim, `ESP.rtcUserMemoryRead()` funciona após reset**

* * *

❌ Não sobrevive a quê?
----------------------

Ela **não sobrevive** a:

*   ❌ Perda de energia (power off)
    
*   ❌ Reset “frio” sem alimentação mantida
    

* * *

🧠 Por que isso acontece?
-------------------------

A RTC memory fica em um domínio separado, alimentado durante deep sleep.

Então:

*   CPU reinicia ✅
    
*   RAM normal é perdida ❌
    
*   **RTC memory continua lá ✅**
    

* * *

⚠️ Cuidados importantes
-----------------------

### 1\. Dados podem corromper

Boa prática: usar **checksum**:

```


C++

struct  State {  
  uint32\_t counter;  
  uint32\_t checksum;  
};  
  
uint32\_t  calcChecksum(State  s) {  
  return  s.counter ^  0xDEADBEEF;  
}








```

* * *

### 2\. Tamanho limitado

*   ~512 bytes disponíveis (depende do uso interno)
    
*   Acesso em blocos de 4 bytes
    

* * *

### 3\. Endereçamento

```


C++

ESP.rtcUserMemoryRead(offset, &data, sizeof(data));  
ESP.rtcUserMemoryWrite(offset, &data, sizeof(data));








```

* * *

🔍 Exemplo prático com reset reason
-----------------------------------

```


C++

State  state;  
  
ESP.rtcUserMemoryRead(0, (uint32\_t\*)&state, sizeof(state));  
  
if (state.checksum !=  calcChecksum(state)) {  
  state.counter = 0; // inicializa  
}  
  
state.counter++;  
  
state.checksum = calcChecksum(state);  
ESP.rtcUserMemoryWrite(0, (uint32\_t\*)&state, sizeof(state));  
  
Serial.println(ESP.getResetReason());  
Serial.println(state.counter);








```

* * *

🔗 Conectando com seu circuito (LDR + RST)
------------------------------------------

Isso é exatamente o que você precisa:

*   LDR → gera reset
    
*   ESP reinicia
    
*   RTC memory → **mantém estado entre eventos**
    

👉 Ou seja: você consegue “lembrar” coisas entre ativações por luz

* * *

✅ Resumo
--------

*   ✔️ Sobrevive a reset (RST, deep sleep wake, software reset)
    
*   ❌ Não sobrevive a desligamento
    
*   ⚠️ Use checksum para segurança
    
*   🎯 Ideal para seu caso com wake por LDR
    

* * *

Se quiser, posso te montar um exemplo onde ele mede **tempo entre eventos de luz**, mesmo usando reset como trigger.

window.\_\_oai\_logHTML?window.\_\_oai\_logHTML():window.\_\_oai\_SSR\_HTML=window.\_\_oai\_SSR\_HTML||Date.now();requestAnimationFrame((function(){window.\_\_oai\_logTTI?window.\_\_oai\_logTTI():window.\_\_oai\_SSR\_TTI=window.\_\_oai\_SSR\_TTI||Date.now()}))

  

O ChatGPT pode cometer erros. Confira informações importantes. Consulte as Preferências de cookies.