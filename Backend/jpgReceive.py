import urllib.request
import urllib
import cv2
import numpy as np
import time

url = "http://192.168.0.101/cam-hi.jpg"
fps = 1
start_time = time.time()
frame_count = 0
frames_array = []

def FpsCounter():
  global frame_count
  global start_time
  frame_count += 1
  elapsed_time = time.time() - start_time
  if elapsed_time >= 1.0:
      fps = frame_count / elapsed_time
      frames_array.append(fps)
      print(f"FPS: {fps:.2f} " + f" AVG: {sum(frames_array) / len(frames_array):.2f}")
      frame_count = 0
      start_time = time.time()    

#pull .jpg from esp32-cam
      
while True:
    start = time.time()
    imgResp = urllib.request.urlopen(url)
    imgNp = np.array(bytearray(imgResp.read()),dtype=np.uint8)
    img = cv2.imdecode(imgNp,-1)
    cv2.imshow('test',img)
    FpsCounter()
    if cv2.waitKey(1) == 27: #escape key
      exit(0)  
    time.sleep(0.5)

# pull .mjpg from esp32-cam
# 10fps avg with 800x600
      
stream = urllib.request.urlopen(url)
bytes = b''
while True:
    bytes += stream.read(1024)
    a = bytes.find(b'\xff\xd8')
    b = bytes.find(b'\xff\xd9')
    if a != -1 and b != -1:
        jpg = bytes[a:b+2]
        bytes = bytes[b+2:]
        i = cv2.imdecode(np.frombuffer(jpg, dtype=np.uint8),-1)
        cv2.imshow('i', i)
        FpsCounter()
        if cv2.waitKey(1) == 27: #escape key
          exit(0)  
