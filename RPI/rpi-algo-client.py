import sys
import socket

class RPiClient:
    """
    Used for connecting to RPI as client
    """
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self):
        self.socket.connect((self.host, self.port))

    def send_message(self, obj):
        for command in obj:
            self.socket.send(command.encode('utf-8'))

    def receive_message(self):
        data = self.socket.recv(1024)
        # print(data.__len__())
        if not data:
            return False
        return data.decode('utf-8')

    def close(self):
        self.socket.close()

def main():
    client = RPiClient("192.168.17.1", 6000)
    
    while True:
        try:
            print("[Algo-PC] Connecting...")
            client.connect()
            break
        except OSError:
            pass
        except Exception as e:
            print(e)
            client.close()
            sys.exit(1)
    print("[Algo-PC] Connected to PC!\n")
    
    msg = ""
    while True:
        msg = input("Enter <r> to receive or <s> to send")
        
        if msg == 'r':
            data = client.receive_message()
            print(data)
        else: 
            print("[Algo-PC] Sending data to RPI...")
            payload = [msg]
            client.send_message(payload)
    
if __name__ == '__main__':
    main()