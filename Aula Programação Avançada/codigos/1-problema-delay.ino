/*
 * CÓDIGO 1: O PROBLEMA DO delay()
 * 
 * Este código demonstra o problema clássico do delay():
 * Quando queremos fazer duas coisas ao "mesmo tempo", 
 * na verdade uma trava a outra.
 * 
 * Hardware necessário:
 * - NodeMCU ESP8266
 * - LED no pino D4 (LED_BUILTIN)
 * - Buzzer no pino D5
 */

const int LED_PIN = LED_BUILTIN;  // D4 no NodeMCU
const int BUZZER_PIN = D5;        // Pino do buzzer

void setup() {
  Serial.begin(115200);
  Serial.println("=== DEMONSTRAÇÃO DO PROBLEMA DO delay() ===");
  Serial.println("LED pisca a cada 1 segundo");
  Serial.println("Buzzer toca a cada 0,5 segundos");
  Serial.println("MAS... nada acontece simultaneamente!");
  Serial.println();
  
  pinMode(LED_PIN, OUTPUT);
  pinMode(BUZZER_PIN, OUTPUT);
}

void loop() {
  Serial.println("LED: LIGADO");
  digitalWrite(LED_PIN, HIGH);   // Acende LED
  delay(1000);                   // Espera 1 segundo
  
  Serial.println("BUZZER: TOCANDO (500ms)");
  tone(BUZZER_PIN, 1000);        // Toca buzzer em 1kHz
  delay(500);                    // Espera 0,5 segundos
  noTone(BUZZER_PIN);            // Para buzzer
  
  Serial.println("LED: DESLIGADO");
  digitalWrite(LED_PIN, LOW);    // Apaga LED
  delay(1000);                   // Espera 1 segundo
  
  Serial.println("--- Ciclo completo ---");
  Serial.println();
}

/*
 * OBSERVAÇÃO IMPORTANTE:
 * 
 * Execute este código e observe no Serial Monitor:
 * 1. O LED acende e fica aceso por 1 segundo
 * 2. O buzzer toca por 0,5 segundos (LED CONTINUA ACESO)
 * 3. O LED apaga e fica apagado por 1 segundo
 * 4. O buzzer NÃO TOCA durante este tempo
 * 
 * PROBLEMA: O buzzer só toca quando o LED está aceso!
 *           Quando o LED está apagado, o buzzer fica em silêncio.
 * 
 * POR QUE ISSO ACONTECE?
 * O delay(1000) após desligar o LED IMPEDE que o código
 * chegue na parte do tone() novamente.
 * 
 * SOLUÇÃO: Precisamos de concorrência!
 */