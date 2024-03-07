import jpgReceive
import transform
import cv2


while True:

    srcL = jpgReceive.getJpg("left")
    srcL = cv2.flip(srcL,0)
    srcL = cv2.flip(srcL,1)

    srcR = jpgReceive.getJpg("right")
    srcR = cv2.flip(srcR,0)
    srcR = cv2.flip(srcR,1)

    srcL = transform.warpedImage(srcL,"left")
    srcR = transform.warpedImage(srcR,"right")


    cv2.imshow("Transformed Image L", srcL)
    cv2.imshow("Transformed Image R", srcR)

    # wait for the key and come out of the loop 
    if cv2.waitKey(1) == ord('q'):
        break
