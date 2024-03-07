import cv2
import numpy as np
import jpgReceive

clicks = 0
points = []

def reset_values():
    global clicks
    global points
    clicks = 0
    points = []

def click_event(event, x, y, flags, params):
    global clicks
    global points
    # checking for left mouse clicks
    if event == cv2.EVENT_LBUTTONDOWN:
 
        # displaying the coordinates
        points.append((x,y))
        print(points)
        clicks = clicks + 1
        if(clicks == 4):
            print("Press q to continue")
            return points


def select_points(image):

    # displaying the image
    cv2.imshow('image', image)

    # setting mouse handler for the image
    # and calling the click_event() function
    cv2.setMouseCallback('image', click_event)

    # wait for a key to be pressed to exit
    cv2.waitKey(0)
    # close the window
    cv2.destroyAllWindows()


def startCalibration():
    srcL = jpgReceive.getJpg("left")
    srcL = cv2.flip(srcL,0)
    srcL = cv2.flip(srcL,1)

    srcR = jpgReceive.getJpg("right")
    srcR = cv2.flip(srcR,0)
    srcR = cv2.flip(srcR,1)

    board = cv2.imread('Backend/dartboard_points.png',1)

    #calibration image
    select_points(board)
    board_points = points
    reset_values()
    print("fine")

    # Left camera
    select_points(srcL)
    print("fine")
    cam_pointsL = points
    reset_values()

    # Right camera
    select_points(srcR)
    cam_pointsR = points
    reset_values()

    board_points = np.array([board_points[0], board_points[1], board_points[2], board_points[3]], dtype=np.float32)
    cam_pointsL = np.array([cam_pointsL[0], cam_pointsL[1], cam_pointsL[2],cam_pointsL[3]], dtype=np.float32)
    cam_pointsR = np.array([cam_pointsR[0], cam_pointsR[1], cam_pointsR[2],cam_pointsR[3]], dtype=np.float32)

    cam_to_boardL = cv2.getPerspectiveTransform(cam_pointsL, board_points)
    cam_to_boardR = cv2.getPerspectiveTransform(cam_pointsR, board_points)
    print(cam_to_boardL)
    print(cam_to_boardR)

    warpL = cv2.warpPerspective(srcL, cam_to_boardL, (1600, 1200))
    warpR = cv2.warpPerspective(srcR, cam_to_boardR, (1600, 1200))
    np.save("Backend/transformation_matrix_L", cam_to_boardL, allow_pickle=True, fix_imports=True)
    np.save("Backend/transformation_matrix_R", cam_to_boardR, allow_pickle=True, fix_imports=True)
    cv2.imshow("WarpL", warpL)
    cv2.imshow("WarpR", warpR)

    cv2.waitKey(0)



    


