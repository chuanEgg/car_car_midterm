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

    String get_UID(){
      
      if( mfrc522->PICC_IsNewCardPresent() && mfrc522->PICC_ReadCardSerial() ){
        
        String UID = dump_byte_array(mfrc522->uid.uidByte, mfrc522->uid.size);
        Serial.println(UID);
        mfrc522->PICC_HaltA();
        mfrc522->PCD_StopCrypto1(); 

        return UID;
      }
      else{
        return "NONE";
      }
    }
};