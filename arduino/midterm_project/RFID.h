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
        res += (buffer[i] < 0x10 ? " 0" : " ");
        res += String(buffer[i], HEX);
        // Serial.print(buffer[i] < 0x10 ? " 0" : " ");
        // Serial.print(buffer[i], HEX);
      }
      res = HexString2ASCIIString(res);
      return res;
    }

    String HexString2ASCIIString(String hexstring) {
      String temp = "", sub = "", result;
      char buf[3];
      for(int i = 0; i < hexstring.length(); i += 2){
        sub = hexstring.substring(i, i+2);
        sub.toCharArray(buf, 3);
        char b = (char)strtol(buf, 0, 16);
        if(b == '\0')
          break;
        temp += b;
      }
      return temp;
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
        return "\0";
      }
    }
};