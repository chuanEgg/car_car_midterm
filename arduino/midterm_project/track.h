class IR_sensor{
  int pin_num ,value;

  public:
    IR_sensor(int num):pin_num(num){
      pinMode(pin_num, INPUT); 
    }

    int is_on_line(){
      return digitalRead(pin_num)>0;
    }
};

class Motor{
  int AIN1, AIN2, BIN1, BIN2, PWMA, PWMB, STBY;
  double wL2 = -2, wL1 = -1, wM = 0, wR1 = 1, wR2 = 2, diff = 1;

  public:
    Motor(int AIN1, int AIN2, int  BIN1, int BIN2, int PWMA, int PWMB, int STBY){
      this->AIN1 = AIN1;
      this->AIN2 = AIN2;
      this->BIN1 = BIN1;
      this->BIN2 = BIN2;
      this->PWMA = PWMA;
      this->PWMB = PWMB;
      this->STBY = STBY;

      pinMode(AIN1,OUTPUT);
      pinMode(AIN2,OUTPUT);
      pinMode(BIN1,OUTPUT);
      pinMode(BIN2,OUTPUT);
      pinMode(PWMA,OUTPUT);
      pinMode(PWMB,OUTPUT);
      pinMode(STBY,OUTPUT);
    }

    void motorWrite(double vL, double vR){
      vL = vL>255 ? 255 : vL;
      vL = vL<-255 ? -255 : vL;
      vR = vR>255 ? 255 : vR;
      vR = vR<-255 ? -255 : vR;
      vR *= 0.9*diff;
      vL *= diff;
      if(vL>=0){
        digitalWrite(STBY, HIGH);
        digitalWrite(AIN1, LOW);
        digitalWrite(AIN2, HIGH);
        analogWrite(PWMA,vL);
      }
      else{
        digitalWrite(STBY, HIGH);
        digitalWrite(AIN1, HIGH);
        digitalWrite(AIN2, LOW);
        analogWrite(PWMA,vL*-1);
      }
      if(vR>=0){
        digitalWrite(STBY, HIGH);
        digitalWrite(BIN1, LOW);
        digitalWrite(BIN2, HIGH);
        analogWrite(PWMB,vR);
      }
      else{
        digitalWrite(STBY, HIGH);
        digitalWrite(BIN1, HIGH);
        digitalWrite(BIN2, LOW);
        analogWrite(PWMB,vR*-1);
      }
    }
    void stop(){
      digitalWrite(STBY, LOW);
    }

    double tracking(double lastError, bool* bSensors){
      int L2 = bSensors[0];
      int L1 = bSensors[1];
      int M = bSensors[2];
      int R1 = bSensors[3];
      int R2 = bSensors[4];
      double error = 0.0;
      if(L2||L1||M||R1||R2){
        error = (wL2*L2 + wL1*L1 + wM*M + wR1*R1 + wR2*R2)/(L1+L2+M+R1+R2);
        // error = (L1+L2+M+R1+R2)*1.0;
      }
      double Kp = 100, Tp = 255, Kd = 10;
      // Kd is not tuned yet
      double correction = Kp*error + Kd*(error-lastError);
      double vL = Tp - correction;
      double vR = Tp + correction;
      motorWrite(vL, vR);
      return error;
    }
};