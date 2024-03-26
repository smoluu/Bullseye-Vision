import cv2
import numpy as np
import cameraReceive

def detectDart():
    img1 = cv2.imread("Backend/boardL.jpg")
    img1 = cv2.cvtColor(img1,cv2.COLOR_BGR2GRAY)
    img1 = cv2.GaussianBlur(img1,(35,35),0)
    
    ret, thresh1 = cv2.threshold(img1, 150, 255, cv2.THRESH_BINARY)
    img2 = cameraReceive.getJpg("left")

    img2Gray = cv2.cvtColor(img2,cv2.COLOR_BGR2GRAY)
    img2Blur = cv2.GaussianBlur(img2Gray,(35,35),0)
    
    #ret, thresh2 = cv2.threshold(img2, 150, 255, cv2.THRESH_BINARY)
    
    diff = cv2.absdiff(img1,img2Blur)
    #gray = cv2.cvtColor(diff,cv2.COLOR_BGR2GRAY)
    ret, mask = cv2.threshold(diff,20,255,cv2.THRESH_BINARY)
    mask = cv2.GaussianBlur(mask,(35,35),0)
    ret, mask = cv2.threshold(mask,25,255,cv2.THRESH_BINARY)

    
    contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(img2, contours,-1, (0,255,0), 2)
    print(f"Contour count: {len(contours)}")


    return  img2


def getTipPoint(img):
    output = img
    gray = cv2.cvtColor(output, cv2.COLOR_BGR2GRAY) 
    edged = cv2.Canny(gray, 30, 200) 
    ret,thresh = cv2.threshold(output, 40, 255, 0)
    contours, hierarchy = cv2.findContours(edged, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    if len(contours) != 0:

        # draw in blue the contours that were founded
        cv2.drawContours(output, contours, -1, 255, 3)

        # find the biggest countour (c) by the area
        c = max(contours, key = cv2.contourArea)
        x,y,w,h = cv2.boundingRect(c)

        # draw the biggest contour (c) in green
        cv2.rectangle(output,(x,y),(x+w,y+h),(0,255,0),2)

    return  output


while True:
    img = detectDart()
    cv2.imshow("Result", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
