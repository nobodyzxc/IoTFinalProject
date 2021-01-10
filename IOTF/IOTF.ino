
#include <Servo.h>
#include <Wire.h>
#include "rgb_lcd.h"

rgb_lcd lcd;
Servo myservo;
int open_pos = 90;
int close_pos = 0;

void LCD_text(String text,int line){
  lcd.clear();
  lcd.setCursor(0, line);
  lcd.print(text);
  delay(100);
}

void setup() {
  Serial.begin(9600);
  myservo.attach(9);
  lcd.begin(16, 2);
  lcd.setRGB(0, 0, 255);
  myservo.write(0);
}

void loop() {
  if (Serial.available() > 0) {
    char com = Serial.read();
    if (com=='H') {
      //      LCD_text("open",0);
      myservo.write(open_pos);
    }
    else if (com=='L') {
      //      LCD_text("close",0);
      myservo.write(close_pos);
    }
    else if (com=='C') {
      lcd.setRGB(0, 0, 255);
      lcd.clear();
    }
    else if (com=='A') {
      String user;
      lcd.setRGB(0, 255, 0);
      LCD_text("Access",0);
      if (Serial.available() >0) {
        //          char c = Serial.read();
        //          LCD_text("debug",0);
        user = Serial.readString();
      }

      lcd.setCursor(0, 1);
      lcd.print("Welcome ");
      lcd.setCursor(9, 1);
      if (user.length() >0) lcd.print(user);
    }
    else if (com=='B') {
      lcd.setRGB(255, 0, 0);
      LCD_text("Error",0);
    }
  }
  delay(100);
}
