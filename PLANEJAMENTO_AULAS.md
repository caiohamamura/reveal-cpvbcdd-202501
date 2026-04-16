# PLANEJAMENTO_AULAS.md - Curso IoT - IFSP Capivari

## Informações Gerais

**Curso:** Técnico Integrado em Informática para Internet
**Professor:** Caio Hamamura
**Instituição:** IFSP - Campus Capivari
**Data de início do planejamento:** 12 de abril de 2026
**Carga horária:** 4 aulas de 45 minutos semanais
**Turma:** 4º ano do ensino médio integrado
**Hardware principal:** NodeMCU ESP8266
**Recursos especiais disponíveis:** Impressora 3D, cortadora a laser, sensores variados, motores

## Objetivos do Curso

1. Desenvolver competências em sistemas embarcados para IoT
2. Integrar conhecimentos de programação, eletrônica e redes
3. Projetar e implementar soluções IoT para problemas reais
4. Promover trabalho colaborativo e documentação técnica

## Estrutura Ajustada à Ementa (13 Tópicos)

### Tópico 1: Noções básicas de ESP8266
- Apresentação do NodeMCU ESP8266
- Configuração do ambiente Arduino IDE
- Primeiro programa: "Hello World" com LED onboard
- GPIO básico: entrada e saída digital

### Tópico 2: Conectividade à Internet
- Configuração Wi-Fi no ESP8266
- Conexão à rede do laboratório
- Verificação de conexão (ping, status)
- Conceitos de IP, gateway, DNS

### Tópico 3: Protocolos de Comunicação
- HTTP básico: GET e POST requests
- Introdução ao MQTT (conceitos de broker, tópicos)
- Comparação HTTP vs MQTT para IoT
- Exemplos práticos com cada protocolo

### Tópico 4: Aplicativos WEB
- Servidor web básico no ESP8266
- Páginas HTML simples para controle
- Formulários web para interação
- CSS básico para estilização

### Tópico 5: Fluxos complexos: Node-RED
- Instalação e configuração do Node-RED
- Conexão do ESP8266 ao Node-RED
- Criação de dashboards básicos
- Fluxos simples de dados

### Tópico 6: Padrões de IoT - Clientes em tempo real
- WebSockets vs polling
- Implementação de atualização em tempo real
- Dashboard que atualiza automaticamente
- Exemplo: monitoramento de sensor em tempo real

### Tópico 7: Padrões de IoT - Controle remoto
- Controle de dispositivos via web
- Botões, sliders, interruptores virtuais
- Segurança básica (autenticação simples)
- Controle de múltiplos dispositivos

### Tópico 8: Padrões de IoT - Clientes sob demanda
- Requisições sob demanda (on-demand)
- Otimização de energia
- Exemplo: acionar sensor apenas quando solicitado
- Comparação com monitoramento contínuo

### Tópico 9: Padrões de IoT - Aplicativos web
- Progressive Web Apps (PWA) básico
- Aplicativo web responsivo
- Instalação no celular ("Add to home screen")
- Funcionamento offline básico

### Tópico 10: Padrões de IoT - De máquina para homem
- Notificações e alertas
- Email/SMS a partir do ESP8266
- Integração com Telegram/WhatsApp (API básica)
- Dashboard com alertas visuais

### Tópico 11: Padrões de IoT - Máquina para máquina
- Comunicação entre múltiplos ESP8266
- Sistemas distribuídos simples
- Sincronização de estados
- Exemplo: sistema de iluminação coordenada

### Tópico 12: Plataformas de IoT
- ThingSpeak para armazenamento e visualização
- Blynk para prototipagem rápida
- Firebase Realtime Database
- Comparação de plataformas gratuitas

### Tópico 13: Projeto Integrador
- Definição de problema real
- Projeto completo com ESP8266
- Integração com impressora 3D/cortadora a laser (caixas, suportes)
- Documentação e apresentação final

## Recursos Necessários

### Hardware (por grupo de 2-3 alunos):
- [ ] NodeMCU ESP8266 (1 por grupo)
- [ ] Kit de sensores básicos (temperatura DHT11/22, umidade, movimento PIR, luz LDR)
- [ ] Atuadores (LEDs, relé, servo motor, buzzer)
- [ ] Protoboard, jumpers e componentes básicos
- [ ] Fonte de alimentação USB
- [ ] Cabo micro USB

