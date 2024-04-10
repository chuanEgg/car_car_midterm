#include "bluetooth.h"
#include "track.h"
#include "RFID.h"

#define pin_PWMA 12
#define pin_PWMB 13
#define pin_AIN1 2
#define pin_AIN2 3
#define pin_BIN1 4
#define pin_BIN2 5
#define pin_STBY 6
#define pin_IR1 32
#define pin_IR2 34
#define pin_IR3 36
#define pin_IR4 38
#define pin_IR5 40
#define pin_RFID_SS 53
#define pin_RFID_RST 9
#define pin_BT_RX 18
#define pin_BT_TX 19

Bluetooth * bt;
IR_sensor * sensors[5];
RFID * rfid;
Motor * motor;

void setup() {
  Serial.begin(9600);
  SPI.begin();
  sensors[0] = new IR_sensor(pin_IR1);
  sensors[1] = new IR_sensor(pin_IR2);
  sensors[2] = new IR_sensor(pin_IR3);
  sensors[3] = new IR_sensor(pin_IR4);
  sensors[4] = new IR_sensor(pin_IR5);
  rfid = new RFID(pin_RFID_SS, pin_RFID_RST);
  motor = new Motor(pin_AIN1, pin_AIN2, pin_BIN1, pin_BIN2, pin_PWMA, pin_PWMB, pin_STBY);
  bt = new Bluetooth();
}

void loop(){
  rfid->get_UID();
}
