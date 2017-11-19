const int led = 3;
int value = 0;

void setup() {
  Serial.begin(9600);
  Serial.setTimeout(3);
  pinMode(led, OUTPUT);
}

void loop() {
  if (Serial.available()) {
    String data = Serial.readString();
    value = data.toInt();
  }

  analogWrite(led, value);
}
