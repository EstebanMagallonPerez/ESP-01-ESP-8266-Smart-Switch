# ESP-01-Smart-Switch
Smart switch for ESP-01 devices 

USAGE:
1. Load sketch onto ESP-01/ESP-8266 or load micropython onto your device(tested on esp32-s2 mini)
2. GPIO-0 pulled to ground will toggle the internal state of the device
3. GPIO-2 is used to trigger a relay to enable/disable whatever device is connected

