import multiprocessing
import time
import threading

from bluetoothapi import BluetoothAPI
from ipsocketapi import IPSocketAPI
from serialapi import SerialAPI
from imageapi import ImageAPI
import RPi.GPIO as GPIO
import atexit
import queue


class Multithreader:
    
    def __init__(self):
        self.bluetoothapi = BluetoothAPI()
        #self.ipsocketapi = IPSocketAPI()
        self.serialapi = SerialAPI()
        #self.imageClientapi = ImageAPI()
        self.write_message_queue = multiprocessing.Queue()
        self.obstacle_id = None
        
    #Function to start all the threads
    def initialize_processes(self):
        global takePictureNow
        global imageQueue
        print("[Main] Attempting to initialize multithreader...")
        self.serialapi.connect()
        #Connect the different components
        #self.ipsocketapi.connect()
        self.bluetoothapi.connect()

        #Run the multithreading
        self.read_bluetooth_process = threading.Thread(target=self.read_bluetooth)
        #self.read_ipsocket_process = threading.Thread(target=self.read_ipsocket)
        #self.read_image_process = threading.Thread(target=self.takePicture)
        self.write_process = threading.Thread(target=self.write)
        self.handleIQ_process = threading.Thread(target=self.handleImageQueue)

        #self.read_ipsocket_process.start()
        self.read_bluetooth_process.start()
        #self.read_image_process.start()
        self.write_process.start()
        self.handleIQ_process.start()
        print("[Main] Initialized multithreader successfully")

        #self.read_ipsocket_process.join()
        self.read_bluetooth_process.join()
        #self.read_image_process.join()
        self.write_process.join()
        self.handleIQ_process.join()

    #Function to take picture and add to the imageQueue
    def takePicture(self):
        global running
        global takePictureNow
        global imageQueue

        while running:
            if takePictureNow == True:
                obstacle_id = self.obstacle_id
                print(f"[Image] Taking the picture for {obstacle_id}")
                takenPicture = self.imageClientapi.rpiTakePicture()
                print(f"[Image] Successfully taken the photo for {obstacle_id}")
                imageQueue.put([takenPicture,obstacle_id])
                takePictureNow = False

    #Function to send the images to the image server and update the result when it comes back
    def handleImageQueue(self):
        global obstacleCounter
        global reccedImages
        global running
        while running:
            if not imageQueue.empty():
                print(f"[Main] Current Queue: {imageQueue}")
                currentQ = imageQueue.get()
                takenPicture = currentQ[0]
                obstacle_id = currentQ[1]
                print("[Main] Sending Image to Server")
                image_id = self.imageClientapi.sendPictureToServer(takenPicture)
                image_id = str(image_id)
                print("[Main] Image ID:", image_id)
                iMsg = image_id.encode('utf-8')
                print("[Main] Sending the picture to ipsocket")
                iMsg = self.convert_to_dict('I', iMsg)
                self.write_message_queue.put(iMsg)

                reccedImages.append(image_id)
                obstacleCounter -=1

                if image_id != '00': #if the message is valid, send results to android
                    print("[Bluetooth] Sending the image results to android")
                    bMsg = "AND_IMG|"+str(obstacle_id)+","+str(image_id)
                    print("[Bluetooth] Message sent to android:",bMsg)
                    bMsg = self.convert_to_dict('B', bMsg)
                    self.write_message_queue.put(bMsg)
                print(f"[Main] Number of obstacles left {obstacleCounter}")
                if obstacleCounter == 0:
                    iMsg = "DONE".encode('utf-8')
                    print("[Main] Sending DONE to ipsocket")
                    iMsg = self.convert_to_dict('I', iMsg)
                    self.write_message_queue.put(iMsg)

    #Function to read messages from the Android tablet
    def read_bluetooth(self):
        global obstacleCounter
        global numObstacle
        global running
        global bluetoothOn
        global firstTime
        global firstMessage

        while running and bluetoothOn:
            message = self.bluetoothapi.read()
            if message is not None and len(message) > 0:               
                print("[Main] Message recieved from bluetooth", message)
                try:
                  if b'ALG' in message:
                      obstacleCounter = len(message.decode('utf-8').split('|'))-1
                      numObstacle = obstacleCounter
                      print(f"[Main] The number of obstacles is {obstacleCounter}")
                      message = self.convert_to_dict('I', message) #Forwarding entire string to algo
                      self.write_message_queue.put(message)
                  elif b'START' in message:
                      firstTime = False
                      message = firstMessage.decode('utf-8')
                      print("[Main] First message decoded")
                      print("[Main] Message to be sent to STM:",message)
                      parts = message.split('&')
                      stm_message = self.convert_to_dict('S', parts[0])
                      self.write_message_queue.put(stm_message)
                      print("[Main] Going to process",stm_message)
                      and_message = self.convert_to_dict('B', parts[1])
                      self.write_message_queue.put(and_message)
                      print("[Main] Sending", and_message, "to Android")
                  elif b'STM' in message:
                      message = message.decode('utf-8')
                      parts = message.split(':')
                      #stm_message = self.convert_to_dict('S', parts[0])
                      #self.write_message_queue.put(stm_message)
                      #print("[Main] Going to process",stm_message)
                      and_message = self.convert_to_dict('S',"STM,"+ parts[1])
                      self.write_message_queue.put(and_message)
                      print("[Main] Sending", and_message, "to STM")
                except:
                      print("[ERROR] Invalid message from bluetooth")
                
    #Function to read messages from Algorithm
    def read_ipsocket(self):
        global reccedImages
        global numObstacle
        global running
        global firstMessage

        while running:
            message = self.ipsocketapi.read()
            if message is not None and len(message) > 0:
                if firstTime:
                    firstMessage = message
                else:
                  if b'STM' in message:
                      message = message.decode()
                      print("[Main] Message to be sent to STM:",message)
                      parts = message.split('&')
                      stm_message = self.convert_to_dict('S', parts[0])
                      self.write_message_queue.put(stm_message)
                      print("[Main] Going to process",stm_message)

                      and_message = self.convert_to_dict('B', parts[1]) 
                      self.write_message_queue.put(and_message)
                      print("[Main] Sending", and_message, "to Android")
                  elif b'IMG' in message: #Taking picture with the camera
                      stringMessage = str(message)
                      obstacle_id = stringMessage.split("|")[1][:-1]
                      print("[Main] Obstacle ID:", obstacle_id)
                      self.obstacle_id = obstacle_id
                      print("[Main] Setting take picture now to be true")
                      global takePictureNow
                      takePictureNow = True
                      print("Continuing with algo")

                  elif b"RPI_END" in message:
                      while True:
                          if len(reccedImages) == numObstacle:
                              time.sleep(5)
                              self.imageClientapi.sendEmptyImage()
                              print("[Image] Closing camera")
                              self.imageClientapi.imageClose()
                              print("[Main] Disconnecting from IP Socket")
                              self.ipsocketapi.server.close()
                              print("[Main] Disconnecting from Bluetooth")
                              self.bluetoothapi.server.shutdown(2)
                              self.bluetoothapi.server.close()
                              running = False
                              exit()
                              break

                  elif message == b"K":
                      print("[Main] Acknowledged by Algo")
                  else:
                      print("[Main] Invalid command", message ,"read from Algo")

    #Protocol to reconnect with Android tablet
    def reconnect_android(self):
        print("[Main] Attempting to reconnect")
        self.bluetoothapi.disconnect()

        global writeOn
        global bluetoothOn
        writeOn = False
        bluetoothOn = False

        self.bluetoothapi.connect()
        print("[Bluetooth] BT successfully reconnected")

        writeOn = True
        bluetoothOn = True


        # call multiprocess and start
        self.read_android_process = threading.Thread(target=self.read_bluetooth)
        self.read_android_process.start()
        self.read_android_process.join()
        self.write_process = threading.Thread(target=self.write)
        self.write_process.start()
        self.write_process.join()

        print("Reconnected to android...")

    

    #Function for writing messages to the different components                    
    def write(self):
        global running
        global writeOn
        while running and writeOn:
            try:
                if self.write_message_queue.empty():
                    continue

                message = self.write_message_queue.get()
                print(message)
                header = message["header"]
                body = message["body"]
                
                if header == "B": #Android
                    print("[Main] Sending ",body," to Android")
                    failed = self.bluetoothapi.write(body)
                    self.bluetoothapi.write(' '.encode('utf-8'))
                    if failed:
                        print("[Bluetooth] Attempting to reconnect bluetooth")
                        self.reconnect_android(self)

                elif header == "I": #Algo
                    print("[Main] Sending", body, "to IpSocket")
                    self.ipsocketapi.write(body)
                    self.ipsocketapi.write('\n'.encode('utf-8'))

                elif header == "S": #STM
                    print(f"[Main] STM processing started body {body}")
                    try:
                      if "STM" in body:
                          #moves = body[3:].split(',')
                          moves = list(body[4:])
                          print(moves)
                          for i in moves:
                                  i  = str.encode(i)
                                  print("After encode",i)
                                  self.serialapi.write(i)
                                  print("[Main] Sending ",i," to STM")
                                  #ack = None
                                  """
                                  while ack is None:
                                      ack = self.serialapi.read()
                                      print("Received from STM", ack)
                                      if  b'AAAA' not in ack:
                                          ack = None
                          
                          self.ipsocketapi.write("K".encode('utf-8'))
                          self.ipsocketapi.write("\n".encode('utf-8'))
                          """
                    except: 
                          print("Sending STM", body)
                          i = str.encode(body)
                          self.serialapi.write(i)
                else:
                    print("[Main] Invalid header " + str(header))
                
                print("[Main] Message sent")
            except Exception as exception:
                print("[Main] Error occurred in write: " + str(exception))
                time.sleep(1)
                
    #Converting to a dictionary to store in the queue
    def convert_to_dict(self, header, body):
        return {"header": header, "body": body}

    #Clean up operation for when the programme is closed midway
    def clean_up(self):
        GPIO.cleanup()


if __name__ == "__main__":
    #Defining global variables
    takePictureNow = False
    imageQueue = queue.Queue(6)
    obstacleCounter = None
    numObstacle = None
    reccedImages = []
    bluetoothOn = True
    writeOn = True
    running = True
    firstTime = True
    firstMessage = ""

    #Running the programme
    mt = Multithreader()
    atexit.register(mt.clean_up)

    time.sleep(2)

    mt.initialize_processes()


