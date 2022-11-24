import cv2
import imutils
import numpy as np
import argparse

from imutils.object_detection import non_max_suppression
import time
from stream import *
import cv2, queue, threading
from datetime import datetime

HOGCV = cv2.HOGDescriptor()
HOGCV.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

record_url = "http://127.0.0.1:5000/add_record"

vehicle_registration = "KBU234Y"
display_url = "http://192.168.187.139" #Node mcu address
URL = "http://192.168.187.73" #Camera address 
vehicle_speed = {
    "speed": 0
}


def detect(frame):
    ## USing Sliding window concept
    rects, weights = HOGCV.detectMultiScale(frame, winStride=(4, 4), padding=(8, 8), scale=1.03)
    rects = np.array([[x, y, x + w, y + h] for (x, y, w, h) in rects])
    pick = non_max_suppression(rects, probs=None, overlapThresh=0.65)

    c = 1
    for x, y, w, h in pick:
        cv2.rectangle(frame, (x, y), (w, h), (139, 34, 104), 2)
        cv2.rectangle(frame, (x, y - 20), (w, y), (139, 34, 104), -1)
        cv2.putText(frame, f'P{c}', (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        c += 1
    
 # Sending counts to database
    data = {
        "speed": vehicle_speed["speed"],
        "number_of_people": c - 1,
        "registration": vehicle_registration

    }

    send_data = requests.post(url=record_url, json=data)


    if send_data.text != "OK":
        cv2.putText(frame, "Error sending data", (20, 10), cv2.FONT_HERSHEY_DUPLEX, 0.8, (255, 255, 255), 2)
    else:
        # Seinding data for display on the lcd (node mcu)
        speed_request = requests.get(url=display_url+"/?people="+str(c-1))
        # Get back the speed measures by the accelerometer 
        vehicle_speed["speed"] = int(speed_request.text)
    # video display
    cv2.putText(frame, f'Total Persons : {c - 1}', (20, 450), cv2.FONT_HERSHEY_DUPLEX, 0.8, (255, 255, 255), 2)
    cv2.imshow('output', frame)


    return frame



def detectByCamera():
    # Read images from camera
    
    set_resolution(url=URL, index=8) #set resolution
    
    video = VideoCapture(URL + ":81/stream") #get video from esp camera

    print('Detecting people...')

    while True:
        frame = video.read()

        frame = detect(frame)
        

        key = cv2.waitKey(1)
        if key == ord('q'):
            break

    video.release()
    cv2.destroyAllWindows() #close camera window 


if __name__ == "__main__":
    detectByCamera()
