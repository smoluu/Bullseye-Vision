import cv2
import numpy as np

def warpedImage(src, side: str):
    
    npz = np.load("Backend/calibration_data.npz",)
    if side == "left":
        return cv2.warpPerspective(src, npz["matrixL"], (1600, 1200))
    elif side == "right":
        return cv2.warpPerspective(src, npz["matrixR"], (1600, 1200))
    

def pointToScore(point):

    score = 0
    return score


matrix = np.load("Backend/transformation_matrix_R.npy",)
print(matrix)