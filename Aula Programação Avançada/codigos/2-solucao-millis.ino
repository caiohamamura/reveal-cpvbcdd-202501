/*
 * CÓDIGO 2: SOLUÇÃO COM millis()
 * 
 * Este código demonstra como usar millis() para
 * executar múltiplas tarefas simultaneamente.
 * 
 * Hardware necessário:
 * - NodeMCU ESP8266
 * - LED no pino D4 (LED_BUILTIN)
 * - Buzzer no pino D5
 */

const int LED_PIN = LED_BUILTIN;    // D4 no NodeMCU
const int BUZZER_PIN = D5;          // Pino do buzzer

// Variáveis para controle de timing com millis()
unsigned long ultimoPisca = 0;      // Quando o LED piscou pela última vez
unsigned long ultimoBip = 0;        // Quando o buzzer bipou pela última vez

// Intervalos de tempo (em milissegundos)
const unsigned long INTERVALO_LED = 1000;    // 1 segundo
const unsigned long INTERVALO_BUZZER = 500;  // 0,5 segundos

void setup() {
  Serial.begin(115200);
  Serial.println("=== SOLUÇÃO COM millis() ===");
  Serial.println("LED pisca a cada 1 segundo");
  Serial.println("Buzzer toca a cada 0,5 segundos");
  Serial.println("AGORA funcionam simultaneamente!");
  Serial.println();
  
  pinMode(LED_PIN, OUTPUT);
  pinMode(BUZZER_PIN, OUTPUT);
  
  // Estado inicial
  digitalWrite(LED_PIN, LOW);
}

void loop() {
  unsigned long tempoAtual = millis();  // Tempo atual em ms
  
  // ============================================
  // TAREFA 1: Controlar o LED
  // ============================================
  if (tempoAtual - ultimoPisca >= INTERVALO_LED) {
    ultimoPisca = tempoAtual;  // Atualiza o tempo do último pisca
    
    // Alterna o estado do LED (se estava ligado, desliga; se estava desligado, liga)
    bool estadoAtual = digitalRead(LED_PIN);
    digitalWrite(LED_PIN, !estadoAtual);
    
    Serial.print("LED: ");
    Serial.println(!estadoAtual ? "LIGADO" : "DESLIGADO");
  }
  
  // ============================================
  // TAREFA 2: Controlar o buzzer
  // ============================================
  if (tempoAtual - ultimoBip >= INTERVALO_BUZZER) {
    ultimoBip = tempoAtual;  // Atualiza o tempo do último bip
    
    // Toca o buzzer por 100ms
    tone(BUZZER_PIN, 1000, 100);  // 1000Hz por 100ms
    
    Serial.println("BUZZER: BIP! (100ms)");
  }
  
  // ============================================
  // TAREFA 3: Podemos adicionar MAIS tarefas aqui!
  // ============================================
  // Exemplo: ler um sensor, enviar dados WiFi, etc.
  // O loop() continua rodando livremente!
}

/*
 * COMO FUNCIONA O millis():
 * 
 * 1. millis() retorna o número de milissegundos desde que
 *    o NodeMCU foi ligado.
 *    
 * 2. A lógica "tempoAtual - ultimoPisca >= INTERVALO_LED"
 *    verifica se já passou tempo suficiente desde a última
 *    execução.
 *    
 * 3. Quando a condição for verdadeira:
 *    a) Executamos a tarefa (piscar LED)
 *    b) Atualizamos "ultimoPisca" para o tempo atual
 *    
 * 4. O loop() continua rodando e verificando TODAS as
 *    condições a cada ciclo.
 * 
 * VANTAGENS:
 * - Não bloqueia o sistema como delay()
 * - Permite múltiplas tarefas "simultâneas"
 * - Fácil de entender e implementar
 * 
 * CUIDADO COM O OVERFLOW:
 * - millis() retorna unsigned long (0 a 4.294.967.295)
 * - Transborda após ~49,7 dias
 * - A lógica "tempoAtual - ultimoPisca" funciona mesmo no overflow!
 * 
 * EXERCÍCIO:
 * Tente adicionar uma terceira tarefa:
 * - Um segundo LED piscando a cada 2 segundos
 * - Serial.print a cada 3 segundos
 * - Ler um botão sem delay()
 */