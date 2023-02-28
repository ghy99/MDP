import bluetooth
import time
import socket
from psutil import process_iter
from signal import SIGKILL

class BluetoothAPI:
    MAC_ADDRESS = 'E4:5F:01:55:A6:C7'
    TABLET_BlUETOOTH = '90:EE:C7:E7:D0:90'
    PORT_NUMBER = 1
    READ_BUFFER_SIZE = 5096

    def __init__(self):
        self.client = None
        self.server = None

    def check_connection(self):
        return self.client is None or self.server is None

    def killBluetooth():
        for proc in process_iter():
            for conns in proc.get_connections(kind='all'):
                if conns.laddr[1] == 1:
                    proc.send_signal(SIGKILL) 
                    continue

    def connect(self):
        try:
           self.server.shutdown(2)
           self.server.close()
        except:
           print("[Bluetooth] Trying to connect to the RPI")
        while True:
            try:
                print("[Bluetooth] Attempting to connect...")

                self.server = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
                print("[Bluetooth] Initialising Server")

                self.server.bind((self.MAC_ADDRESS, self.PORT_NUMBER))

                self.server.listen(self.PORT_NUMBER)

                self.client, client_address = self.server.accept()
                print("[Bluetooth] Server Accepted")

            except Exception as exception:
                print("[Bluetooth] Connection failed: " + str(exception))
                print("[Bluetooth] Disconnecting from server")
                self.server.shutdown(1)
                self.server.close()
                time.sleep(1)
            else:
                print("[Bluetooth] Connected successfully")
                print("[Bluetooth] Client address is " + str(client_address))
                break

    def write(self, message):
        print("[Bluetooth] Attempting to send message:")
        print(message)

        try:
            self.client.send(message)
            print("[Bluetooth] Sent message:", message)
            return False
        except Exception as exception:
            print("[Bluetooth] Failed to send: " + str(exception))
            return True

    def disconnect(self):
        try:
            if self.client is not None:
                self.client.shutdown(socket.SHUT_RDWR)
                self.client.close()
                self.client = None
                print('Android - Disconnecting Client Socket')

            if self.server is not None:
                self.server.shutdown(socket.SHUT_RDWR)
                self.server.close()
                self.server = None
                print('Android - Disconnecting Server Socket')

        except Exception as e:
            print('[Android Disconnect all error] %s' % str(e))

    def read(self):
        while self.server is not None and self.client is not None:
            print("")
            print("[Bluetooth] Attempting to read...")
            try:
                message = self.client.recv(self.READ_BUFFER_SIZE)
                if message is not None and len(message) > 0:
                    print("[Bluetooth] Message read:")
                    print(message)
                    if message.decode() == "close":
                        print("[Bluetooth] Shutting down..")
                        self.server.shutdown(1)
                        self.server = None
                    return message
            except Exception as exception:
                print("[Bluetooth] Failed to read: " + str(exception))



if __name__ =='__main__':
    bluetoothapi = BluetoothAPI()
    bluetoothapi.connect()
    while True:
        command = input("Enter Command(r/close): ")
        if command == "close":
            print("Closing Serial Connection")
            server = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
            server.shutdown(2)
            server.close()
        elif command == 'r':
            msg = bluetoothapi.read()
            print("read", msg, "from bluetooth")
        else:
            command = str.encode(command)
            bluetoothapi.write(command)
