#define FASTLED_ALLOW_INTERRUPTS 0
#include "FastLED.h"
#include <EEPROM.h>

// How many leds in your strip?
#define NUM_LEDS 60
#define DATA_PIN 13
#define CLOCK_PIN 14
#define COLOR_ORDER RGB
#define BLINKEAREA 3
int incrementer = 255/NUM_LEDS;
CHSV startcolor(100, 255, 255);
CRGB leds[NUM_LEDS];
int h = 0;
typedef struct {
  int currentBrightness = 0;
  int targetBrightness = 0;
  int updown;
  CHSV color = startcolor; 
} blinkeblinke, *pblinkeblinke;

blinkeblinke myLeds[10];


void newBlink(int pos) {
  for (int i = 0; i < BLINKEAREA; i++) { 
    if (pos-i > 0 and pos-i < NUM_LEDS) { 
      myLeds[pos-i].targetBrightness = BLINKEAREA - i;
      myLeds[pos-i].updown = 1;
    }
  }
}

void blinkMe() {
  for (int i = 0; i < sizeof(myLeds); i++) {
    if (myLeds[i].currentBrightness != myLeds[i].targetBrightness) {
      myLeds[i].currentBrightness = myLeds[i].currentBrightness + myLeds[i].updown;
    }
    if (myLeds[i].currentBrightness == myLeds[i].targetBrightness) {
      myLeds[i].targetBrightness = 0;
      if (myLeds[i].currentBrightness == 0) {
       myLeds[i].updown = 0;
      }
      else {
        myLeds[i].updown = -1;
      }
    }
    myLeds[i].color.v += (50*myLeds[i].updown*myLeds[i].currentBrightness); 
   }
}

void setup() {
  Serial.begin(9600);
  // put your setup code here, to run once:
  FastLED.addLeds<APA102, DATA_PIN, CLOCK_PIN, RGB>(leds, NUM_LEDS);
  
}



void loop() {


  
 for (int i = 0; i < sizeof(myLeds); i++) {
  leds[i]  =  myLeds[i].color;  
  //Serial.println(myLeds[i].color);
  }
  FastLED.show();
 
  if (random(10) % 5 == 0) {
     newBlink(random(NUM_LEDS));
  }

  delay(10000);

}
