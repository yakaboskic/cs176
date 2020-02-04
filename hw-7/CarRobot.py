
from shapely.geometry import Point, Polygon
from math import pi
import matplotlib.pyplot as plt
import random
import numpy as np

from rrt import RRT
from GraphCarRobot import graph_results, animate_results #plot_tree, animate_results

#-- Carlike robot Workspace Class.
class Workspace:
    def __init__(self, dim=(15, 15), obstacles=None):
        self.obstacles = obstacles
        self.dim = dim


    #-- Checks for collision
    def is_collision(self, state):
        #-- Casts as a shapely point
        state_point = Point(state[0], state[1])
        if self.obstacles is None:
            return False
        else:
            #-- For each obstacle checks if the point is contained in the obstacle.
            for obstacle in self.obstacles:
                if obstacle.contains(state_point):
                    return True
            return False

    def graph_results(self, results, car_rrt, plot_tree=False):
        return graph_results(self, results, car_rrt, plot_tree)

    def animate_results(self, results, car_rrt, plot_tree=False):
        return animate_results(self, results, car_rrt, plot_tree)


if __name__ == '__main__':
    random.seed(446)
    obstacles = [Polygon([(2,0), (2, 2), (3, 2), (3, 0)]),
                Polygon([(4,4), (4,8), (7,1)]),
                Polygon([(2,2), (1,8), (2,4), (3,3)])]
    workspace = Workspace(dim=(12,12), obstacles=obstacles)
    car_rrt = RRT(workspace, (1, 1, pi), (10, 10, pi), 10000, num_rand_actions=6, max_control_time=2, step_threshold=.05)
    results = car_rrt.build_rrt()
    print(results)
    ax = workspace.graph_results(results, car_rrt, plot_tree=False)
    plt.show()
