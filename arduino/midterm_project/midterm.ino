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
bool sensors_read[5];
RFID * rfid;
Motor * motor;
bool bStop = false, bStateSetting = false;
double lastError = 0.0;
String node_UID;

void Search();
void SetState();

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

// motorWrite(vL, vR) until ir sensors read the same with ir[]
void Motor::moveTill(bool* ir, int ir_size, double vL, double vR){
  bool flag = true;
  while(flag){
    motorWrite(vL, vR);
    // check if sensor values are what we wanted
    int cnt = 0;
    for(int i=0; i<ir_size; i++){
      if(sensors[i]->is_on_line() == ir[i]){
        cnt ++;
      }
    }
    if(cnt == ir_size){
      flag = 0;
    }
  }
}

void loop(){
  if (bStop) {
    motor->motorWrite(0, 0);
    Serial.println("bStop!!");
  }else
    Search();
  SetState();
  // delay(100);
}

// a l r u s
void SetState(){
  // TODO:
  // 1. Get command from bluetooth
  // 2. Change state if need
  if(!bStateSetting) return;
  char cmd = 'n';
  // while(bStateSetting){
  Serial.println("State Setting");
  if (bt->available()){
    Serial.println("read from bt");
    cmd = bt->read_data()[0];
    if(!cmd) return;
    Serial.println(cmd);
    if (cmd == 'a'){
      motor->move(120, 150, 175);
      bStop = false;
    }
    if (cmd == 'l'){
      motor->move(100, 100, 100);
      motor->move(75, 200, 50);
      bool ir[] = {0, 0, 1, 0, 0};
      motor->moveTill(ir, 5, 150, 0);
      bStop = false;
    }
    if (cmd == 'r'){
      motor->move(100, 100, 100);
      motor->move(75, 50, 200);
      bool ir[] = {0, 0, 1, 0, 0};
      motor->moveTill(ir, 5, 0, 150);
      bStop = false;
    }
    if (cmd == 'u'){
      motor->move(60, 120, 120);
      motor->move(100, -200, 200);
      bool ir[] = {0, 0, 1, 0, 0};
      motor->moveTill(ir, 5, -100, 100);
      bStop = false;
    }
    if (cmd == 'e'){
      motor->move(30, 120, 120);
      motor->motorWrite(0, 0);
      // bStop = false;
    }
    if (cmd == 's'){
      motor->move(50, 120, 120);
      bStop = false;
    }
    bStateSetting = false;
  }else{
    motor->motorWrite(0, 0);
  }
  return;
}
void Search(){
  // TODO: let your car search graph(maze) according to bluetooth command from computer
  for(int i=0; i<5; i++){
    sensors_read[i] = sensors[i]->is_on_line();
    Serial.print(sensors_read[i]);
  }
  Serial.println();
  if(!bStop)
    lastError = motor->tracking(lastError, sensors_read);
  String temp = rfid->get_UID();
  Serial.println(lastError);
  if(temp != "NONE"){
    node_UID = temp;
  }
  if(lastError == -1){ // touch node
    bStop = true;
    bt->send_data(node_UID);
    Serial.print("send UID: ");
    Serial.println(node_UID);
    bStateSetting = true;
  }
}
