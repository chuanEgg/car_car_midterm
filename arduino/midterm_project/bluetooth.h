class Bluetooth{
  public:
    Bluetooth(){
      Serial1.begin(9600);
    }

    // check if there is data to read from buffer
    bool available(){
      return Serial1.available() > 0;
    }

    // read data from buffer
    char read_data(){
      return (char)Serial1.read();
    }

    // send data to bluetooth module and send it
    void send_data(String data){
      Serial1.write(data.c_str());
      Serial1.write('\n');
    }

    void send_data(char* data){
      Serial1.write(data);
      Serial1.write('\n');
    }

    void send_data(byte* byteArray, int size){
      for(int i = 0 ; i < size ; i++){
        Serial1.write(byteArray[i]);
      }
      Serial1.write('\n');
    }
};
