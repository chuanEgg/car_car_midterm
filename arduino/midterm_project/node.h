#include "track.h"

// void turn2(Motor* motor, char cmd){
//   switch()
// }

void turn (Motor* motor, char cmd) {
  if (cmd == 'a'){
    motor->move(120, 150, 175);
  }
  if (cmd == 'l'){
    motor->move(100, 100, 100);
    motor->move(75, 200, 50);
    bool ir[] = {0, 0, 1, 0, 0};
    motor->moveTill(ir, 5, 150, 0);
  }
  if (cmd == 'r'){
    motor->move(100, 100, 100);
    motor->move(75, 50, 200);
    bool ir[] = {0, 0, 1, 0, 0};
    motor->moveTill(ir, 5, 0, 150);
  }
  if (cmd == 'u'){
    motor->move(60, 120, 120);
    motor->move(100, -200, 200);
    bool ir[] = {0, 0, 1, 0, 0};
    motor->moveTill(ir, 5, -100, 100);
  }
  if (cmd == 'e'){
    motor->move(30, 120, 120);
    motor->motorWrite(0, 0);
  }
  if (cmd == 's'){
    motor->move(10, 120, 120);
    bool ir[] = {0, 0, 1, 0, 0};
    motor->moveTill(ir, 5, 120, 124);
  }
  return;
}
