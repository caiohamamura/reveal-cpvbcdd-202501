# 📋 CHECKLIST DO PROJETO — Contador de Flashes via MQTT
## Versão Professor Caio — 22/04/2026

---

## Projeto: O que o ESP faz

1. **Conecta ao Wi-Fi**
2. **Conecta ao broker MQTT** `test.mosquitto.org:1883`
3. **Inscreve-se** no tópico `ifsp-capivari/ciclos/[NOME_DA_DUPLA]`
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
- [ ] Fio D0 → RST conectado (para wake por timer, se usar)

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

### Opção 1: Serial Monitor
1. Observar o contador subindo a cada ciclo
2. Desligar USB
3. Ligar USB novamente
4. Verificar se o contador continua de onde parou (não reinicia em 0!)

### Opção 2: MQTT Explorer (web)
1. Abrir: http://test.mosquitto.org:1880
2. Inscrever-se no tópico `ifsp-capivari/ciclos/#`
3. Observar os valores aparecendo em tempo real

### Opção 3: Comando mosquitto_sub
```bash
# No computador com mosquitto instalado:
mosquitto_sub -h test.mosquitto.org -t "ifsp-capivari/ciclos/#" -v
```

---

## 💡 Dicas para Debugging

| Problema | Possível Causa | Solução |
|----------|----------------|---------|
| "Wi-Fi failed" | ssid/senha errados | Verificar credenciais |
| "MQTT timeout" | Rede bloqueando porta 1883 | Testar com celular como hotspot |
| Contador reinicia em 0 | Broker não recebeu valor anterior | Verificar se publish foi bem sucedido |
| ESP não acorda | Fio D0→RST solto | Verificar conexão D0→RST |

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
