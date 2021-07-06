import random

from utility import *


class Spline:
    """
    The class wrapper for a spline

    Methods
    -------
    __init__ : initializes the spline
    print : prints the spline

    Attributes
    ----------
    start_position : the starting position of the spline
    end_position : the ending position of the spline
    speed : the speed with which the object moves on the spline
    centre : the centre of the circle whose part is the spline
    radius : the radius of the circle whose part is the spline
    tangent : tangents to spline at start_position and end_position
    road : a collection of points that define the spline
    path_length : the length of the spline

    """

    def __init__(self, start, end, speed, tangent=None, point=None):
        self.start_position = start
        self.end_position = end
        self.speed = speed
        m2 = slope(start, end)
        d = distance(start, end)
        if tangent is None or tangent[0] == m2:
            self.centre = (inf, inf)
            self.radius = inf
            self.tangent = [m2, end]
        else:
            m1 = tangent[0]
            theta = pi/2 if m1*m2 == -1 else atan((m2-m1)/(1+m1*m2))
            if theta < 0:
                theta = pi + theta
            r = d/(2*sin(theta))
            c1, c2 = compute_centre(m1, start, r)
            self.centre = c1 if distance(c1, end) < distance(c2, end) else c2
            self.radius = r
            self.tangent = [-1/slope(self.centre, end), end]
        self.road, self.x, self.y = traverse(
            start, end, self.radius, self.centre, point
        )
        self.path_length = path_length(self.road)

    def print(self):
        print("Start position : ", self.start_position)
        print("End position : ", self.end_position)
        print("Centre : ", self.centre)
        print("Radius : ", self.radius)
        print("Path length : ", self.path_length)
        print("Speed : ", self.speed)
        print("Tangent : ", self.tangent)
        print("Traversal Path : ")
        for point in self.road:
            print(point)


class Path:
    """
    The class wrapper for a particular path

    Methods
    -------
    __init__ : initializes the spline
    print : prints the entire path
    mutate : mutate a section of the path
    crossover : crosses two path to produce a new path

    Attributes
    ----------
    start : the start position of the path
    end : the end position of the path
    path : the collection of splines that define the path

    """

    def __init__(self, start, goal, speed):
        self.start = start
        self.end = goal
        size = random.random()*5 + 1
        part = int(distance(start, goal)/size)
        n = random.randint(part+5, part+10)
        stepx = (goal[0] - start[0])/n
        stepy = (goal[1] - start[1])/n
        points = [(start[0] + i*stepx, start[1] + i*stepy) for i in range(n)]
        stepx = stepx + 1 if stepx > 0 else stepx - 1
        stepy = stepy + 1 if stepy > 0 else stepy - 1
        path = None
        for point in points:
            xvar, yvar = size*stepx*random.random(), size*stepy*random.random()
            x1, y1 = point
            x2, y2 = x1+xvar, y1+yvar
            x, y = random.random()*(x2-x1) + x1, random.random()*(y2-y1) + y1
            if path is None:
                spline = Spline(start, (x, y), speed)
                path = [spline]
            else:
                spline = Spline(
                    path[-1].end_position, (x, y),
                    speed, path[-1].tangent, path[-1].road[-5]
                )
                path.append(spline)
        spline = Spline(
            path[-1].end_position, goal, speed,
            path[-1].tangent, path[-1].road[-5]
        )
        path.append(spline)
        self.path = path

    def print(self):
        print("Splines in the path")
        for i, spline in enumerate(self.path):
            print(i+1, '. ', end='')
            spline.print()
    
    def mutate(self, start):
        segments = random.randint(1, 10)
        for i, spline in enumerate(self.path):
            if spline.start_position == start:
                start_index = i
                break
        end_index = start_index + segments
        if end_index >= len(self.path):
            end = self.end
        else:
            end = self.path[end_index].end_position
        partial_path = Path(start, end, self.path[0].speed)
        self.path[start_index: end_index] = partial_path.path

    def crossover(self, other):
        l1, l2 = len(self.path), len(other.path)
        i = random.randint(l1//3, 2*l1//3)
        j = random.randint(l2//3, 2*l2//3)
        point1, point2 = self.path[i].end_position, other.path[j].end_position
        partial1 = Path(point1, point2, self.path[0].speed)
        partial2 = Path(point2, point1, other.path[0].speed)
        seg11, seg12 = self.path[:i+1], self.path[i+1:]
        seg21, seg22 = other.path[:j+1], other.path[j+1:]
        self.path[:] = seg11 + partial1.path + seg22
        other.path[:] = seg21 + partial2.path + seg12
        return self, other
