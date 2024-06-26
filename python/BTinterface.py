import logging,time,sys
from typing import Optional

from BT import Bluetooth

from maze import Action

log = logging.getLogger(__name__)

# hint: You may design additional functions to execute the input command,
# which will be helpful when debugging :)


class BTInterface:
    def __init__(self, port: Optional[str] = None):
        log.info("Arduino Bluetooth Connect Program.")
        self.bt = Bluetooth()
        if port is None:
            port = input("PC bluetooth port name: ")
        while not self.bt.do_connect(port):
            if port == "quit":
                self.bt.disconnect()
                quit()
            port = input("PC bluetooth port name: ")

    def start(self):
        input("Press enter to start.")
        # self.bt.serial_write_string("s")
        # time.sleep(1)

    def get_UID(self): #old one
        UID = self.bt.serial_read_byte()
        #return self.process_UID(UID)
        return self.process_UID_ver2(UID)
    
    def get_data(self): #new one, returns the string of received data 
        data = str(self.bt.serial_read_byte())
        data = data[2:-2]
        data.upper()
        return data
        

    def send_action(self, dirc : Action):
        # TODO : send the action to car
        
        if(dirc == Action.ADVANCE):
            dirc = b'a'
        elif(dirc == Action.TURN_LEFT):
            dirc = b'l'
        elif(dirc == Action.TURN_RIGHT):
            dirc = b'r'
        elif(dirc == Action.U_TURN):
            dirc = b'u'
        elif(dirc == Action.START):
            dirc = b's'
        elif(dirc == Action.HALT):
            dirc = b'e'
            
        self.bt.serial_write_bytes(dirc)
        return

    def end_process(self):
        # time.sleep(2)
        # self.bt.serial_write_string("e")
        # time.sleep(2)
        self.bt.disconnect()
        
        
    def process_UID(self,unprocessed_UID : str):
        UID = ""
        if(unprocessed_UID):
            for i in range(1,int(len(unprocessed_UID)/2)-1):
                partial_integer = int(( "0x" + unprocessed_UID[i*2:i*2+2]),16)
                UID += chr(partial_integer)
        return UID

    def process_UID_ver2(self,unprocessed_UID : bytes):
        UID = str(unprocessed_UID)
        UID = UID[2:-2]
        UID.upper()
        return UID

if __name__ == "__main__":
    test = BTInterface()
    test.start()
    test.end_process()
