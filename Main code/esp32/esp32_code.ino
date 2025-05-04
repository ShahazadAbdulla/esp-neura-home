#include <WiFi.h>
#include <WebSocketsServer.h>

const char* ssid = "Wifi";         // Wi-Fi SSID
const char* password = "password"; // Wi-Fi Password

WebSocketsServer webSocket(81);  // WebSocket server on port 81

#define LED_PIN 5    // Define the LED pin (adjust as needed)
#define FAN_PIN 17    // Define the FAN pin (adjust as needed)

String videoStatus = "Paused";  // Initially set video status to "Paused"

// Function to send status to all WebSocket clients
void sendStatusToClients() {
    String ledStatus = (digitalRead(LED_PIN) == HIGH) ? "LED ON" : "LED OFF";
    String fanStatus = (digitalRead(FAN_PIN) == HIGH) ? "FAN ON" : "FAN OFF";
    String videoStatusMessage = (videoStatus == "Playing") ? "VIDEO PLAYING" : "VIDEO PAUSED";  // Send "VIDEO PLAYING" or "VIDEO PAUSED"

    // Send the status updates to all connected WebSocket clients
    webSocket.broadcastTXT(ledStatus);  // Send LED status
    webSocket.broadcastTXT(fanStatus);  // Send FAN status
    webSocket.broadcastTXT(videoStatusMessage);  // Send VIDEO status
}

void webSocketEvent(uint8_t num, WStype_t type, uint8_t *payload, size_t length) {
    String message = String((char*)payload);

    if (type == WStype_TEXT) {
        Serial.println("Received: " + message);  // This logs the incoming WebSocket message

        // Handle light control commands
        if (message == "LED ON") {
            digitalWrite(LED_PIN, HIGH);  // Turn LED ON
            sendStatusToClients(); // Broadcast status to all clients
        }
        else if (message == "LED OFF") {
            digitalWrite(LED_PIN, LOW);  // Turn LED OFF
            sendStatusToClients(); // Broadcast status to all clients
        }
        // Handle fan control commands
        else if (message == "FAN ON") {
            digitalWrite(FAN_PIN, HIGH);  // Turn FAN ON
            sendStatusToClients(); // Broadcast status to all clients
        }
        else if (message == "FAN OFF") {
            digitalWrite(FAN_PIN, LOW);  // Turn FAN OFF
            sendStatusToClients(); // Broadcast status to all clients
        }
        // Handle video control commands
        else if (message == "VIDEO PLAY") {
            videoStatus = "Playing";  // Set video status to "Playing"
            webSocket.sendTXT(num, "VIDEO PLAY SUCCESS"); // Send confirmation to the client that sent the message
            sendStatusToClients(); // Broadcast status to all clients
        }
        else if (message == "VIDEO PAUSE") {
            videoStatus = "Paused";  // Set video status to "Paused"
            webSocket.sendTXT(num, "VIDEO PAUSE SUCCESS"); // Send confirmation to the client that sent the message
            sendStatusToClients(); // Broadcast status to all clients
        }
    }
}

void setup() {
    Serial.begin(115200);
    pinMode(LED_PIN, OUTPUT);  // Initialize the LED pin as output
    pinMode(FAN_PIN, OUTPUT);  // Initialize the FAN pin as output

    // Connect to Wi-Fi
    WiFi.begin(ssid, password);
    while (WiFi.status() != WL_CONNECTED) {
        delay(1000);
        Serial.println("Connecting to WiFi...");
    }

    Serial.print("Connected! ESP32 IP: ");
    Serial.println(WiFi.localIP());  // Print ESP32 IP

    webSocket.begin();  // Start the WebSocket server
    webSocket.onEvent(webSocketEvent);  // Set up WebSocket event handler
}

void loop() {
    webSocket.loop();  // Keep checking for WebSocket messages
}
