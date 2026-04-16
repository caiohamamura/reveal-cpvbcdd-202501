# ✅ CHECKLIST DO PROJETO
## Relógio IoT com NTP - Aula de Programação Avançada

**Nome:** ________________________  
**Turma:** 4º ano Técnico Integrado  
**Data:** ________________________  
**Nota:** ___/100

---

## 📋 PARTE 1: PREPARAÇÃO DO AMBIENTE (10 pontos)

### **Software**
- [ ] Arduino IDE instalado e configurado
- [ ] Placa ESP8266 selecionada (NodeMCU 1.0)
- [ ] Bibliotecas instaladas:
  - [ ] WiFi (já vem com Arduino)
  - [ ] NTPClient (instalar via Library Manager)
  - [ ] Ticker (instalar via Library Manager)
- [ ] Porta COM correta selecionada

### **Hardware**  
- [ ] NodeMCU ESP8266
- [ ] LED (qualquer cor)
- [ ] Buzzer ativo
- [ ] Resistor 220Ω (para o LED)
- [ ] Protoboard
- [ ] Cabos jumper (macho-macho)
- [ ] Cabo USB micro-B

---

## 🔧 PARTE 2: MONTAGEM DO CIRCUITO (15 pontos)

### **Conexões corretas:**
- [ ] NodeMCU alimentado via USB
- [ ] LED no pino **D4** (LED_BUILTIN)
- [ ] Resistor 220Ω em série com LED
- [ ] Buzzer no pino **D5**
- [ ] GND do buzzer no GND do NodeMCU
- [ ] Todas as conexões firmes e sem curto

### **Teste inicial:**
- [ ] LED acende ao conectar (pino D4 tem LED interno)
- [ ] Buzzer emite som quando pino D5 vai para HIGH
- [ ] Nenhum componente esquenta
- [ ] Protoboard organizada e limpa

---

## 💻 PARTE 3: PROGRAMAÇÃO (60 pontos)

### **Fase 1: WiFi Básico** (15 pts)
- [ ] Configurar SSID e senha no código
- [ ] Conectar à rede WiFi
- [ ] Mostrar IP no Serial Monitor
- [ ] Indicador visual de conexão (LED piscando rápido)
- [ ] Reconexão automática se WiFi cair

### **Fase 2: NTP Funcional** (15 pts)
- [ ] Inicializar cliente NTP
- [ ] Configurar fuso horário (GMT-3)
- [ ] Sincronizar hora com servidor NTP
- [ ] Mostrar hora formatada no Serial
- [ ] Indicador visual de sincronização (LED piscando médio)

### **Fase 3: Concorrência com millis()** (15 pts)
- [ ] LED pisca a cada 1 segundo usando millis()
- [ ] NÃO usa delay() em lugar nenhum
- [ ] Código bem estruturado com variáveis de timing
- [ ] Funciona mesmo com outras tarefas rodando
- [ ] LED indica estado do sistema (conectado/sincronizando)

### **Fase 4: Ticker para Buzzer** (15 pts)
- [ ] Buzzer toca a cada 1 minuto usando Ticker
- [ ] Tom diferente para horas cheias (00 minutos)
- [ ] Não interfere com outras tarefas
- [ ] Código modular com função separada
- [ ] Evita tocar múltiplas vezes no mesmo minuto

### **Bônus: Funcionalidades Extras** (+15 pts)
- [ ] **+5 pts:** Segundo LED indicando estado
- [ ] **+5 pts:** Configuração de alarme via Serial
- [ ] **+5 pts:** Mostrar hora em display LCD
- [ ] **+10 pts:** Modo economia de energia (Deep Sleep)

---

## 🧪 PARTE 4: TESTES E VALIDAÇÃO (15 pontos)

### **Testes obrigatórios:**
- [ ] **Teste 1:** Conectar WiFi → LED indica conectando → depois conectado
- [ ] **Teste 2:** Sincronizar NTP → LED indica sincronizando → depois sincronizado
- [ ] **Teste 3:** LED pisca a cada 1 segundo EXATAMENTE (usar cronômetro)
- [ ] **Teste 4:** Buzzer toca a cada 1 minuto EXATAMENTE
- [ ] **Teste 5:** Hora exibida no Serial está correta (comparar com relógio)
- [ ] **Teste 6:** Desconectar WiFi → sistema tenta reconectar automaticamente
- [ ] **Teste 7:** Tudo funciona simultaneamente (WiFi + LED + Buzzer + Serial)

### **Testes de estabilidade:**
- [ ] Executar por 5 minutos sem travar
- [ ] Memória RAM estável (monitorar no Serial)
- [ ] Sem vazamento de memória
- [ ] Reset automático se travar (Watchdog opcional)

---

## 📊 CRITÉRIOS DE AVALIAÇÃO

### **Funcionalidade** (50 pontos)
- [ ] 10 pts: WiFi conecta e mantém conexão
- [ ] 10 pts: NTP sincroniza e mostra hora correta
- [ ] 10 pts: LED pisca no timing correto
- [ ] 10 pts: Buzzer toca no timing correto
- [ ] 10 pts: Tudo funciona simultaneamente

