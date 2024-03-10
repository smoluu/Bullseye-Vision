import math

def pointToAngle(center, point):
    cx = center[0]
    cy = center[1]
    px = point[0]
    py = point[1]

    # Calculate the differences in x and y coordinates relative to the center
    deltaX = px - cx
    deltaY = py - cy

    # Calculate the angle using arctan2, and adjust it to have 360 degrees at the top
    angleRad = math.atan2(deltaX, deltaY)
    angleDeg = math.degrees(angleRad)
    angleDeg = (180-angleDeg) % 360

    return angleDeg

def pointToRadius(center, point):
    cx = center[0]
    cy = center[1]
    
    px = point[0]
    py = point[1]

    # Calculate radius
    radius = ((px - cx) ** 2 + (py - cy) ** 2) ** 0.5
    return radius


def pointToScore(center, point):
    score = 0

    return score
