import jpgReceive
import transform
import cv2

DEGUB = True

while True:

    srcL = jpgReceive.getJpg("left")

    srcR = jpgReceive.getJpg("right")

    srcL = transform.warpedImage(srcL,"left")
    srcR = transform.warpedImage(srcR,"right")



    if DEGUB == True:
        height, width = srcR.shape[:2]
        center = (width//2, height//2)

        cv2.circle(srcR,(center),7,(255,255,255), 2)

    cv2.imshow("Transformed Image L", srcL)
    cv2.imshow("Transformed Image R", srcR)

    # wait for the key and come out of the loop 
    if cv2.waitKey(1) == ord('q'):
        break
