
from shapely.geometry import Point, Polygon
from math import pi

import matplotlib.pyplot as plt
import random

from rrt import RRT
from CarRobot import Workspace


def test1():
    obstacles = [Polygon([(2,0), (2, 2), (3, 2), (3, 0)]),
                Polygon([(4,4), (4,8), (7,1)]),
                Polygon([(2,2), (1,8), (2,4), (3,3)])]
    workspace = Workspace(dim=(12,12), obstacles=obstacles)
    car_rrt = RRT(workspace, (1, 1, pi), (10, 10, pi), 10000, num_rand_actions=6, max_control_time=1, step_threshold=.05)
    results = car_rrt.build_rrt()
    print(results)
    ax = workspace.graph_results(results, car_rrt, plot_tree=False)
    plt.show()

def test2():
    obstacles = [Polygon([(2,0), (8, 0), (8, 1), (2, 1)]),
                Polygon([(2,10), (8,10), (8,8), (2,8)]),
                Polygon([(2,1), (2,8), (3,8), (3,1)])]
    workspace = Workspace(dim=(12,12), obstacles=obstacles)
    car_rrt = RRT(workspace, (1, 6, pi), (6, 6, pi), 10000, num_rand_actions=6, max_control_time=1, step_threshold=.05)
    results = car_rrt.build_rrt()
    print(results)
    ax = workspace.graph_results(results, car_rrt, plot_tree=False)
    plt.show()

def test11():
    obstacles = [Polygon([(2,0), (2, 2), (3, 2), (3, 0)]),
                Polygon([(4,4), (4,8), (7,1)]),
                Polygon([(2,2), (1,8), (2,4), (3,3)])]
    workspace = Workspace(dim=(12,12), obstacles=obstacles)
    car_rrt = RRT(workspace, (1, 1, pi), (10, 10, pi), 10000, num_rand_actions=6, max_control_time=1, step_threshold=.05)
    results = car_rrt.build_rrt()
    print(results)
    anim = workspace.animate_results(results, car_rrt)
    plt.show()

def test22():
    obstacles = [Polygon([(2,0), (8, 0), (8, 1), (2, 1)]),
                Polygon([(2,10), (8,10), (8,8), (2,8)]),
                Polygon([(2,1), (2,8), (3,8), (3,1)])]
    workspace = Workspace(dim=(12,12), obstacles=obstacles)
    car_rrt = RRT(workspace, (1, 6, pi), (6, 6, pi), 10000, num_rand_actions=6, max_control_time=1, step_threshold=.05)
    results = car_rrt.build_rrt()
    print(results)
    anim = workspace.animate_results(results, car_rrt, plot_tree=True)
    plt.show()

''' Extension Tests'''

def test3():
    obstacles = [Polygon([(2,0), (2, 2), (3, 2), (3, 0)]),
                Polygon([(4,4), (4,8), (7,1)]),
                Polygon([(2,2), (1,8), (2,4), (3,3)])]
    workspace = Workspace(dim=(12,12), obstacles=obstacles)
    car_rrt = RRT(workspace, (1, 1, pi), (10, 10, pi), 10000, num_rand_actions=1, max_control_time=1, step_threshold=.05)
    results = car_rrt.build_rrt()
    print(results)
    ax = workspace.graph_results(results, car_rrt, plot_tree=False)
    plt.show()

def test4():
    obstacles = [Polygon([(2,0), (2, 2), (3, 2), (3, 0)]),
                Polygon([(4,4), (4,8), (7,1)]),
                Polygon([(2,2), (1,8), (2,4), (3,3)])]
    workspace = Workspace(dim=(12,12), obstacles=obstacles)
    car_rrt = RRT(workspace, (1, 1, pi), (10, 10, pi), 10000, num_rand_actions=2, max_control_time=1, step_threshold=.05)
    results = car_rrt.build_rrt()
    print(results)
    ax = workspace.graph_results(results, car_rrt, plot_tree=False)
    plt.show()

def test5():
    obstacles = [Polygon([(2,0), (2, 2), (3, 2), (3, 0)]),
                Polygon([(4,4), (4,8), (7,1)]),
                Polygon([(2,2), (1,8), (2,4), (3,3)])]
    workspace = Workspace(dim=(12,12), obstacles=obstacles)
    car_rrt = RRT(workspace, (1, 1, pi), (10, 10, pi), 10000, num_rand_actions=3, max_control_time=1, step_threshold=.05)
    results = car_rrt.build_rrt()
    print(results)
    ax = workspace.graph_results(results, car_rrt, plot_tree=False)
    plt.show()

def test6():
    obstacles = [Polygon([(2,0), (2, 2), (3, 2), (3, 0)]),
                Polygon([(4,4), (4,8), (7,1)]),
                Polygon([(2,2), (1,8), (2,4), (3,3)])]
    workspace = Workspace(dim=(12,12), obstacles=obstacles)
    car_rrt = RRT(workspace, (1, 1, pi), (10, 10, pi), 10000, num_rand_actions=4, max_control_time=1, step_threshold=.05)
    results = car_rrt.build_rrt()
    print(results)
    ax = workspace.graph_results(results, car_rrt, plot_tree=False)
    plt.show()

