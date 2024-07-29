#include <ESP8266WiFi.h>

byte button = 0;
const char* ssid = "SSID";
const char* password = "PASSWORD";
bool lastState = 2;
bool deviceState = 0;
const String deviceName = "Closet Light";


WiFiServer wifiServer(4444);

void setup() {
  //set baud rate to enable serial debugging
  Serial.begin(9600);
  delay(1000);
  //Connect to wifi network
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting..");
  }
  //Print ip address this will be registered with the server later
  Serial.print("Connected to WiFi. IP:");
  Serial.println(WiFi.localIP());
  pinMode(0, INPUT_PULLUP);

  wifiServer.begin();
  registerDevice();
}

void toggleDevice() {
  deviceState = !deviceState;
}


void loop() {
  bool currentState = digitalRead(button);
  delay(10);

  //TODO if first loop send registration message to server

  WiFiClient client = wifiServer.available();
  if (client) {
    char c = client.read();
    Serial.write(c);
    if(c == '0'){
      toggleDevice();
      Serial.print("New state is:");
      Serial.println(deviceState);
    }
    client.stop();
  }

  if (lastState == 1 && currentState != 1) {
    toggleDevice();
    updateDevice();
  }
  lastState = currentState;
}
void registerDevice() {
  String jsonName = "{\"name\":\"";
  String jsonIp = "\",\"ip\":";
  String ip = WiFi.localIP().toString();
  String jsonClose = "}";
  String output = jsonName + deviceName + jsonIp + ip + jsonClose;
  sendMessage(output);
}

void updateDevice() {
  String jsonName = "{\"name\":\"";
  String jsonState = "\",\"state\":";
  String state = "";
  if (deviceState) {
    state = "\"True\"";
  } else {
    state = "\"False\"";
  }
  String jsonClose = "}";
  String output = jsonName + deviceName + jsonState + state + jsonClose;
  sendMessage(output);
}

void sendMessage(String data) {
  const uint16_t port = 4444;
  const char * host = "192.168.1.50";  //Change to whatever your LED Controller IP is

  WiFiClient client;
  if (client.connect(host, port)) //Try to connect to TCP Server
  {
    Serial.println("Connected to Desktop... ");
    char charData[data.length() + 1];
    data.toCharArray(charData, data.length() + 1);
    client.write((uint8_t *)charData, sizeof(charData));
  }
  else
  {
    Serial.println("connection failed ... ");
  }

}
