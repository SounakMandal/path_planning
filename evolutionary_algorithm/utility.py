from math import *

import numpy as np



def distance(point1, point2):
    """
    Compute distance between two points
    """

    x1, y1 = point1
    x2, y2 = point2
    return sqrt((x2-x1) ** 2 + (y2-y1) ** 2)


def path_length(path):
    """
    Given a list of point that defines a path computes path_length
    """
    
    d = 0
    for i in range(len(path)-1):
        d += distance(path[i], path[i+1])
    return d


def slope(point1, point2):
    """
    Calculate slope of line joining two points
    """
    
    x1, y1 = point1
    x2, y2 = point2
    return inf if x1 == x2 else (y2-y1)/(x2-x1)


def position(line, point1, point2):
    """
    Given two points and a line find whether the points lie on the same or opposite side
    """
    
    m, (x, y) = line
    (x1, y1), (x2, y2) = point1, point2
    if m == inf:
        return 'same' if (x-x1)*(x-x2) > 0 else 'opposite'
    else:
        c = y-m*x
        return 'same' if (y1-m*x1-c)*(y2-m*x2-c) > 0 else 'opposite'


def compute_centre(m, start, r):
    """
    Given start point, slope and radius computes the two possible centres
    """
    
    if m == 0:
        c1 = (start[0]-r, start[1])
        c2 = (start[0]+r, start[1])
    elif m == inf:
        c1 = (start[0], start[1]-r)
        c2 = (start[0], start[1]+r)
    else:
        alpha = atan(-1/m)
        if alpha < 0:
            alpha = pi + alpha
        c1 = (start[0]+r*cos(alpha), start[1]+r*sin(alpha))
        c2 = (start[0]-r*cos(alpha), start[1]-r*sin(alpha))
    return c1, c2


def angle(point, centre):
    """
    Computes the angle made by the position vector joining point and centre
    """
    
    x, y = point[0] - centre[0], point[1] - centre[1]
    if x == 0:
        return pi if y >= 0 else 1.5*pi
    alpha = atan(abs(y/x))
    if x > 0:
        return alpha if y >= 0 else 2*pi - alpha
    else:
        return pi - alpha if y >= 0 else pi + alpha


def traverse(start, end, radius, centre, point):
    """
    Computes the list of traversed points in a spline
    """
    
    if radius != inf:
        x, y = centre
        line = [slope(start, centre), start]
        pos = position(line, point, end)
        theta = angle(start, centre)
        theta1 = angle(end, centre)
        theta2 = theta1-2*pi if theta1 > theta else theta1+2*pi
        if pos == 'opposite':
            alpha = theta1 if abs(theta-theta1) < pi else theta2
        else:
            alpha = theta1 if abs(theta-theta1) > pi else theta2
        if abs(radius*abs(theta1-theta) - radius*abs(theta2-theta)) > 20:
            alpha = theta1 if abs(theta1-theta) < abs(theta2-theta) else theta2
        step = (alpha-theta)/10
        traversal_path = [
            (x + radius*cos(theta), y + radius*sin(theta))
            for theta in np.arange(theta, alpha, step)
        ]
    else:
        x1, y1 = start
        x2, y2 = end
        x, y = x2-x1, y2-y1
        xstep, ystep = x/10, y/10
        traversal_path = [
            (x1+alpha, y1+beta) 
            for alpha, beta in zip(np.arange(0, x, xstep), np.arange(0, y, ystep))
        ]
    if end not in traversal_path:
        traversal_path.append(end)
    x_set, y_set = [], []
    for x, y in traversal_path:
        x_set.append(x)
        y_set.append(y)
    return traversal_path, x_set, y_set
