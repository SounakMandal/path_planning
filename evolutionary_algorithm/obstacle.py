import random
import time


def generate_obstacle(
    length, width, velocity=(2, 1.5),
    clearance_radius=10, delta_x=5, delta_v=5
):
    """
    Generates obstacles with random position on the map

    Parameters
    ----------
    length : length of the map
    width : width of the map
    velocity : velocity of the obstacle
    clearance_radius : minimum distance from obstacle where object can pass
    delta_x : uncertainity in position
    delta_v : uncertainity in velocity

    Returns
    -------
    obstacle: A single obstacle with specified fields

    """

    obstacle = {
        "position": (random.random()*length, random.random()*width),
        "velocity": velocity,
        "clearance_radius": clearance_radius,
        "delta_x": delta_x,
        "delta_v": delta_v
    }
    return obstacle


def generate_list(n=50, length=100, width=100):
    """
    Returns a list of obstacles

    Parameters
    ----------
    n : number of obstacles
    length : length of map
    width : width of map

    Returns
    -------
    A list of obstacles

    """

    obstacle_list = [generate_obstacle(length, width) for i in range(n)]
    return obstacle_list


def update_list(obstacle_list, t):
    """
    Updates the uncertainity in position and velocity of obstacles

    Parameters
    ---------
    obstacle_list : A list of all obstacles on map
    t : starting time
    
    """
    
    for obstacle in obstacle_list:
        delta_t = time.time() - t
        x, y = obstacle['position']
        v_x, v_y = obstacle['velocity']
        obstacle['delta_x'] += obstacle['delta_v']*delta_t
        obstacle['position'] = (x + v_x*delta_t, y + v_y*delta_t)
