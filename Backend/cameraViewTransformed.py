import cameraReceive
from score import pointToAngle, pointToRadius, pointToScore
from dart import getNewDartContour, getTipPoint
import cv2
import numpy as np
npz = np.load("Backend/calibration_data.npz",)

DEGUB = True
warpImage = True

clickPoint = ()
red = (0,0,255)
blue = (255,0,0)
green = (0,255,0)

def click_event(event, x, y, flags, params):
    global clickPoint
    # checking for left mouse clicks
    if event == cv2.EVENT_LBUTTONDOWN:
        clickPoint = x, y
        return clickPoint
    
while True:

    srcL = cameraReceive.getJpg("left")
    srcR = cameraReceive.getJpg("right")



    if warpImage:
        srcL = cv2.warpPerspective(srcL, npz["matrixL"], (1600, 1200))
        srcR = cv2.warpPerspective(srcR, npz["matrixR"], (1600, 1200))


    if DEGUB == True:

        #get center points from calibration data
        centerL = list(npz["centerPoints"][0][0])
        centerR = list(npz["centerPoints"][1][0])

        # draw center
        cv2.circle(srcL,(centerL),7,(255,0,0), 2)
        cv2.circle(srcR,(centerR),7,(255,0,0), 2)

        

        if clickPoint:

            # draw click point
            cv2.circle(srcL,(clickPoint),7,(255,0,0), 2)
            cv2.circle(srcR,(clickPoint),7,(255,0,0), 2)
            
            # LEFT SIDE
            radius = pointToRadius(centerL, clickPoint)
            cv2.circle(srcL, (centerL), int(radius), (255,0,0), 2)
            cv2.putText(srcL, "R:" + str(int(radius)), (clickPoint[0],clickPoint[1]-10),0,1,red,1,cv2.LINE_AA)

            angleDeg = pointToAngle(centerL, clickPoint)
            cv2.putText(srcL, "D:" + str(angleDeg), (clickPoint[0],clickPoint[1]-35),0,1,red,1,cv2.LINE_AA)
            score = pointToScore(centerL,clickPoint)
            cv2.putText(srcL, "S:" + str(score), (clickPoint[0],clickPoint[1]-60),0,1,red,1,cv2.LINE_AA)

            # RIGHT SIDE
            radius = pointToRadius(centerR, clickPoint)
            cv2.circle(srcR, (centerR), int(radius), (255,0,0), 2)
            cv2.putText(srcR, "R:" + str(int(radius)), (clickPoint[0],clickPoint[1]-10),0,1,red,1,cv2.LINE_AA)
            angleDeg = pointToAngle(centerR, clickPoint)
            cv2.putText(srcR, "D:" + str(angleDeg), (clickPoint[0],clickPoint[1]-35),0,1,red,1,cv2.LINE_AA)
    
        # draw tip point
        dartContour, mask = getNewDartContour()
        tipX, tipY = getTipPoint(dartContour)
        tip = cv2.perspectiveTransform(np.array([[(tipX,tipY)]],np.float64), npz["matrixL"])[0]
        cv2.circle(srcL,(int(tip[0][0]),int(tip[0][1])),5,red,2)

        

    cv2.imshow("img_L", srcL)
    cv2.imshow("img_R", srcR)
    cv2.setMouseCallback('img_L', click_event)
    cv2.setMouseCallback('img_R', click_event)
    #cv2.imshow("Transformed Image R", srcR)

    # wait for the key and come out of the loop 
    if cv2.waitKey(1) == ord('q'):
        break
