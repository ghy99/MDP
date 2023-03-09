import time
import threading

from bluetoothapi import BluetoothAPI
from serialapi import SerialAPI
import RPi.GPIO as GPIO
import atexit
import socket
import imagezmq
from picamera2 import Picamera2, Preview
import cv2
import numpy as np

class Multithreader:
    
    def __init__(self):
        self.bluetoothapi = BluetoothAPI()
        self.serialapi = SerialAPI()
    
    #Function to start all the threads
    def initialize_processes(self):
        print("[Main] Attempting to initialize multithreader...")
        #Connect the different components
        self.serialapi.connect()
        self.bluetoothapi.connect()

        #Run the multithreading
        self.read_bluetooth_process = threading.Thread(target=self.read_bluetooth)
        self.read_image_process = threading.Thread(target=self.read_image)

        self.read_bluetooth_process.start()
        self.read_image_process.start()
        print("[Main] Initialized multithreader successfully")

        self.read_bluetooth_process.join()
        self.read_image_process.join()

    #Function to take picture, send to the image server and handle result
    def read_image(self):
        global takePic
        global running
        global start
        try:
            #sender = imagezmq.ImageSender(connect_to="tcp://192.168.17.15:50000")#jie kai laptop
            sender = imagezmq.ImageSender(connect_to="tcp://192.168.17.30:50000")#sishi laptop
            rpi_name = socket.gethostname()
            cam = Picamera2()
            config = cam.create_preview_configuration(main={"size":(720,720)})
            cam.configure(config)
            cam.start()
            print("[Image] Start Taking Photo")
            time.sleep(1.0)
            result = ("38".encode('utf-8'))
            while result!=b'N':
                if takePic:
                    time.sleep(2)
                    image = cam.capture_array()
                    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                    print("[Image]Finished taking picture and sending photo...")
                    result = sender.send_image(rpi_name, image)
                    print("[Main] Received result:", result)
                    if b'38' in result:
                        print("Sending R to STM")
                        self.serialapi.write("R".encode("utf-8"))
                        takePic = False
                    elif b'39' in result:
                        print("Sending L in STM")
                        self.serialapi.write("L".encode("utf-8"))
                        takePic = False
                    elif b'00' in result:
                        print("It is a bullseye!")
                        continue
                    else: 
                        print("Unable to recognise!")
                        continue
        except Exception as error:
            print("Image Recognition Error!")
            print(error)


    #Function to read messages for bluetooth and stop the function after start is read
    def read_bluetooth(self):
        global takePic
        global running
        global start
        while start:
            message = self.bluetoothapi.read()
            if message is not None and len(message) > 0:               
                print("[Main] Message recieved from bluetooth", message)
                try:
                  if b'SP' in message:
                      #Tell STM to move
                      self.serialapi.write(("SP").encode("utf-8"))
                      #wait for stm acknowledgement
                      ack = None
                      while ack is None:
                        ack = self.serialapi.read()
                        print("Received from STM", ack)
                        if  b'A' in ack:
                            ack = "A"
                            start=False
                            break
                except:
                      print("[ERROR] Invalid message from bluetooth")
        while running and takePic==False:
            smessage = self.serialapi.read()
            if(smessage is not None and b'P'in smessage):
                print("[Main] Message recieved from STM", message,"|Taking Pic Now")
                takePic=True
                self.read_image()
        exit()
                     
    #Clean up operation after we exit the programme
    def clean_up(self):
        GPIO.cleanup()


if __name__ == "__main__":
    takePic = False
    readSTM = False
    running = True
    start = True
    currentObs = 1

    #Running the programme
    mt = Multithreader()
    atexit.register(mt.clean_up)

    time.sleep(1)

    mt.initialize_processes()


