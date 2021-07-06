import copy

import matplotlib.patches as mpatches
import matplotlib.pyplot as plt

from cost import *
from obstacle import *
from path import *


def plot_obstacles(obstacle_list, axis):
    for obstacle in obstacle_list:
        x, y = obstacle['position']
        circle = mpatches.Circle((x, y), obstacle['delta_x'], fill=False)
        axis.add_artist(circle)
        axis.scatter(x, y, color='black', s=5)


def plot_path(path, axis, color='blue'):
    for spline in path:
        axis.plot(spline.x, spline.y, color)


def plot_all(axes, obstacle_list):
    color = {0: 'red', 1: 'blue', 2: 'orange', 3: 'green'}
    for col in range(2):
        plot_obstacles(obstacle_list, axes[0, col])
    path_count = len(population)
    for i in range(path_count):
        axis = axes[0, 0] if i < path_count // 2 else axes[0, 1]
        plot_path(population[i].path, axis, color[i % 4])


obstacle_list = generate_list()
start, end = (0, 0), (100, 100)
generation_count, generations = 1, 1
population = [Path(start, end, 5) for i in range(20)]

while generation_count <= generations:
    print(f"Starting generation {generation_count}")
    figure, axes = plt.subplots(1, 2, squeeze=False)
    figure.suptitle(f"Generation {generation_count}")
    plot_all(axes, obstacle_list)
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
    
    population = population[:-6]
    population.extend(copy1 + copy2)
    print("Population for next generation : ", len(population))
    generation_count += 1
    if generation_count > generations:
        generations += int(input('Enter the number of generations to continue training : '))
    print()
plt.show()
