/*
  AEGISFARM ESP32 Sensor Node — 35% Prototype
  Sends motion events to an MQTT broker.
  Replace placeholder Wi-Fi/MQTT settings before use.
*/
#include <WiFi.h>
#include <PubSubClient.h>

const char* WIFI_SSID = "YOUR_WIFI";
const char* WIFI_PASS = "YOUR_PASSWORD";
const char* MQTT_HOST = "192.168.1.100";
const int MQTT_PORT = 1883;
const char* MQTT_TOPIC = "aegisfarm/sensors/node01";
const int PIR_PIN = 27;

WiFiClient wifiClient;
PubSubClient mqtt(wifiClient);

void connectWiFi() {
  WiFi.begin(WIFI_SSID, WIFI_PASS);
  while (WiFi.status() != WL_CONNECTED) delay(400);
}

void connectMQTT() {
  while (!mqtt.connected()) {
    String clientId = "aegisfarm-node-" + String((uint32_t)ESP.getEfuseMac(), HEX);
    mqtt.connect(clientId.c_str());
    delay(500);
  }
}

void setup() {
  pinMode(PIR_PIN, INPUT);
  Serial.begin(115200);
  connectWiFi();
  mqtt.setServer(MQTT_HOST, MQTT_PORT);
}

void loop() {
  if (!mqtt.connected()) connectMQTT();
  mqtt.loop();

  if (digitalRead(PIR_PIN) == HIGH) {
    const char* payload = "{\"node\":\"node01\",\"sensor\":\"PIR\",\"motion\":true}";
    mqtt.publish(MQTT_TOPIC, payload);
    delay(3000);
  }
  delay(100);
}
