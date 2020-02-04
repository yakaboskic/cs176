from RobotArm import Workspace, RobotArm
from PRM import angular_distance, get_direction_vector, get_midpoint

from math import pi

if __name__ == '__main__':
    c1 = [1.25*pi, 0]
    c2 = [.75*pi, 0]
    print('c1', c1)
    print('c2', c2)

    mid = get_midpoint(c1, c2)

    path = [c1, mid, c2]

    robot_arm = RobotArm([1,2])
    workspace = Workspace(robot_arm)

    workspace.draw_animation(path)
