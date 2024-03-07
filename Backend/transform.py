import cv2
import numpy as np

def getTransdormedPoint(point,side):
    if side == "left":
        matrix = np.load("Backend/transformation_matrix_L",)
    if side == "right":
        matrix = np.load("Backend/transformation_matrix_R",)
    
    #src_transformed = cv2.transform(src, matrix, None)
