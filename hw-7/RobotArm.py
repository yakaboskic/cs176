from math import cos, sin, pi
import matplotlib.pyplot as plt
from shapely.geometry import Polygon, LineString
import random

from GraphRobotArm import graph_workspace, animate_workspace, animate_workspace_2
from PRM import PRM

#-- Robot Arm Class
class RobotArm:
    def __init__(self, arm_lengths=[1,1]):
        self.joints = len(arm_lengths)
        self.arm_lengths = arm_lengths
        self.thetas = [0 for _ in range(len(arm_lengths))]

    #-- Gets all joint coordinates using geometry equation described in report.
    def get_joint_coordinates(self):
        locations = [(0, 0)]
        start_location = (0, 0)
        theta_total = 0
        for i, theta in enumerate(self.thetas):
            theta_total += theta
            x = start_location[0] + (self.arm_lengths[i] * cos(theta_total))
            y = start_location[1] + (self.arm_lengths[i] * sin(theta_total))
            locations.append((x, y))
            start_location = (x, y)

        return locations

    #-- You can set the robot arm angles
    def set_joint_angles(self, thetas):
        self.thetas = thetas
        return self.get_joint_coordinates()

#-- Method that returns a random theta state in configuration space
def rand_c_space_corrd(num_thetas):
    thetas = []
    for i in range(num_thetas):
        thetas.append(random.uniform(0, 2*pi))
    return thetas

#-- Workspace for the Robot Arm Problem
class Workspace:
    def __init__(self, robot_arm, dim=(10, 10), obstacles=None, c_space_function=rand_c_space_corrd):
        self.robot_arm = robot_arm
        self.dim = dim
        self.obstacles = obstacles
        self.c_space_function = c_space_function

    def c_space_fun(self):
        return self.c_space_function(len(self.robot_arm.thetas))

    def draw_workspace(self):
        fig = graph_workspace(self)
        plt.show()

    def draw_animation(self, path):
        fig = animate_workspace(self, path)
        plt.show()

    def get_animation(self, path):
        ani = animate_workspace_2(self, path)
        plt.show()

    def is_collision(self, thetas=None):
        if self.obstacles is None:
            return False
        for obstacle in self.obstacles:
            if thetas is not None:
                self.robot_arm.set_joint_angles(thetas)
            if obstacle.intersects(LineString(self.robot_arm.get_joint_coordinates())):
                return True
        return False

if __name__ == '__main__':
    robot_arm = RobotArm([1, 1, 1, 1])
    obstacles = [Polygon([(1,1), (1,3), (3,3), (3,1)]),
                 Polygon([(0,-1), (-1,-3), (-3,-3), (-3,-1)])]
    workspace = Workspace(robot_arm, obstacles=obstacles)
    road_map = PRM(10000, 5, workspace)
    solution = road_map.query((pi, 0, pi/7, 0), (.1,.1,.1, 0))
    print(solution)
    workspace.get_animation(solution.path)
