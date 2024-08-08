#include <ESP8266WiFi.h>
#include <EEPROM.h>


//device variables
bool lastState = 2;
bool deviceState = 0;

//START CONFIG
byte buttonPin = 0;
byte relayPin = 2;
const char* ssid = "SSID";
const char* password = "Password";
const String deviceName = "Dinning Table";
const uint16_t port = 4444;
const char * server_ip = "192.168.1.50";
//END CONFIG


WiFiServer wifiServer(port);

void setup() {
  //set baud rate to enable serial debugging
  Serial.begin(9600);
  delay(1000);

  //Connect to wifi network
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    printData("Connecting..");
  }
  //Print ip address this will be registered with the server later
  printData("Connected to WiFi. IP:");
  printData(WiFi.localIP().toString());
  pinMode(buttonPin, INPUT_PULLUP);
  pinMode(relayPin, OUTPUT);

  wifiServer.begin();
  sendDeviceRegistration();
}

void setRelay(bool state) {
  if (state) {
    printData("New state is HIGH");
    deviceState = state;
    digitalWrite(relayPin, HIGH);
    sendDeviceState();
  } else {
    printData("New state is HIGH");
    deviceState = state;
    digitalWrite(relayPin, LOW);
    sendDeviceState();
  }
}

void toggleRelay() {
  setRelay(!deviceState);
}


void loop() {
  bool currentState = digitalRead(buttonPin);
  delay(10);

  //TODO if first loop send registration message to server

  WiFiClient client = wifiServer.available();
  if (client) {
    char c = client.read();
    printData("handling a client message");
    if (c == '0') {
      setRelay(false);
    } else if (c == '1') {
      setRelay(true);
    } else if (c == '2') {
      toggleRelay();
    } else {
      sendDeviceState();
    }
    client.write(deviceState);
    client.stop();
  }

  if (lastState == 1 && currentState != 1) {
    toggleRelay();
  }
  lastState = currentState;
}

//Server Communication code
void sendDeviceRegistration() {
  String jsonName = "{\"name\":\"";
  String jsonIp = "\",\"ip\":\"";
  String ip = WiFi.localIP().toString();
  String jsonClose = "\"}";
  String output = jsonName + deviceName + jsonIp + ip + jsonClose;
  sendMessage(output);
}

void sendDeviceState() {
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

  WiFiClient client;
  if (client.connect(server_ip, port)) //Try to connect to TCP Server
  {
    printData("Connected to Desktop... ");
    char charData[data.length() + 1];
    data.toCharArray(charData, data.length() + 1);
    client.write((uint8_t *)charData, sizeof(charData));
  }
  else
  {
    printData("connection failed ... ");
  }
}
#ifdef DEBUG
void printData(String toPrint) {
  Serial.println(toPrint);
}
#else
void printData(String toPrint) {}
#endif