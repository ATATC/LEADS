#include "WheelSpeedSensor.h"
#include "Algorithms.h"

WheelSpeedSensor::WheelSpeedSensor(int *const pins) : Device<int>(pins) {
}

void WheelSpeedSensor::initialize() {
    pinMode(_pins[0], INPUT);
    _t1 = 0;
    _t2 = millis();
}

int WheelSpeedSensor::read() {
    if (millis() - _t2 > BOUNCETIME && pulseTriggered(_pins[0])) {
        _t1 = _t2;
        _t2 = millis();
    }
    return 60000 / (_t2 - _t1);
}

String WheelSpeedSensor::debug() {
    return String(_t1) + " " + String(_t2);
}
