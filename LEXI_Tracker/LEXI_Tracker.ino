/* File: Lexi_Tracker.ino
 *
 * Author: Max Maleno
 *
 * Last Updated: 7/28/18
*/

 // server IP = 192.168.0.12
 // when connected to my phone = 172.20.10.5
 // when connected to home = 192.168.1.23

#include <ESP8266WiFi.h>
#include <SoftwareSerial.h>
#include <TinyGPS.h>

//The Park's 14214 WiFi credentials
const char* ssid = "715E7C";                //"M.Network";//"Max Maleno's iPhone";
const char* password = "B2ULAEG342585";     //"dpmaleno1";//"mmaleno16";

// Create an instance of the server
// specify the port to listen on as an argument
WiFiServer server(80);
TinyGPS gps;
SoftwareSerial ss(13, 15); // green, yellow (on gps: tx, rx)

int fixPin = 16;              // pin Fix pin from GPS is connected to on Feather
int countOnes;                // initialize our counter for how long fix is high
String ScountOnes;            // create a string that we can print to Serial for # of countOnes
long rssi;                    // strength of wifi signal, in dBm
int ADCreading = 0;           // int to store our ADC reading in.  The ADC is connected to
                              // a voltage divider which is powered by the battery.  See
                              // readADC() for more information

int hoursRelativeUTC = -7;  // Quick timezone and daylight savings comparison variable

// runs once on startup
void setup()
{
  Serial.begin(115200);               // initialize computer's serial monitor
  ss.begin(9600);                     // initialize software serial (to avoid using hardware UART pins
  delay(10);
  
  // Connect to WiFi network & print useful information
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);
  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);

  //Give update on connection status on Serial monitor
  while (WiFi.status() != WL_CONNECTED)
  {
    delay(500);
    Serial.print(".");                // status "connecting" dots on serial monitor
  }
  
  Serial.println("");
  Serial.println("WiFi connected");
  rssi = WiFi.RSSI();                 // get wifi signal strength (RSSI)
  Serial.print("RSSI: ");
  Serial.println(rssi);
  
  // Start the server
  server.begin();
  Serial.println("Server started");

  // Print the IP address
  Serial.println(WiFi.localIP());
}

// runs continuously, equivalent to a while(1) loop
void loop()
{
  float flat, flon;                           // create our floats lat and long
  unsigned long age;                          // create our unused but necessary age

  rssi = WiFi.RSSI();                         // recalculate RSSI to be sent as telemetry
  String rssiString = String(rssi);           // convert RSSI to string to be put into HTML doc
  Serial.println("RSSI: " + rssiString);
  readADC();
  String adcString = String(ADCreading);
  Serial.println("ADC: " + adcString);
  
  boolean fixStatus = checkFix();             // find out whether we are connected or not to satellites
                                              // check out checkFix() down below
  // print fix status on monitor
  if (fixStatus)
  {
    Serial.println("Has Fix");
  }
  else
  {
    Serial.println("No Fix");
  }
  
  gps.f_get_position(&flat, &flon, &age);               // extract telemetry from GPS module
  String flatString = String(flat, 6);                  // convert latitude to 6-char string
  String flonString = String(flon, 9);                  // convert latitude to 9-char string
  String fixStatusString = String(fixStatus);           // convert fix status to string
  String numSatsString = String(gps.satellites());      // create string of how many satellites are connected
  
  int time[4] = {0,0,0,0};                              // initialize timestamp array
  getTime(gps, time);                                   // extract nuclear clock time from GPS data and put it into time array
                                                        // see getTime below
  // put timestamp data into separate strings
  String hourString = String(time[0]);
  String minString = String(time[1]);
  String secString = String(time[2]);
  String merString = String();

  // interpret timestamp as AM or PM
  if (time[3])
  {
    merString = "PM";
  }
  else
  {
    merString = "AM";
  }

  // needed for TinyGPS library to not poop its pants *eye roll*
  smartdelay(0);
  
  // Check if a client has connected
  WiFiClient client = server.available();
  if (!client)
  {
    return;
  }
  
  // Wait until a client makes a request.  This can either be mac or pi
  Serial.println("new client");
  while(!client.available())
  {
    delay(1);
  }
  
  // Read the first line of the request
  String req = client.readStringUntil('\r');
  Serial.println(req);
  client.flush();

/*
  // Prototyping lines to create a random coordinate in the playing field
  float x = randomDouble(-117.754903, -117.753419);//working coord: -117.753640
  float x = flon;
  String xString = String(x, 9);
  Serial.println(xString);

  float y = randomDouble(33.652619, 33.653867);//working coord: 33.652975
  float y = flat;
  String yString = String(y, 6);
  Serial.println(yString);
*/

  Serial.println(flonString);
  Serial.println(flatString);

  // Prepare the HTML document to be sent
  String s = "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n"
    "<!DOCTYPE HTML>\r\n"
    "<html>\r\n"
    "wifi: " + rssiString + "<br/>\r\n"
    "adc: " + adcString + "<br/>\r\n"
    "x: " + flonString + "<br/>\r\n"
    "y: " + flatString + "<br/>\r\n"
    "fix?: " + fixStatusString + "<br/>\r\n"
    "sats: " + numSatsString + "<br/>\r\n"
    "hour: " + hourString + "<br/>\r\n"
    "min: " + minString + "<br/>\r\n"
    "sec: " + secString + "<br/>\r\n"
    "mer: " + merString + "<br/>\r\n"
    "</html>";

  // Send the response to the client
  client.print(s);
  delay(500);
  Serial.println("Client disonnected");
}

