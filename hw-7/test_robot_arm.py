from RobotArm import *
from PRM import PRM

from shapely.geometry import Polygon
import random


def test1():
    robot_arm = RobotArm([1, 2])
    obstacles = [Polygon([(1,1), (1,3), (3,3), (3,1)]),
                 Polygon([(0,-1), (-1,-3), (-3,-3), (-3,-1)])]
    workspace = Workspace(robot_arm, obstacles=obstacles)
    road_map = PRM(10000, 5, workspace)
    solution = road_map.query((pi, 0), (.1,.1))
    print(solution)
    if len(solution.path) > 0:
        workspace.get_animation(solution.path)

def test2():
    robot_arm = RobotArm([1, 1, 1])
    obstacles = [Polygon([(1,1), (1,3), (3,3), (3,1)]),
                 Polygon([(0,-1), (-1,-3), (-3,-3), (-3,-1)])]
    workspace = Workspace(robot_arm, obstacles=obstacles)
    road_map = PRM(10000, 5, workspace)
    solution = road_map.query((pi, 0, .1), (.1,.1, 6.2))
    print(solution)
    if len(solution.path) > 0:
        workspace.get_animation(solution.path)

def test3():
    robot_arm = RobotArm([1, 1, 1, 2])
    obstacles = [Polygon([(1,1), (1,3), (3,3), (3,1)]),
                 Polygon([(0,-1), (-1,-3), (-3,-3), (-3,-1)])]
    workspace = Workspace(robot_arm, obstacles=obstacles)
    road_map = PRM(10000, 5, workspace)
    solution = road_map.query((pi, 0, 6.2, 0), (.1,0,0, 0))
    print(solution)
    if len(solution.path) > 0:
        workspace.get_animation(solution.path)

def test4():
    print('This will take a minute')
    robot_arm = RobotArm([1, 1, 1])
    obstacles = [Polygon([(1,1), (1,3), (3,3), (3,1)]),
                 Polygon([(-2, 3), (-2, 1), (-1, 3), (-1, 1)]),
                Polygon([(-.5, -.5), (.5, -.5), (.5, -5), (-.5, -5)]),
                Polygon([(-.1, 1.5), (-.1, 1.6), (.1, 1.6), (.1, 1.5)]),
                Polygon([(1.85,-.025), (1.85, -.5), (2, -.5), (2, -.025)])]
    workspace = Workspace(robot_arm, obstacles=obstacles)
    road_map = PRM(10000, 5, workspace)
    solution = road_map.query((1.25*pi, 0, .1), (.1,.1, 6.2))
    print(solution)
    if len(solution.path) > 0:
        workspace.get_animation(solution.path)

'''
Report Graph versions of the animations above.
'''

def test11():
    robot_arm = RobotArm([1, 2])
    obstacles = [Polygon([(1,1), (1,3), (3,3), (3,1)]),
                 Polygon([(0,-1), (-1,-3), (-3,-3), (-3,-1)])]
    workspace = Workspace(robot_arm, obstacles=obstacles)
    road_map = PRM(10000, 5, workspace)
    solution = road_map.query((pi, 0), (.1,.1))
    print(solution)
    if len(solution.path) > 0:
        workspace.draw_animation(solution.path)

def test22():
    robot_arm = RobotArm([1, 1, 1])
    obstacles = [Polygon([(1,1), (1,3), (3,3), (3,1)]),
                 Polygon([(0,-1), (-1,-3), (-3,-3), (-3,-1)])]
    workspace = Workspace(robot_arm, obstacles=obstacles)
    road_map = PRM(10000, 5, workspace)
    solution = road_map.query((pi, 0, .1), (.1,.1, 6.2))
    print(solution)
    if len(solution.path) > 0:
        workspace.draw_animation(solution.path)

def test33():
    robot_arm = RobotArm([1, 1, 1, 2])
    obstacles = [Polygon([(1,1), (1,3), (3,3), (3,1)]),
                 Polygon([(0,-1), (-1,-3), (-3,-3), (-3,-1)])]
    workspace = Workspace(robot_arm, obstacles=obstacles)
    road_map = PRM(10000, 5, workspace)
    solution = road_map.query((pi, 0, 6.2, 0), (.1,0,0, 0))
    print(solution)
    if len(solution.path) > 0:
        workspace.draw_animation(solution.path)

def test44():
    print('This will take a minute')
    robot_arm = RobotArm([1, 1, 1])
    obstacles = [Polygon([(1,1), (1,3), (3,3), (3,1)]),
                 Polygon([(-2, 3), (-2, 1), (-1, 3), (-1, 1)]),
                Polygon([(-.5, -.5), (.5, -.5), (.5, -5), (-.5, -5)]),
                Polygon([(-.1, 1.5), (-.1, 1.6), (.1, 1.6), (.1, 1.5)]),
                Polygon([(1.85,-.025), (1.85, -.5), (2, -.5), (2, -.025)])]
    workspace = Workspace(robot_arm, obstacles=obstacles)
    road_map = PRM(10000, 5, workspace)
    solution = road_map.query((1.25*pi, 0, .1), (.1,.1, 6.2))
    print(solution)
    if len(solution.path) > 0:
        workspace.draw_animation(solution.path)

if __name__ == '__main__':
    random.seed(1)

    #-- Animation Tests
    test1()
    test2()
    test3()
    test4()

    #-- Static Graph Tests (as seen in report).
    #test11()
    #test22()
    #test33()
    #test44()
