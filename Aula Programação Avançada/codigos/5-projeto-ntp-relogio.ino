/*
 * PROJETO FINAL: RELÓGIO IoT COM NTP
 * 
 * Este projeto integra tudo o que aprendemos:
 * 1. Conexão WiFi
 * 2. Sincronização NTP
 * 3. millis() para LED
 * 4. Ticker para buzzer
 * 5. Serial para monitoramento
 * 
 * Hardware necessário:
 * - NodeMCU ESP8266
 * - LED no pino D4 (LED_BUILTIN)
 * - Buzzer no pino D5
 * - WiFi disponível
 * 
 * Bibliotecas necessárias:
 * - WiFi
 * - NTPClient
 * - Ticker
 */

#include <ESP8266WiFi.h>
#include <NTPClient.h>
#include <WiFiUdp.h>
#include <Ticker.h>

// ============================================
// CONFIGURAÇÃO WIFI
// ============================================
const char* SSID = "SUA_REDE_WIFI";
const char* PASSWORD = "SUA_SENHA_WIFI";

// ============================================
// CONFIGURAÇÃO NTP
// ============================================
WiFiUDP ntpUDP;
NTPClient timeClient(ntpUDP, "pool.ntp.org", -10800, 60000);
// -10800 = GMT-3 (Horário de Brasília)
// 60000 = atualiza a cada 60 segundos

// ============================================
// CONFIGURAÇÃO HARDWARE
// ============================================
const int LED_PIN = LED_BUILTIN;    // D4 no NodeMCU
const int BUZZER_PIN = D5;          // Pino do buzzer

// ============================================
// VARIÁVEIS GLOBAIS
// ============================================
// Para controle do LED com millis()
unsigned long ultimoPisca = 0;
const unsigned long INTERVALO_LED = 1000;  // 1 segundo

// Para controle do buzzer com Ticker
Ticker timerBuzzer;
int minutosAnterior = -1;

// Estados do sistema
enum EstadoSistema {
  CONECTANDO_WIFI,
  SINCRONIZANDO_NTP,
  FUNCIONANDO,
  ERRO
};

EstadoSistema estadoAtual = CONECTANDO_WIFI;

void setup() {
  Serial.begin(115200);
  Serial.println();
  Serial.println("=== RELÓGIO IoT COM NTP ===");
  Serial.println("Projeto integrador da aula");
  Serial.println("===========================");
  Serial.println();
  
  // Configurar pinos
  pinMode(LED_PIN, OUTPUT);
  pinMode(BUZZER_PIN, OUTPUT);
  digitalWrite(LED_PIN, LOW);
  
  // Conectar ao WiFi
  conectarWiFi();
  
  // Iniciar cliente NTP
  timeClient.begin();
  
  // Configurar timer do buzzer (a cada 1 minuto)
  timerBuzzer.attach(60.0, verificarMinuto);
  
  Serial.println("Sistema inicializado!");
  Serial.println("Aguardando sincronização NTP...");
  Serial.println();
}

void loop() {
  // Atualizar hora NTP
  timeClient.update();
  
  // Verificar estado do WiFi
  if (WiFi.status() != WL_CONNECTED) {
    estadoAtual = CONECTANDO_WIFI;
    reconectarWiFi();
  } else if (!timeClient.isTimeSet()) {
    estadoAtual = SINCRONIZANDO_NTP;
  } else {
    estadoAtual = FUNCIONANDO;
  }
  
  // Executar tarefas baseadas no estado
  switch (estadoAtual) {
    case CONECTANDO_WIFI:
      indicadorConectandoWiFi();
      break;
      
    case SINCRONIZANDO_NTP:
      indicadorSincronizandoNTP();
      break;
      
    case FUNCIONANDO:
      executarFuncionamentoNormal();
      break;
      
    case ERRO:
      indicadorErro();
      break;
  }
  
  // Pequeno delay para não sobrecarregar
  delay(10);
}

// ============================================
// FUNÇÕES DE CONEXÃO WIFI
// ============================================
void conectarWiFi() {
  Serial.print("Conectando à rede: ");
  Serial.println(SSID);
  
  WiFi.begin(SSID, PASSWORD);
  
  int tentativas = 0;
  while (WiFi.status() != WL_CONNECTED && tentativas < 20) {
    delay(500);
    Serial.print(".");
    tentativas++;
  }
  
  if (WiFi.status() == WL_CONNECTED) {
    Serial.println();
    Serial.print("Conectado! IP: ");
    Serial.println(WiFi.localIP());
  } else {
    Serial.println();
    Serial.println("Falha na conexão WiFi!");
    estadoAtual = ERRO;
  }
}

void reconectarWiFi() {
  static unsigned long ultimaTentativa = 0;
  
  if (millis() - ultimaTentativa > 10000) {  // A cada 10 segundos
    ultimaTentativa = millis();
    Serial.println("Tentando reconectar WiFi...");
    WiFi.disconnect();
    WiFi.begin(SSID, PASSWORD);
  }
}

