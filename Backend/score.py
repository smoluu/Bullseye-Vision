import math

#start, end, score
angleScoreRanges = (
    (0, 8, 20),
    (8.001, 27, 1),
    (27.001, 45, 18),
    (45.001, 63, 4),
    (63.001, 81, 13),
    (81.001, 99, 6),
    (99.001, 117, 10),
    (117.001, 135, 15),
    (135.001, 153, 2),
    (153.001, 171, 17),
    (171.001, 188.5, 3),
    (188.501, 206, 19),
    (206.001, 224.5, 7),
    (224.501, 242.5, 16),
    (242.501, 261, 8),
    (261.001, 279.5, 11),
    (279.501, 297.5, 14),
    (297.501, 315.5, 9),
    (315.501, 333.5, 12),
    (333.501, 351.5, 5),
    (351.501, 360, 20),
)

#start, end, multiplier
radiusMultiplierRanges = (
    (511,549,3), #triple
    (305, 340, 2), #double
)

#start, end, score
radiusBullRanges = (
    (20.01, 52, 25), #bull
    (0, 20, 50) #bullseye
)


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
    multiplier = 1
    angleDeg = pointToAngle(center, point)
    pointRadius = pointToRadius(center, point)
    bullRadius = radiusBullRanges[0][1]
    outRadius = radiusMultiplierRanges[0][1]

    # dart is between bullradius & outradius
    if pointRadius >= bullRadius and pointRadius <= outRadius:

        # Calculate multiplier
        for radius in radiusMultiplierRanges:
            if pointRadius >= radius[0] and pointRadius <= radius[1]:
                multiplier = radius[2]

        # Calculate score
        for angle in angleScoreRanges:
            if angleDeg >= angle[0] and angleDeg <= angle[1]:
                score = angle[2]
    # bull
    elif pointRadius <= bullRadius:

        for radius in radiusBullRanges:
             if pointRadius >= radius[0] and pointRadius <= radius[1]:
                score = radius[2]
    else:
        return 0
    
    return score * multiplier
