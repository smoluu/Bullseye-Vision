import cameraReceive
import transform
import cv2
import numpy as np

DEGUB = True
npz = np.load("Backend/calibration_data.npz",)
clickPoint = []

def click_event(event, x, y, flags, params):
    global clickPoint
    # checking for left mouse clicks
    if event == cv2.EVENT_LBUTTONDOWN:
        clickPoint = x,y
        print(clickPoint)
        return clickPoint
    
while True:

    srcL = cameraReceive.getMjepg("left")

    srcR = cameraReceive.getMjepg("right")

    srcL = transform.warpedImage(srcL,"left")
    srcR = transform.warpedImage(srcR,"right")



    if DEGUB == True:
        height, width = srcR.shape[:2]
        centerL = npz["centerPoints"][0][0]
        centerR = npz["centerPoints"][1][0]

        cv2.circle(srcL,(centerL),10,(0,0,255), 1)
        cv2.circle(srcR,(centerR),7,(255,0,0), 2)

        if clickPoint:
            cv2.circle(srcL,(clickPoint),7,(255,0,0), 2)
    cv2.imshow("img_L", srcL)
    cv2.setMouseCallback('img_L', click_event)
    #cv2.imshow("Transformed Image R", srcR)

    # wait for the key and come out of the loop 
    if cv2.waitKey(1) == ord('q'):
        break
