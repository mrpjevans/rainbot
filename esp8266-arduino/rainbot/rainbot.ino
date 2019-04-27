#include <Pushover.h>
#include <ESP8266HTTPClient.h>
#include <ESP8266WiFi.h>
#include "Credentials.h"

// What sensitivity to trigger?
const int sensorThreshold = 700;

// State
bool itsRaining = false;

// Inputs
int sensorPin = A0;
int sensorValue = 0; 

// Connect to T'Internet
void connect() {

  if (WiFi.status() != WL_CONNECTED) {

    WiFi.begin(ssid, password);

    while (WiFi.status() != WL_CONNECTED) {

      delay(500);
      Serial.println("Waiting for connection");

    }

    Serial.println("Connected");
  
  }
 
}

// Send a message via Pushover
void sendNotification(char *pushovermessage) {

  WiFiClient client;

  int length;
  String Msg = pushovermessage;
  length = 81 + Msg.length();
  
  if (client.connect("api.pushover.net", 80)) {
    
    Serial.println("Sending message…");
    client.println("POST /1/messages.json HTTP/1.1");
    client.println("Host: api.pushover.net");
    client.println("Connection: close\r\nContent-Type: application/x-www-form-urlencoded");
    client.print("Content-Length: ");
    client.print(length);
    client.println("\r\n");
    client.print("token=" + pushoverKey + "&user=" + pushoverUser + "&message=" + Msg);
    client.stop();
    Serial.println("Done");
    Serial.println("");
    delay(100);
    
  }

}

// Basic setup
void setup() {
  Serial.begin(115200);
  connect();
  sendNotification("Rainbot lives!");
}

// Main loop
void loop() {

  // Is it raining?
  sensorValue = analogRead(sensorPin);
  
  // Have we detected rain?
  if (sensorValue <= sensorThreshold) {

    // If this is a new state
    if (!itsRaining) {

      // Tell someone!
      itsRaining = true;
      connect();
      sendNotification("It's raining!");

    }
    
  } else if (itsRaining) {

    // If we're here, it's stopped raining.
    itsRaining = false;
    connect();
    sendNotification("Yay! No more rain.");
    
  }

  // Check every 5 seconds
  delay(5000);

}


