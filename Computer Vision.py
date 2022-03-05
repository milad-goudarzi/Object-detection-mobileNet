#!/usr/bin/env python
# coding: utf-8

# # Object detection and data transmission over Bluetooth

# In[1]:


from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input, decode_predictions
import numpy as np
import cv2
import socket

mode1=MobileNetV2(weights='imagenet')

HEADERSIZE = 10

hostMACAddress = '30:e3:7a:ef:bc:34' # The MAC address of a Bluetooth adapter on the server. The server might have multiple Bluetooth adapters.
port = 4 # 3 is an arbitrary choice. However, it must match the port used by the client.
backlog = 5
size = 1024
s = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
s.bind((hostMACAddress,port))
s.listen(backlog)
try:
    print("waiting for connection requests")
    client, address = s.accept()
    print("connection established")

    def inference(x):
        x=np.expand_dims(x, axis=0)
        x=preprocess_input(x)
        preds=mode1.predict(x)
        return decode_predictions(preds,top=1)[0][0][1]
    cap=cv2.VideoCapture(0)
    prev_prediction = "nothing"
    while True:
        
        ret, frame=cap.read()
        frame=cv2.resize(frame,(224,224))
        predicted=inference(frame[...,::-1])
        if predicted != prev_prediction and (predicted == "tripod" or predicted == "sunglasses"):
            msg = predicted + " detected!"
            msg = f'{len(msg):<{HEADERSIZE}}' + msg
            client.send(bytes(msg, "utf-8"))
            prev_prediction = predicted
        
    #   client.put("test.txt", predicted)
        cv2.putText(frame, predicted, (5 , 30), cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,0,255),lineType=cv2.LINE_AA)
        frameout=cv2.resize(frame,(650,600))
        cv2.imshow('Webcam', frameout)
        if cv2.waitKey(1) == 13:
    #	client.disconnect()
            break
    cap.release()
    cv2.destroyAllWindows()

except:
    print("Closing socket")
    client.close()
    s.close()
    


# In[ ]:




