import random

import scipy.integrate as integrate

from utility import *


def spline_obstacle_cost(spline, obstacle):
    """
    Compute the cost of a single spline for a single obstacle
    
    Parameters
    ---------
    spline : The current spline on which body moves
    obstacle : The obstacle due to which cost is computed
    
    Returns
    -------
    The cost encountered on spline due to obstacle

    """

    x, y = obstacle['position']
    delta_x = obstacle['delta_x']
    clearance_radius = obstacle['clearance_radius']

    def c(r, theta):
        centre = x + r*cos(theta), y + r*sin(theta)
        spline_points, cost = spline.road, 0
        for i in range(len(spline_points)-1):
            alpha = distance(spline_points[i], centre)
            s = distance(spline_points[i], spline_points[i+1])
            cost += 0 if alpha > clearance_radius else 10*s/(alpha**2)
        return cost

    def gamma(r):
        point_cost, dtheta = 0, 0.1
        for theta in np.arange(0, 2*pi, dtheta):
            point_cost += c(r, theta)*dtheta
        return point_cost/(2*pi)

    def f(r):
        numerator = 2*np.exp(-np.square(r/delta_x))
        denominator = sqrt(pi)*delta_x*erf(1)
        return numerator*gamma(r)/denominator
    
    """Using scipy module integration return integrate.quad(f, 0, delta_x)[0]"""
    if delta_x == 0:
        return c(0, 0)
    total_cost, dr = 0, 1
    for r in np.arange(0, delta_x, dr):
        total_cost += f(r)*dr
    return total_cost


def spline_cost(spline, obstacle_list):
    """
    Computes the cost of a single spline due to all obstacles
    """
    
    cost = 0
    for obstacle in obstacle_list:
        cost += spline_obstacle_cost(spline, obstacle)
    return cost


def obstacle_cost(path, obstacle_list):
    """
    Computes the cost of entire path due to all obstacles
    """
    
    cost = 0
    for spline in path:
        cost += spline_cost(spline, obstacle_list)
    return cost


def fuel_cost(path):
    """
    Computes total path_length which is a measure of fuel cost
    """
    
    length = 0
    for spline in path:
        length += spline.path_length
    return length


def cost(path, obstacle_list):
    """
    Returns the total cost of the path
    """

    cost1 = fuel_cost(path)
    cost2 = obstacle_cost(path, obstacle_list)
    print(f"Obstacle cost : {cost1}, Fuel cost : {cost2}")
    return cost1 + cost2
