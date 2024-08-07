import cv2
import numpy as np
import cameraReceive
import math
from score import pointToScore
from tts import text_to_speech
import time #for testing
npz = np.load(
    "Backend/calibration_data.npz",
)


def getNewDartContour():
    img = cv2.imread("Backend/boardL.jpg")
    img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    img = cv2.GaussianBlur(img,(25,25),0)
    
    ret, thresh1 = cv2.threshold(img, 150, 255, cv2.THRESH_BINARY)
    img2 = cameraReceive.getJpg("left")

    img2Gray = cv2.cvtColor(img2,cv2.COLOR_BGR2GRAY)
    img2Blur = cv2.GaussianBlur(img2Gray,(25,25),0)
    
    #ret, thresh2 = cv2.threshold(img2, 150, 255, cv2.THRESH_BINARY)
    
    diff = cv2.absdiff(img,img2Blur)
    ret, mask = cv2.threshold(diff,20,255,cv2.THRESH_BINARY)
    mask = cv2.GaussianBlur(mask,(35,35),0)
    ret, mask = cv2.threshold(mask,25,255,cv2.THRESH_BINARY)

    
    contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    return  contours, mask


def getTipPoint(contours):
    if len(contours) > 0:

        triangle = cv2.minEnclosingTriangle(contours[0])
        triangle = triangle[1].astype(int)
        tPoints = []
        tPoints.append(tuple(triangle[0][0]))
        tPoints.append(tuple(triangle[1][0]))
        tPoints.append(tuple(triangle[2][0]))
        tPoints.sort()

        # calculate index of closest contour point to tpoints[0]
        minDist = 1000
        closestContourIndex = 0

        for  index,point in enumerate(contours[0]):
            dist = math.dist(tPoints[0],(point[0]))
            if minDist > dist:
                minDist = dist
                closestContourIndex = index

        tipX = contours[0][closestContourIndex][0][0]
        tipY = contours[0][closestContourIndex][0][1]

        warpedTip = cv2.perspectiveTransform(np.array([[(tipX,tipY)]],np.float64), npz["matrixL"])[0]
        print(warpedTip)

        # cv2.circle(img,(tipX,tipY),7,(0,0,255),-1)

        return  tipX,tipY, warpedTip

    return None, None, None


if __name__ == "__main__":
    centerL = list(npz["centerPoints"][0][0])
    oldScore = 0
    while True:
        contour, mask = getNewDartContour()
        x, y, warpedTip = getTipPoint(contour)
        img = cameraReceive.getJpg("left")
        if x and y:
            triangle = cv2.minEnclosingTriangle(contour[0])
            triangle = triangle[1].astype(int)
            tPoints = []
            tPoints.append(tuple(triangle[0][0]))
            tPoints.append(tuple(triangle[1][0]))
            tPoints.append(tuple(triangle[2][0]))
            tPoints.sort()
            # draw triangle
            cv2.line(img,tPoints[0],tPoints[1], (255,0,0), 2, 0)
            cv2.line(img,tPoints[1],tPoints[2], (0,255,0), 2, 0)
            cv2.line(img,tPoints[2],tPoints[0], (0,0,255), 2, 0)
            cv2.drawContours(img, contour, -1, (0, 255, 0), 2)
            # draw tip point
            cv2.circle(img,(x,y),3,(0,0,255),2)
            # display score
            score = pointToScore(centerL,warpedTip)
            cv2.putText(img, "Score:" + str(int(score)), (100,100),0,1,(255,0,0),1,cv2.LINE_AA)
            # tts
            if score != oldScore and score != 0:
                text_to_speech(str(score))
                oldScore = score

            # centroid of contour
            # M = cv2.moments(cont[0])
            # cX = int(M["m10"] // M["m00"])
            # cY = int(M["m01"] // M["m00"])
            # cv2.circle(img,(cX,cY),3,(0,0,255),2)

            time.sleep(0.2)
            

        cv2.imshow("img_L", img)
        cv2.imshow("temp", mask)
        if cv2.waitKey(1) == ord('q'):
            break
