# ESP-01-Smart-Switch
Smart switch for ESP-01 devices 

## USAGE ESP-01:
1. Load sketch onto ESP-01/ESP-8266
2. GPIO-0 pulled to ground will toggle the internal state of the device
3. GPIO-2 is used to trigger a relay 

## USAGE ESP32 S2 mini
This probably works with other micropython supported devices, but I havent tested 🤷🏽‍♂️
1. load python boot code onto your device
2. GPIO-0 (build in button) will toggle the internal state of the device
3. GPIO-1 is used to trigger a relay

