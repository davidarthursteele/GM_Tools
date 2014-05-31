import math

def pythagorean(a,b):
    return math.sqrt(a**2 + b**2)

def rangefinder_2d():
    x = float(raw_input("Please input the distance (in meters) of the X coordinate. - "))
    y = float(raw_input("Please input the distance (in meters) of the Y coordinate. - "))
    return pythagorean(x,y)

def rangefinder_3d():
    xy = rangefinder_2d()
    z = float(raw_input("Please input the change in elevation (in meters). - "))
    return pythagorean(xy,z)

print rangefinder_3d()