### **Qualidade do Código** (30 pontos)
- [ ] 10 pts: Código bem organizado e comentado
- [ ] 10 pts: Uso correto de millis() (sem delay())
- [ ] 5 pts: Uso correto de Ticker
- [ ] 5 pts: Tratamento de erros (WiFi, NTP)
- [ ] Bônus: Código no GitHub (+5 pts)

### **Apresentação** (20 pontos)
- [ ] 10 pts: Circuito organizado e seguro
- [ ] 5 pts: Demonstração funcionando
- [ ] 5 pts: Explicação clara do funcionamento
- [ ] Bônus: Criatividade/Inovação (+5 pts)

---

## 🚨 PROBLEMAS COMUNS E SOLUÇÕES

### **WiFi não conecta:**
- [ ] Verificar se rede é 2.4GHz (ESP8266 não conecta em 5GHz)
- [ ] Verificar senha correta
- [ ] Verificar se router permite novos dispositivos
- [ ] Tentar rede aberta para teste

### **NTP não sincroniza:**
- [ ] Verificar conexão WiFi primeiro
- [ ] Tentar servidor alternativo: "br.pool.ntp.org"
- [ ] Aumentar timeout do NTPClient
- [ ] Verificar fuso horário correto (-10800 para Brasil)

### **LED não pisca no timing correto:**
- [ ] Verificar se está usando millis() e não delay()
- [ ] Verificar overflow de millis() (raro, mas possível)
- [ ] Verificar se não está perdendo condição por usar ">" em vez de ">="
- [ ] Testar com intervalo maior primeiro (ex: 5 segundos)

### **Buzzer não toca:**
- [ ] Verificar se buzzer é ativo (toca com 5V) ou passivo (precisa de PWM)
- [ ] Verificar polaridade (buzzer ativo tem + e -)
- [ ] Testar buzzer direto na fonte 5V
- [ ] Verificar se função do Ticker está sendo chamada

### **Sistema trava:**
- [ ] Verificar se não está usando delay() dentro de interrupt/Ticker
- [ ] Verificar memória (usar Serial.print(ESP.getFreeHeap()))
- [ ] Reduzir frequência de Serial.print()
- [ ] Implementar Watchdog timer

---

## 📝 CHECKLIST FINAL DO ALUNO

**ANTES DE ENTREGAR:**

- [ ] Código compila sem erros
- [ ] Código está no GitHub (se aplicável)
- [ ] Todos os testes da PARTE 4 passaram
- [ ] Circuito desmontado e componentes guardados
- [ ] Esta checklist preenchida e assinada

**AUTOAVALIAÇÃO:**

- [ ] Entendi a diferença entre delay() e millis()
- [ ] Sei quando usar Ticker vs millis()
- [ ] Compreendo o conceito de concorrência
- [ ] Consigo explicar como o NTP funciona
- [ ] Identifiquei meu maior aprendizado nesta aula

**DIFICULDADES ENCONTRADAS:**
1. ____________________________________________________
2. ____________________________________________________
3. ____________________________________________________

**SOLUÇÕES APLICADAS:**
1. ____________________________________________________
2. ____________________________________________________
3. ____________________________________________________

---

## 🏆 DESAFIOS EXTRAS (OPCIONAL)

Para quem terminar antes ou quiser se desafiar:

### **Nível Iniciante:**
- [ ] Adicionar botão para pausar/retomar o buzzer
- [ ] LED muda de cor baseado na hora (verde=manhã, azul=tarde, etc.)

### **Nível Intermediário:**
- [ ] Implementar alarme configurável via Serial
- [ ] Mostrar temperatura local junto com a hora
- [ ] Fazer backup da hora em EEPROM quando WiFi cair

### **Nível Avançado:**
- [ ] Implementar servidor Web para configurar alarmes
- [ ] Usar Deep Sleep e acordar apenas para tocar alarmes
- [ ] Integrar com Google Sheets para registro de eventos

---

## 📚 RECURSOS ADICIONAIS

### **Links úteis:**
- Documentação ESP8266: https://arduino-esp8266.readthedocs.io/
- Biblioteca NTPClient: https://github.com/arduino-libraries/NTPClient
- Biblioteca Ticker: https://github.com/esp8266/Arduino/tree/master/libraries/Ticker
- Simulador online: https://wokwi.com (teste sem hardware)

### **Códigos de exemplo:**
- `/codigos/1-problema-delay.ino` → O problema
- `/codigos/2-solucao-millis.ino` → Solução com millis()
- `/codigos/3-solucao-ticker.ino` → Solução com Ticker
- `/codigos/4-solucao-interrupt.ino` → Solução com Interrupt
- `/codigos/5-projeto-ntp-relogio.ino` → Projeto completo

---

**ASSINATURA DO ALUNO:** ________________________  
**DATA DE ENTREGA:** ________________________  

**FEEDBACK DO PROFESSOR:**  
________________________________________________________________  
________________________________________________________________  
________________________________________________________________  

**NOTA FINAL:** ___/100  
**OBSERVAÇÕES:** ________________________________________________