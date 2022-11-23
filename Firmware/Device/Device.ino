#include <Wire.h>           
 #include <LiquidCrystal_I2C.h>    
 LiquidCrystal_I2C lcd(0x27,20,4);   
 // if lcd is not print then use this 0x27..


 // Import required libraries
#include <ESP8266WiFi.h>
#include <ESPAsyncTCP.h>
#include <ESPAsyncWebServer.h>

// Replace with your network credentials
String ssid = "Wegner";
String password = "12345678";

const char* PARAM_INPUT_1 = "people";
const char* PARAM_INPUT_2 = "Y";

// Create AsyncWebServer object on port 80
AsyncWebServer server(80);
int vehicleSpeed=0;
int numberOfPeople=0;

void setup() {
  // put your setup code here, to run once:
Serial.begin(9600);
 lcd.begin();      
   lcd.backlight();



 // Connect to Wi-Fi
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi..");
    displayOnLcd("Connecting to: ",0,0);
     displayOnLcd(String(ssid), 0,1);
  }

  // Print ESP Local IP Address
  Serial.println(WiFi.localIP());
  
  displayOnLcd("Connected to: ", 0,0);
  lcd.setCursor(0,2);
  lcd.print(WiFi.localIP());

  
  // Send a GET request to <ESP_IP>/update?output=<inputMessage1>&state=<inputMessage2>
  server.on("/", HTTP_GET, [] (AsyncWebServerRequest *request) {
    String people;
   
    // GET input1 value on <ESP_IP>/update?output=<inputMessage1>&state=<inputMessage2>
    if (request->hasParam(PARAM_INPUT_1)) {
      people = request->getParam(PARAM_INPUT_1)->value();
//      inputMessage2 = request->getParam(PARAM_INPUT_2)->value();
numberOfPeople=people.toInt();
      
    }
    else {
      people = "None";
    }
    Serial.print("People: ");
    Serial.print(people);
    
    request->send(200, "text/plain", String(vehicleSpeed));
  });

  // Start server
  server.begin();
  delay(3000);
  lcd.clear();

   
}
String convertSpeedTo3SF(int Speed){
  if (Speed<10){
    return "00"+String(Speed);
  }
  else if (Speed<100){
    return "0"+String(Speed);
  }
  else {
    return String(Speed);
  }
}
void loop() {
  // put your main code here, to run repeatedly:
  int Speed=measureSpeed();
//  lcd.clear();
  displayOnLcd("Speed:"+convertSpeedTo3SF(Speed), 0,0);
  displayOnLcd("KM/H", 10,0);
  displayOnLcd("Passengers: "+String(numberOfPeople), 0,1);

}
int measureSpeed(){
  // put your main code here, to run repeatedly:
  int rawSpeed=analogRead(A0);
  int processedSpeed=map(rawSpeed,512, 1025,0,300);
  
  Serial.print("Speed in KM/H:");
  int speedKm_H=abs(abs(processedSpeed)-54);
  vehicleSpeed=speedKm_H;
  Serial.println(speedKm_H);
  delay(500);
  return speedKm_H;
}
void displayOnLcd(String message, int row, int column){
  
   lcd.setCursor(row,column);  
   lcd.print(message);  
     
}
