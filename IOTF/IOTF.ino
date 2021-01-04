
#include <Servo.h>
#include <Wire.h>
#include "rgb_lcd.h"

const int colorR = 255;
const int colorG = 0;
const int colorB = 0;
rgb_lcd lcd;
Servo myservo;
int open_pos = 160;
int close_pos = 0;

void LCD_text(String text,int line){
    lcd.setCursor(0, line);
    lcd.print(text);
    delay(3000);
    lcd.clear();
}
void setup() {
  Serial.begin(9600);
  myservo.attach(9);
  lcd.begin(16, 2);
  lcd.setRGB(colorR, colorG, colorB);
  LCD_text("hello, world!",0);
}

void loop() {
  if (Serial.available() > 0) { 
    char com = Serial.read();
    if (com=='H') {
      LCD_text("open",0);
      myservo.write(open_pos);
    }
    else if (com=='L') {
      LCD_text("close",0);
      myservo.write(close_pos);
    }
    else if (com=='A') {
      String user;
      LCD_text("Access",0);
        if (Serial.available() >0) {
//          char c = Serial.read();
          LCD_text("debug",0);
          user = Serial.readString();
        } 
      lcd.setCursor(0, 0);
      lcd.print("Welcome ");
      lcd.setCursor(9, 0);
      if (user.length() >0) lcd.print(user);
      delay(5000);
      lcd.clear();
    }
    else if (com=='B') {
      LCD_text("Error",0);
    }
  }
  delay(100);     
  }