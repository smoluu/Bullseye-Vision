import cv2
import numpy as np
import cameraReceive

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
        if params == "points":
            points.append((x,y))
            print(points)
            clicks = clicks + 1
            if(clicks == 4):
                print("Press q to continue")
                return points
        if params == "center":
            points.append((x,y))
            print(points)
            return points


def selectPoints(image, mode):

    # displaying the image
    cv2.imshow('image', image)

    # setting mouse handler for the image
    # and calling the click_event() function
    cv2.setMouseCallback('image', click_event, mode)

    # wait for a key to be pressed to exit
    cv2.waitKey(0)
    # close the window
    cv2.destroyAllWindows()


def startCalibration():
    srcL = cameraReceive.getJpg("left")

    srcR = cameraReceive.getJpg("right")

    board = cv2.imread('Backend/calibration_image.png',1)

    #calibration image
    selectPoints(board,"points")
    board_points = points
    reset_values()

    # Left camera
    selectPoints(srcL, "points")
    cam_pointsL = points
    reset_values()

    # Right camera
    selectPoints(srcR, "points")
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

    #center points
    selectPoints(warpL, "center")
    centerL = points
    reset_values()

    selectPoints(warpR, "center")
    centerR = points
    reset_values()

    centerPoints = np.array([centerL,centerR])

    np.savez("Backend/calibration_data.npz", matrixL=cam_to_boardL, matrixR=cam_to_boardR, centerPoints=centerPoints, allow_pickle=True, fix_imports=True)

    cv2.waitKey(0)



    


