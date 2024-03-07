import jpgReceive
import cv2
import numpy as np

matrixL = np.load("Backend/transformation_matrix_L.npy",)
matrixR = np.load("Backend/transformation_matrix_R.npy",)


while True:

    srcL = jpgReceive.getJpg("left")
    srcL = cv2.flip(srcL,0)
    srcL = cv2.flip(srcL,1)

    srcR = jpgReceive.getJpg("right")
    srcR = cv2.flip(srcR,0)
    srcR = cv2.flip(srcR,1)


    warpedL = cv2.warpPerspective(srcL, matrixL, (1600, 1200))
    warpedR = cv2.warpPerspective(srcR, matrixR, (1600, 1200))

    cv2.imshow("Transformed Image L", warpedL)
    cv2.imshow("Transformed Image R", warpedR)

    # wait for the key and come out of the loop 
    if cv2.waitKey(1) == ord('q'):
        break
