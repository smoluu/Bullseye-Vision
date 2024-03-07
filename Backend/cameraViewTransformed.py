import jpgReceive
import transform
import cv2
import numpy as np

DEGUB = True
npz = np.load("Backend/calibration_data.npz",)

while True:

    srcL = jpgReceive.getJpg("left")

    srcR = jpgReceive.getJpg("right")

    srcL = transform.warpedImage(srcL,"left")
    srcR = transform.warpedImage(srcR,"right")



    if DEGUB == True:
        height, width = srcR.shape[:2]
        print(npz["centerPoints"])
        centerL = npz["centerPoints"][0][0]
        centerR = npz["centerPoints"][1][0]

        cv2.circle(srcL,(centerL),7,(255,255,255), 2)
        cv2.circle(srcR,(centerR),7,(255,255,255), 2)

    cv2.imshow("Transformed Image L", srcL)
    cv2.imshow("Transformed Image R", srcR)

    # wait for the key and come out of the loop 
    if cv2.waitKey(1) == ord('q'):
        break