### Recursos Especiais do IFSP Capivari:
- [ ] Impressora 3D (para caixas e suportes dos projetos)
- [ ] Cortadora a laser (para placas frontais e estruturas)
- [ ] Sensores avançados disponíveis no laboratório
- [ ] Motores e atuadores variados

### Software:
- [ ] Arduino IDE (gratuito)
- [ ] Python 3.x
- [ ] Mosquitto (broker MQTT local)
- [ ] Node-RED (opcional para visualização)
- [ ] Git para versionamento

### Laboratório:
- [ ] Computadores com acesso USB
- [ ] Internet para configuração de dispositivos
- [ ] Espaço para montagem de protótipos
- [ ] Armazenamento seguro para componentes

## Metodologia

1. **Aprendizado baseado em projetos**: Cada unidade culmina em um mini-projeto
2. **Pair programming**: Trabalho em duplas/trios
3. **Documentação técnica**: GitHub como portfólio
4. **Avaliação contínua**: Checkpoints semanais
5. **Apresentações**: Compartilhamento de soluções

## Cronograma Detalhado (1 Semestre - ~16 semanas)

**Semana 1:** Tópico 1 - Apresentação do curso + Primeiro pisca LED
**Semana 2:** Tópico 2 - Conexão Wi-Fi + verificação online
**Semana 3:** Tópico 3 - HTTP básico + leitura de API pública
**Semana 4:** Tópico 3 - MQTT + broker local Mosquitto
**Semana 5:** Tópico 4 - Servidor web básico no ESP8266
**Semana 6:** Tópico 5 - Node-RED + dashboard simples
**Semana 7:** Tópico 6 - WebSockets + atualização em tempo real
**Semana 8:** Tópico 7 - Controle remoto via web
**Semana 9:** Tópico 8 + 9 - Clientes sob demanda + PWA
**Semana 10:** Tópico 10 - Notificações (email/Telegram)
**Semana 11:** Tópico 11 - M2M (múltiplos ESP8266)
**Semana 12:** Tópico 12 - Plataformas IoT (ThingSpeak/Blynk)
**Semana 13:** Tópico 13 - Início do projeto integrador
**Semana 14:** Tópico 13 - Desenvolvimento do projeto
**Semana 15:** Tópico 13 - Finalização + impressão 3D/corte laser
**Semana 16:** Tópico 13 - Apresentações finais

*Nota: Cada tópico ocupa aproximadamente 3 horas (4 aulas de 45 min)*

## Acompanhamento

### Checkpoints:
- ✅ Configuração do ambiente
- ✅ Primeiro circuito funcionando
- ✅ Leitura de sensor + envio de dados
- ✅ Sistema com múltiplas tarefas
- ✅ Protótipo funcional
- ✅ Documentação completa
- ✅ Apresentação final

### Critérios de Avaliação Alinhados aos Objetivos:
- Entendimento dos conceitos IoT (15%)
- Aplicação prática dos conceitos (20%)
- Integração robótica + internet (15%)
- Desenvolvimento de programas/algoritmos (20%)
- Teste e recuperação de dados (10%)
- Interação com sensores avançados (10%)
- Controle remoto via internet (10%)

---

## Próximos Passos

1. **Criar guias detalhados** para cada tópico com atividades passo a passo
2. **Preparar exemplos de código** específicos para ESP8266
3. **Desenvolver projetos práticos** que utilizem impressora 3D/cortadora laser
4. **Criar materiais de apoio** (slides, checklists, rubricas de avaliação)
5. **Planejar uso dos recursos especiais** integrados às atividades
6. **Estabelecer sistema de versionamento** (GitHub para os projetos)

## Vantagens do ESP8266:
✅ Wi-Fi integrado - não precisa de módulos adicionais
✅ Mais barato que Arduino + shield Wi-Fi
✅ Compatível com Arduino IDE - curva de aprendizado suave
✅ Suficiente para todos os padrões IoT da ementa
✅ Ideal para prototipagem rápida

---

*Este documento será atualizado conforme o planejamento avança. Última atualização: 12/04/2026*