#include "LEADS.h"

const int PIN_VOT[] = {A0};

VoltageSensor VOT(PIN_VOT);

void setup() {
    Serial.begin(9600);
    VOT.initialize();
}

void loop() {
    returnFloat(VOLTAGE_SENSOR, VOT.read());
    delay(100);
}
