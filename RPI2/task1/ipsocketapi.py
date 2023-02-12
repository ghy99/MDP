import socket
import time

class IPSocketAPI:
    READ_BUFFER_SIZE = 2048

    def __init__(self):
        self.client = None
        self.server = None
        self.client_address= None

    def check_connection(self):
        return self.client is None or self.server is None

    def connect(self):
        while True:
            print("[Algorithm] Attempting to connect...")
            try:
                self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                self.server.bind(('192.168.17.1', 6000))
                self.server.listen()
                print("Listening...")
                self.client, self.client_address = self.server.accept()
                #self.server= socket.socket()
                #print("Connecting")
                #self.server.connect(('192.168.17.20',6000))
                print("Connected"+str(self.client_address))
                #self.server.listen(1)
                
            except Exception as exception:
                print("[Algorithm] Connection failed: " + str(exception))

                time.sleep(3)
            else:
                print("[Algorithm] Connected successfully")
                print("[Algorithm] Client address is " + str(self.client_address))

                break

    def write(self, message):
        print("[Algorithm] Attempting to send message:")
        print(message)

        try:
            self.client.send(message)
        except Exception as exception:
            print("[Algorithm] Failed to send: " + str(exception))

    def read(self):
        print("")
        print("[Algorithm] Attempting to read...")

        try:
            message = self.client.recv(self.READ_BUFFER_SIZE)
        except Exception as exception:
            print("[Algorithm] Failed to read: " + str(exception))
        else:
            if message is not None and len(message) > 0:
                print("[Algorithm] Message read:")
                print(message)

                return message


if __name__ == '__main__':
    ipsocketapi = IPSocketAPI()
    try:
       ipsocketapi.server.close()
    except:
       print("not connected")
    ipsocketapi.connect()

    #while True:
    message = "ALG|10,6,S"
    ipsocketapi.write(message.encode('utf-8'))
    ipsocketapi.write('\n'.encode('utf-8'))
    while True:
        msg = input("write sth")
        if msg == 'r':
           ipsocketapi.read()
        else:
           ipsocketapi.write(msg.encode('utf-8'))
           ipsocketapi.write('\n'.encode('utf-8'))

