import serial
import time

class SerialAPI:
    SERIAL_PORT = '/dev/ttyUSB0'
    BAUD_RATE = 115200
    
    def __init__(self):
        
        self.serial_connection = None
    
    def check_connection(self):
        return self.serial_connection is None
    
    def connect(self):
        while True:
            try:
                print("[STM] Attempting to connect...")
                
                self.serial_connection = serial.Serial(self.SERIAL_PORT, self.BAUD_RATE)
            except Exception as exception:
                print("[STM] Connection failed: " + str(exception))
                
                time.sleep(1)
            else:
                print("[STM] Connected successfully")
                
                break
    
    def write(self, message):
        print("[STM] Attempting to send message:")
        print(message)
        
        try:
            self.serial_connection.write(message)
            print("[STM] Successfully sent to STM")
        except Exception as exception:
            print("[STM] Failed to send: " + str(exception))
    
    def read(self):
        print("")
        print("[STM] Attempting to read...")
        message = None
        try:
            message = self.serial_connection.read_until(b'A')
        except Exception as exception:
            print("[STM] Failed to read: "  + str(exception))
        else:
            if message is not None and len(message) > 0:
                print("[STM] Message read:")
                print(message)
                
                return message

    def removeSpaces(self,message):
        stringMessage = str(message,"UTF-8")
        
        stringMessage = stringMessage.replace(" ","")
        message = stringMessage.encode()
        
        return message
    
        
        
    
if __name__ =='__main__':
    serialapi = SerialAPI()
    serialapi.connect()
    
    while True:
        command = input("Enter Command: ")
        if command == "close":
            print("Closing Serial Connection")
            serialapi.serial_connection.close()
            exit()
        command = str.encode(command)
        serialapi.write(command)
        print("Sent", command)
       # serialapi.read()
