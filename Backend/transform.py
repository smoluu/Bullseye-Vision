import cv2
import numpy as np

def warpedImage(src, side: str):
    if side == "left":
        matrix = np.load("Backend/transformation_matrix_L.npy",)
    elif side == "right":
        matrix = np.load("Backend/transformation_matrix_R.npy",)
    
    return cv2.warpPerspective(src, matrix, (1600, 1200))

def pointToScore(point):

    score = 0
    return score