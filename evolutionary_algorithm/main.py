import copy

import matplotlib.patches as mpatches
import matplotlib.pyplot as plt

from cost import *
from obstacle import *
from path import *


def plot_obstacles(obstacle_list, axis):
    for obstacle in obstacle_list:
        x, y = obstacle['position']
        circle = mpatches.Circle(
            (x, y), obstacle['delta_x'], fill=False,
            linestyle="dotted"
        )
        axis.add_artist(circle)
        axis.scatter(x, y, color='black', s=5)


def plot_path(path, axis):
    for spline in path:
        axis.plot(spline.x, spline.y)


def plot_all(obstacle_list):
    for i in range(2):
        plot_obstacles(obstacle_list, axes1[0, i])
        plot_obstacles(obstacle_list, axes2[0, i])
    
    path_count = len(population)
    for i in range(path_count):
        if i < path_count//4:
            axis = axes1[0, 0]
        elif path_count//4 <= i < path_count//2:
            axis = axes1[0, 1] 
        elif path_count//2 <= i < (3*path_count) //4:
            axis = axes2[0, 0]
        else:
            axis = axes2[0, 1]
        plot_path(population[i].path, axis)


obstacle_list = generate_list()
start, end = (0, 0), (100, 100)
generation_count, generations = 1, 1
population = [Path(start, end, 5) for i in range(20)]

while generation_count <= generations:
    print(f"Starting generation {generation_count}")
    figure, axes1 = plt.subplots(1, 2, squeeze=False)
    figure.suptitle(f"Generation {generation_count}")
    figure, axes2 = plt.subplots(1, 2, squeeze=False)
    figure.suptitle(f"Generation {generation_count}")
    plot_all(obstacle_list)
    
    costs = []
    for path in population:
        cost = path_cost(path, obstacle_list)
        costs.append(cost)
    population.sort(key=lambda x: x.cost)

    print()
    print(f"Generation {generation_count} over")
    print("Generation statistics")
    print(f"Minimum path cost : {min(costs)}")
    print(f"Maximum path cost : {max(costs)}")
    print(f"Mean path cost : {sum(costs)/len(costs)}")
    
    temp = [copy.deepcopy(path) for path in population[:4]]
    copy1 = []
    for path in temp:
        splines = path.path
        max_cost, mutation_index = 0, 0
        for i, spline in enumerate(splines):
            if spline.cost > max_cost:
                max_cost = spline.cost
                mutation_index = i
        path.mutate(splines[mutation_index].start_position)
        copy1.append(path)
    print("Mutated paths : ", len(copy1))
    
    temp = [copy.deepcopy(path) for path in population[:4]]
    copy2 = []
    for i in range(len(temp)-1):
        path1, path2 = temp[i].crossover(temp[i+1])
        copy2.extend([path1, path2])
    print("Crossed over paths : ", len(copy2))
    
    population = population[:-8]
    population.extend(copy1 + copy2)
    print("Population for next generation : ", len(population))
    generation_count += 1
    if generation_count > generations:
        generations += int(input('Enter the number of generations to continue training : '))
    print()
plt.show()
