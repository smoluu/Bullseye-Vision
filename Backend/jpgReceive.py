import urllib.request
import urllib
import cv2
import numpy as np
import time
import configparser

config = configparser.ConfigParser()
config.read("backend/config.ini")
URL_LEFT = config["CAMERA"]["URL_LEFT"]
URL_RIGHT = config["CAMERA"]["URL_RIGHT"]

fps = 0
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
def getJpg(side):
    if side == "left":
        imgResp = urllib.request.urlopen(URL_LEFT + "/cam-hi.jpg")
    if side == "right":
        imgResp = urllib.request.urlopen(URL_RIGHT + "/cam-hi.jpg")
    imgNp = np.array(bytearray(imgResp.read()),dtype=np.uint8)
    FpsCounter()
    return cv2.imdecode(imgNp,-1)


# pull .mjpeg from esp32-cam
def getMjepg(side):
    if side == "left":
        stream = urllib.request.urlopen(URL_LEFT + "/cam.mjpeg")
    if side == "right":
        stream = urllib.request.urlopen(URL_RIGHT + "/cam.mjpeg")
    bytes = b''
    while True:
        bytes += stream.read(256)
        a = bytes.find(b'\xff\xd8')
        b = bytes.find(b'\xff\xd9')
        if a != -1 and b != -1:
            jpg = bytes[a:b+2]
            bytes = bytes[b+2:]
            FpsCounter()
            return cv2.imdecode(np.frombuffer(jpg, dtype=np.uint8),-1)
