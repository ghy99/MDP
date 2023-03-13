import time
import imagezmq
from picamera2 import Picamera2, Preview
import numpy as np
import cv2
import socket
from imutils.video import VideoStream

count=0
sender = imagezmq.ImageSender(connect_to="tcp://192.168.17.15:50000")
rpi_name = socket.gethostname()
cam = Picamera2()
config = cam.create_preview_configuration(main={"size":(1000,1000)})
cam.configure(config)
cam.start()
print("[Image] Start Taking Photo")
time.sleep(1.0)
while count<2:
        time.sleep(2)
        image = cam.capture_array()
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        print("[Image]Finished taking picture and sending photo...")
        result = sender.send_image(rpi_name, image)
        print("[Main] Received result:", result)
        if b'38' in result:
            print("Result is R")
            count+= 1
        elif b'39' in result:
            print("Result is L")
            count+=1
        else:
            print("Nothing Detected!")
cam.close()
