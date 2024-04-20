#include "bluetooth.h"
#include "RFID.h"
#include "node.h"

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

enum status {
  START,
  ADVANCING,
  GOING_STRAIGHT_THROUGH,
  TURNING_LEFT,
  TURNING_RIGHT,
  U_TURNING,
  END
};

enum position{
  PATH,
  NODE
};

double lastError = 0.0;
unsigned long loop_timer = 0;
unsigned long last_UID = 0;
unsigned long last_enter_node_time = 0;
status current_status = START;
status next_status = END;
position current_position = PATH;
bool sensors_read[5];

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

  for(int i = 0 ; i < 5 ; i++){
    sensors_read[i] = false;
  }
}


status temp = START; // for debugging

// void loop(){
//     for(int i = 0 ; i < 5 ; i++){
//       Serial.print(sensors[i]->is_on_line() == true);
//       Serial.print(" ");
//     }
//     Serial.println();
// }
// void loop(){
//   unsigned long UID = rfid->get_UID();
//   if(UID!=0){
//     byte byteArray[4];
//     rfid->UID_to_byteArray(byteArray, UID);
//     bt->send_data(byteArray,4);
//     Serial.println(UID,HEX);
//   }
// }


void loop(){

  // char* UID_string;
  // UID_string = new char[15];
  // if(rfid->get_UID_string(UID_string)!=0){
  //   Serial.println(UID_string);
  // }
  if(current_status != temp){
    Serial.println(current_status);
    temp = current_status;
  }

  // Serial.println(current_status);
  switch(current_status){
    case START:
      if(bt->available() && bt->read_data() == 's'){ //if bluetooth recieved start command, switch to advancing
        current_status = ADVANCING;
        last_enter_node_time = millis();
        motor->motorWrite(120,120);
        delay(200);
      }
      break;
      

    case ADVANCING:

      while(true){
        //tracking and changing state
        if(loop_timer%2 == 0){
          char sensor_sum = 0;
          for(int i = 0 ; i < 5 ; i++){ sensors_read[i] = sensors[i]->is_on_line(); sensor_sum += sensors_read[i];}
          lastError = motor->tracking(lastError, sensors_read);

          if(current_position != NODE && sensor_sum >= 4 &&  millis() - 700 > last_enter_node_time){
            byte byteArray[1];
            byteArray[0] = 'n';
            bt->send_data(byteArray,1);
            current_position = NODE;
            current_status = next_status;
            last_enter_node_time = millis();
            break;
          }
          else if(current_position == NODE && sensor_sum <= 3 ){
            current_position = PATH;
            current_status = ADVANCING;
          }
        }

        // for UID, check every 10 loop
        if( loop_timer %10 == 0){
          byte byteArray[4];
          unsigned long UID = rfid->get_UID();
          if( UID != 0 && UID != last_UID){
            last_UID = UID;
            rfid->UID_to_byteArray(byteArray, UID);
            bt->send_data(byteArray,4);
            Serial.println(UID,HEX);
          }
        }

        //for bt, check every loop to change command in time
        if(bt->available()){
          char cmd = bt->read_data();
          Serial.println(cmd);
          switch(cmd){
            case 'a':
              next_status = GOING_STRAIGHT_THROUGH;
              break;
            case 'l':
              next_status = TURNING_LEFT;
              break;
            case 'r':
              next_status = TURNING_RIGHT;
              break;
            case 'u':
              next_status = U_TURNING;
              break;
            case 'e':
              next_status = END;
              break;
          }
        }

        loop_timer += 1;
      }
      break;

    case GOING_STRAIGHT_THROUGH:
      motor->motorWrite(255,255);
      delay(500);
      current_status = ADVANCING;
      next_status = ADVANCING;
      break;

    case TURNING_LEFT:
      motor->motorWrite(255,100);
      delay(700);
      current_status = ADVANCING;
      next_status = ADVANCING;
      break;
    case TURNING_RIGHT:
      motor->motorWrite(80,255);
      delay(700);
      current_status = ADVANCING;
      next_status = ADVANCING;
      break;
    case U_TURNING:
      motor->motorWrite(150,-150);
      delay(800);
      current_status = ADVANCING;
      next_status = ADVANCING;
      break;
    case END:
      motor->motorWrite(0,0);
      // if(bt->available() && bt->read_data() == 's'){ //if bluetooth recieved start command, switch to advancing
      //   current_status = ADVANCING;
      //   next_status = END;
      //   last_enter_node_time = millis();
      // }
      break;

    default:
      break;
  }
  
}