// Function to create our random x and y coordinate
// Not used in working version, just for prototyping / debugging
double randomDouble(double minf, double maxf)
{
  return minf + random(1UL << 31) * (maxf - minf) / (1UL << 31);  // use 1ULL<<63 for max double values)
}

// necessary delay so, as stated above, TinyGPS library doesn't fail to do its job
static void smartdelay(unsigned long ms)
{
  unsigned long start = millis();
  do 
  {
    while (ss.available())
      gps.encode(ss.read());
  }
  while (millis() - start < ms);
}


// function to find out whether we are connected to satellites or not.
// this function is based on the fact that Fix will be high for ~200ms
// every 15 seconds if there is a fix.  If there is not a fix, Fix will
// be high for !1s every 2s.  Fairly janky, but is extremely reliable!!
boolean checkFix()
{  
  for (int count = 0; count < 2000; count++)
  { 
    // loop for ~2 seconds
    int fixRead = digitalRead(fixPin);              // either 1 or 0 depending on if
    if (fixRead)
    {                                  // fixPin is high or low, respectively
      countOnes++;
    }
    smartdelay(0);
    delay(1);
  }
  
  ScountOnes = String(countOnes);                 // 'S'countOnes as in 'String' countOnes...
  Serial.println("countOnes = " + ScountOnes);    // print how many countOnes we had

  // these conditionals determine whether we return hasFix or noFix
  if (countOnes > 300)
  {
    countOnes = 0;
    return 0;
  }
  else
  {
    countOnes = 0;
    return 1;
  }
  
}


// function to extract nuclear time from satellites
static void getTime(TinyGPS &gps, int time[4])
{
  int year;
  byte month, day, hour, minute, second, hundredths;
  unsigned long age;
  gps.crack_datetime(&year, &month, &day, &hour, &minute, &second, &hundredths, &age);
  smartdelay(0);

  // pack timestamp (sans miliseconds) into time array
  time[0] = int(hour);
  time[1] = int(minute);
  time[2] = int(second);
//time[3] = 0 or 1, indicating am or pm (respectively), depending on lines below

  // multiple conditionals to clean up hour value
  time[0] += hoursRelativeUTC;  // adjust UTC hour reading into local hour
  
  if (time[0] < 0)
  {                             // if, after we adjust from UTC time, we get a negative hour,
    time[0] += 24;              // lets push the time forward 24 hours so the number is positive and correct
  }

  // we don't run on military time, so fix 0 hours to 12 (am)
  if (time[0] == 0)
  {
    time[0] = 12;
  }

  // If time is PM, then subtract 12 to get human hour and make time[3] = 1 to indicate PM
  if (time[0] > 12)
  {
    time[0] -= 12;
    time[3] = 1;
  }
  else
  {
    time[3] = 0;          // if time is not PM, then it's AM, and make time[3] = 0 to indicate AM
  }
}

// get an analog reading from the ADC
// ADC on ESP8266 is 10 bits (0-1023), and runs from GND to 0.958 V
// Max voltage of LiPo is 4.20 V, min voltage is 2.8 V
// chosen resistors: R1=2.2ko, R2=470o
// 4.2V -> 0.74V, 2.8V -> 0.493V 
// https://www.adafruit.com/product/328
// https://forums.adafruit.com/viewtopic.php?f=19&t=74972&sid=9000a0ed6258078eb726d3f2f322f5eb
static void readADC()
{
  ADCreading = analogRead(A0);
}

