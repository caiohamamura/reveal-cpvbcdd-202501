# 📋 CHECKLIST DO PROJETO — Contador de Flashes via MQTT
## Versão Professor Caio — 22/04/2026

---

## Projeto: O que o ESP faz

1. **Conecta ao Wi-Fi**
2. **Conecta ao broker MQTT** `broker.emqx.io:1883`
3. **Inscreve-se** no tópico `aula11/ciclos/[LETRA_DA_DUPLA]`
4. **Recebe** o último valor salvo (ou 0 se não existir)
5. **Incrementa** o valor em 1
6. **Publica** o novo valor no mesmo tópico
7. **Dorme** deep sleep
8. **Repete** infinitamente

---

## ✅ Checklist de Verificação

### Hardware e Fiação
- [ ] Cabo micro USB conectado
- [ ] Wi-Fi do laboratório disponível
- [ ] **Circuito de Wake (OBRIGATÓRIO para todos os ESP8266 NodeMCU):**
  - [ ] **D0 (GPIO16) → RST** conectado (pull-up interno fraco, reforçado externamente)
  - [ ] **SD0 (GPIO7) → VCC via pull-up de 10kΩ** ← ESSENCIAL para bootstrap pós-deep sleep
  - [ ] **GPIO2 (D4) → VCC via pull-up de 10kΩ** ← Recomendado por segurança
- [ ] **Resistores de pull-up:** verificar que estão bem conectados
- [ ] **ATENÇÃO:** Sem o pull-up em GPIO7 (SD0), o ESP pode entrar em modo de programação SPI ou travar durante o bootstrap pós-deep sleep — este é o problema mais comum!

### Código
- [ ] Nome da dupla ajustado no tópico MQTT (único!)
- [ ] ssid e senha do WiFi configurados
- [ ] Código carregado sem erros
- [ ] Bibliotecas instaladas:
  - [ ] `AsyncMQTTClient` (marvinroger/async-mqtt-client)
  - [ ] `NTPClient` (já vem com ESP8266)

### Testes
- [ ] Wi-Fi conectou (Serial Monitor mostra "Wi-Fi conectado!")
- [ ] MQTT conectou (Serial Monitor mostra "MQTT conectado!")
- [ ] Recebeu valor do broker (Serial Monitor mostra "📥 Recebido: X")
- [ ] Enviou valor incrementado (Serial Monitor mostra "📤 Enviando: Y")
- [ ] Entrou em deep sleep (Serial Monitor mostra "💤 Dormindo...")
- [ ] Acordou após deep sleep e contador incrementou?

### Verificação de Persistência
- [ ] Reset manual → contador incrementa? (deep sleep wake = reset)
- [ ] Desligar USB → ligar → **MQTT broker mantém o último valor!**

---

## 📊 Rubrica de Avaliação

| Critério | Peso | Verificação |
|----------|------|-------------|
| **Conexão Wi-Fi** | 10% | Conecta corretamente |
| **Conexão MQTT** | 15% | Conecta ao broker test.mosquitto.org |
| **Subscribe** | 10% | Recebe último valor do tópico |
| **Publish** | 15% | Publica valor incremented |
| **Deep Sleep** | 15% | Dorme e acorda corretamente |
| **Persistência MQTT** | 20% | Broker mantém valor entre ciclos |
| **Código organizado** | 15% | Comentado, limpo, nome da dupla no tópico |

---

## 🔍 Como Testar a Persistência MQTT

### Cirar uma página web que acessa o mesmo MQTT via Websockets
1. Abrir: http://broker.mqtt.io:8083
2. Inscrever-se no tópico `aula11/ciclos/[LETRA_GRUPO]`
3. Adicionar um elemento simples que vai mostrar o resultado obtido do MQTT


## 💡 Dicas para Debugging

| Problema | Possível Causa | Solução |
|----------|----------------|---------|
| "Wi-Fi failed" | ssid/senha errados | Verificar credenciais |
| "MQTT timeout" | Rede bloqueando porta 1883 | Testar com celular como hotspot |
| Contador reinicia em 0 | Broker não recebeu valor anterior | Verificar se publish foi bem sucedido |
| ESP não acorda | Fio D0→RST solto ou pull-up GPIO7 ausente | Verificar D0→RST E GPIO7→VCC (10kΩ) |
| ESP trava após deep sleep / mostra caracteres garbage | Pull-up GPIO7 (SD0) ausente ou fraco | Adicionar pull-up de 10kΩ entre SD0 e VCC — sem isto o bootstrap falha |

---

## 🎯 Critério de Sucesso

**O projeto funciona se:**
1. Ao plugar o ESP, ele conecta ao Wi-Fi e MQTT
2. O Serial Monitor mostra o contador incrementando a cada ciclo
3. O contador **não reinicia em 0** mesmo após power-off (broker mantém!)
4. O deep sleep funciona (ESP dorme e acorda sozinho)

---

*Criado em: 22/04/2026*
*Projeto simplificado seguindo Roteiro_resumido.md*
