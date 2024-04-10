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
    String read_data(){
      String data = "";
      if(Serial1.available()){
        data = Serial1.readString();
      }
      return data;
    }

    // send data to bluetooth module and send it
    void send_data(String data){
      Serial1.write(data.c_str());
      Serial1.write("\n");
    }
};