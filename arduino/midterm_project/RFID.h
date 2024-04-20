#include <SPI.h>
#include <MFRC522.h>

class RFID{
  MFRC522 *mfrc522;
  int block = 1, len = 18;
  byte buffer[18];

  public:
    RFID(int SS_PIN, int RST_PIN){
      mfrc522 = new MFRC522(SS_PIN, RST_PIN);
      mfrc522->PCD_Init();
    }

    String dump_byte_array(byte *buffer, byte bufferSize) {
      String res = "";
      for (byte i = 0; i < bufferSize; i++) {
        res += String(buffer[i], HEX);
      }
      res.toUpperCase();
      return res;
    }

    // String get_UID(){
      
    //   if( mfrc522->PICC_IsNewCardPresent() && mfrc522->PICC_ReadCardSerial() ){
        
    //     String UID = dump_byte_array(mfrc522->uid.uidByte, mfrc522->uid.size);
    //     Serial.println(UID);
    //     mfrc522->PICC_HaltA();
    //     mfrc522->PCD_StopCrypto1(); 

    //     return UID;
    //   }
    //   else{
    //     return "NONE";
    //   }
    // }


    // get the UID of RFID card in unsigned long format
    unsigned long get_UID(){ 
      if( mfrc522->PICC_IsNewCardPresent() && mfrc522->PICC_ReadCardSerial() ){
        unsigned long UID = 0;
        for(int i=0; i<4; i++){
          UID += mfrc522->uid.uidByte[i];
          UID <<= 8*(i<3);
        }
        mfrc522->PICC_HaltA();
        mfrc522->PCD_StopCrypto1(); 
        return UID;
      }
      else{
        return 0;
      }
    }

    // turn the UID of RFID card from unsigned long into char* format, returns 1 for success, 0 for fail
    // bool UID_to_string(unsigned long UID,char* UID_in_string){
    //   if(UID!=0){
    //     char upper_UID_string[6];
    //     char lower_UID_string[6];
    //     // char UID_in_string[15];
    //     int upper_UID = UID>>16;
    //     int lower_UID = (UID<<16)>>16;
    //     snprintf(upper_UID_string, 6, "%X", upper_UID);
    //     snprintf(lower_UID_string, 6, "%X", lower_UID);
    //     strcpy(UID_in_string,upper_UID_string);
    //     strcat(UID_in_string,lower_UID_string);
    //     return true;
    //   }
    //   else{
    //     return false;
    //   }
    // }

    void UID_to_byteArray(byte* byteArray, unsigned long UID){
      byteArray[0] = (byte)((UID >> 24) & 0xFF);
      byteArray[1] = (byte)((UID >> 16) & 0xFF);
      byteArray[2] = (byte)((UID >> 8) & 0xFF);
      byteArray[3] = (byte)(UID & 0xFF);
    }
};
