#include <Servo.h>

int vermelho = 13; // define o valor 13 para a variável led
int verde = 12;
char situacao;


Servo servo_motor;

void setup() {
  Serial.begin(9600);
  pinMode(vermelho, OUTPUT); // declara led (pino 13 do arduino) como saída (OUTPUT)
  pinMode(verde, OUTPUT);
  servo_motor.attach(11);
}

void loop() {
  situacao = Serial.read(); // variável que vai receber a mensagem do Python

  if (situacao == 'E') {
    digitalWrite(verde, LOW);
    digitalWrite(vermelho, HIGH);
    servo_motor.write(0);
  } else if (situacao == 'C') {
    digitalWrite(verde, HIGH);
    digitalWrite(vermelho, LOW);
    servo_motor.write(90);

  }
  
}