def test7():
    obstacles = [Polygon([(2,0), (2, 2), (3, 2), (3, 0)]),
                Polygon([(4,4), (4,8), (7,1)]),
                Polygon([(2,2), (1,8), (2,4), (3,3)])]
    workspace = Workspace(dim=(12,12), obstacles=obstacles)
    car_rrt = RRT(workspace, (1, 1, pi), (10, 10, pi), 10000, num_rand_actions=5, max_control_time=1, step_threshold=.05)
    results = car_rrt.build_rrt()
    print(results)
    ax = workspace.graph_results(results, car_rrt, plot_tree=False)
    plt.show()


def test8():
    obstacles = [Polygon([(2,0), (2, 2), (3, 2), (3, 0)]),
                Polygon([(4,4), (4,8), (7,1)]),
                Polygon([(2,2), (1,8), (2,4), (3,3)])]
    workspace = Workspace(dim=(12,12), obstacles=obstacles)
    car_rrt = RRT(workspace, (1, 1, pi), (10, 10, pi), 10000, num_rand_actions=6, max_control_time=1, step_threshold=.05)
    results = car_rrt.build_rrt()
    print(results)
    ax = workspace.graph_results(results, car_rrt, plot_tree=False)
    plt.show()

def test33():
    obstacles = [Polygon([(2,0), (2, 2), (3, 2), (3, 0)]),
                Polygon([(4,4), (4,8), (7,1)]),
                Polygon([(2,2), (1,8), (2,4), (3,3)])]
    workspace = Workspace(dim=(12,12), obstacles=obstacles)
    car_rrt = RRT(workspace, (1, 1, pi), (10, 10, pi), 10000, num_rand_actions=6, max_control_time=2, step_threshold=.05)
    results = car_rrt.build_rrt()
    print(results)
    ax = workspace.graph_results(results, car_rrt, plot_tree=False)
    plt.show()

def test44():
    obstacles = [Polygon([(2,0), (2, 2), (3, 2), (3, 0)]),
                Polygon([(4,4), (4,8), (7,1)]),
                Polygon([(2,2), (1,8), (2,4), (3,3)])]
    workspace = Workspace(dim=(12,12), obstacles=obstacles)
    car_rrt = RRT(workspace, (1, 1, pi), (10, 10, pi), 10000, num_rand_actions=6, max_control_time=1, step_threshold=.05)
    results = car_rrt.build_rrt()
    print(results)
    ax = workspace.graph_results(results, car_rrt, plot_tree=False)
    plt.show()

def test55():
    obstacles = [Polygon([(2,0), (2, 2), (3, 2), (3, 0)]),
                Polygon([(4,4), (4,8), (7,1)]),
                Polygon([(2,2), (1,8), (2,4), (3,3)])]
    workspace = Workspace(dim=(12,12), obstacles=obstacles)
    car_rrt = RRT(workspace, (1, 1, pi), (10, 10, pi), 10000, num_rand_actions=6, max_control_time=.75, step_threshold=.05)
    results = car_rrt.build_rrt()
    print(results)
    ax = workspace.graph_results(results, car_rrt, plot_tree=False)
    plt.show()

def test66():
    obstacles = [Polygon([(2,0), (2, 2), (3, 2), (3, 0)]),
                Polygon([(4,4), (4,8), (7,1)]),
                Polygon([(2,2), (1,8), (2,4), (3,3)])]
    workspace = Workspace(dim=(12,12), obstacles=obstacles)
    car_rrt = RRT(workspace, (1, 1, pi), (10, 10, pi), 10000, num_rand_actions=6, max_control_time=.5, step_threshold=.05)
    results = car_rrt.build_rrt()
    print(results)
    ax = workspace.graph_results(results, car_rrt, plot_tree=False)
    plt.show()

def test77():
    obstacles = [Polygon([(2,0), (2, 2), (3, 2), (3, 0)]),
                Polygon([(4,4), (4,8), (7,1)]),
                Polygon([(2,2), (1,8), (2,4), (3,3)])]
    workspace = Workspace(dim=(12,12), obstacles=obstacles)
    car_rrt = RRT(workspace, (1, 1, pi), (10, 10, pi), 10000, num_rand_actions=6, max_control_time=.25, step_threshold=.05)
    results = car_rrt.build_rrt()
    print(results)
    ax = workspace.graph_results(results, car_rrt, plot_tree=False)
    plt.show()


def test88():
    obstacles = [Polygon([(2,0), (2, 2), (3, 2), (3, 0)]),
                Polygon([(4,4), (4,8), (7,1)]),
                Polygon([(2,2), (1,8), (2,4), (3,3)])]
    workspace = Workspace(dim=(12,12), obstacles=obstacles)
    car_rrt = RRT(workspace, (1, 1, pi), (10, 10, pi), 10000, num_rand_actions=6, max_control_time=.2, step_threshold=.05)
    results = car_rrt.build_rrt()
    print(results)
    ax = workspace.graph_results(results, car_rrt, plot_tree=False)
    plt.show()

if __name__ == '__main__':
    random.seed(445)

    '''
    Report graphs
    '''
    test1()
    test2()

    '''
    Animations of graphs
    '''
    #test11()
    #test22()


    '''Extension Results'''
    #test3()
    #test4()
    #test5()
    #test6()
    #test7()
    #test8()
    
    #test33()
    #test44()
    #test55()
    #test66()
    #test77()
    #test88()