// ============================================
// FUNÇÕES DE INDICAÇÃO VISUAL
// ============================================
void indicadorConectandoWiFi() {
  // LED pisca rápido (250ms)
  if (millis() - ultimoPisca >= 250) {
    ultimoPisca = millis();
    digitalWrite(LED_PIN, !digitalRead(LED_PIN));
    
    static int piscadas = 0;
    piscadas++;
    if (piscadas % 8 == 0) {  // A cada 2 segundos
      Serial.println("Conectando WiFi...");
    }
  }
}

void indicadorSincronizandoNTP() {
  // LED pisca médio (500ms)
  if (millis() - ultimoPisca >= 500) {
    ultimoPisca = millis();
    digitalWrite(LED_PIN, !digitalRead(LED_PIN));
    
    static int piscadas = 0;
    piscadas++;
    if (piscadas % 4 == 0) {  // A cada 2 segundos
      Serial.println("Sincronizando NTP...");
    }
  }
}

void indicadorErro() {
  // LED pisca muito rápido (100ms)
  if (millis() - ultimoPisca >= 100) {
    ultimoPisca = millis();
    digitalWrite(LED_PIN, !digitalRead(LED_PIN));
  }
}

// ============================================
// FUNCIONAMENTO NORMAL
// ============================================
void executarFuncionamentoNormal() {
  // LED pisca a cada 1 segundo (indicador de "vivo")
  if (millis() - ultimoPisca >= INTERVALO_LED) {
    ultimoPisca = millis();
    digitalWrite(LED_PIN, !digitalRead(LED_PIN));
  }
  
  // Mostrar hora periodicamente
  static unsigned long ultimaHoraExibida = 0;
  if (millis() - ultimaHoraExibida >= 5000) {  // A cada 5 segundos
    ultimaHoraExibida = millis();
    
    String horaFormatada = timeClient.getFormattedTime();
    int hora = timeClient.getHours();
    int minuto = timeClient.getMinutes();
    int segundo = timeClient.getSeconds();
    
    Serial.print("Hora atual: ");
    Serial.print(horaFormatada);
    Serial.print(" (");
    Serial.print(hora);
    Serial.print(":");
    Serial.print(minuto);
    Serial.print(":");
    Serial.print(segundo);
    Serial.println(")");
    
    // Mostrar estado do sistema
    Serial.print("WiFi: ");
    Serial.print(WiFi.SSID());
    Serial.print(" (");
    Serial.print(WiFi.RSSI());
    Serial.println(" dBm)");
    Serial.println();
  }
}

// ============================================
// FUNÇÃO DO BUZZER (chamada pelo Ticker)
// ============================================
void verificarMinuto() {
  // Esta função é chamada a cada 1 minuto pelo Ticker
  
  if (estadoAtual == FUNCIONANDO && timeClient.isTimeSet()) {
    int minutoAtual = timeClient.getMinutes();
    
    // Tocar buzzer a cada minuto
    tone(BUZZER_PIN, 1000, 100);  // Bip curto
    
    // Bip especial na hora cheia
    if (minutoAtual == 0) {
      Serial.println("🎵 HORA CHEIA! 🎵");
      tone(BUZZER_PIN, 1500, 500);  // Bip longo
    }
    
    // Evitar tocar múltiplas vezes no mesmo minuto
    if (minutoAtual != minutosAnterior) {
      minutosAnterior = minutoAtual;
      Serial.print("Minuto: ");
      Serial.println(minutoAtual);
    }
  }
}

/*
 * DESAFIOS PARA OS ALUNOS:
 * 
 * 1. ADICIONE UM SEGUNDO LED
 *    - LED verde: WiFi conectado
 *    - LED amarelo: Sincronizando NTP
 *    - LED azul: Funcionando normal
 *    - LED vermelho: Erro
 * 
 * 2. IMPLEMENTE ALARME
 *    - Configurar hora do alarme via Serial
 *    - Tocar melodia no horário configurado
 *    - Usar millis() para não bloquear
 * 
 * 3. MOSTRAR HORA NO DISPLAY
 *    - Conectar display LCD 16x2
 *    - Mostrar hora e data
 *    - Adicionar botão para mudar visualização
 * 
 * 4. REGISTRO DE EVENTOS
 *    - Salvar horários de eventos no EEPROM
 *    - Tocar buzzer nos horários salvos
 *    - Reset via botão
 * 
 * 5. MODO ECONOMIA DE ENERGIA
 *    - Desligar WiFi após sincronizar
 *    - Acordar a cada minuto para verificar alarmes
 *    - Usar Deep Sleep do ESP8266
 * 
 * DICAS DE DEBUG:
 * 
 * 1. Sempre comece testando o WiFi sozinho
 * 2. Depois teste o NTP sozinho
 * 3. Só então integre com millis() e Ticker
 * 4. Use Serial.println() para ver o que está acontecendo
 * 5. Teste sem hardware primeiro (simule no Serial)
 * 
 * BOA SORTE! 🚀
 */

/*
 * PARA CONFIGURAR SEU WIFI:
 * 
 * Altere estas linhas:
 * const char* SSID = "NOME_DA_SUA_REDE";
 * const char* PASSWORD = "SENHA_DA_SUA_REDE";
 * 
 * Dica: Crie um arquivo "credenciais.h" separado
 * e use #include para não expor suas senhas no código.
 */