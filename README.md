# ESP-01-Smart-Switch
Smart switch for ESP-01 devices/esp32 device with micropython... probably works with other micropython supported devices, I have no proof, but I have no doubts 🤷🏽‍♂️

## USAGE ESP-01:
1. Load sketch onto ESP-01/ESP-8266
2. GPIO-0 pulled to ground will toggle the internal state of the device
3. GPIO-2 is used to trigger a relay 

## USAGE ESP32 S2 mini(micropython)
1. load python boot code onto your device
2. GPIO-0 (build in button) will toggle the internal state of the device
3. GPIO-1 is used to trigger a relay

## Dummy server
Listens to and sends data to the connected devices. Some simple TCP server like this could be used to manage device states
