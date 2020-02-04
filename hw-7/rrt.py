# using shapely for collision detection

from shapely.geometry import Polygon, Point

#poly = Polygon(((0, 0), (0, 1), (1, 1), (1, 0)))
#point = Point(2, .2)

#print(poly)
#print(poly.contains(point))

import random
from math import sqrt
import operator
import numpy as np

from planar_trajectory import PlanarTrajectory
from planarsim import *

from PRM import vdc


#-- Helper Node class that keeps track of the trajectory used to get to the point in space along with the state
class RRT_Node:
    def __init__(self, state, trajectory=None, time= None, parent=None):
        self.state = state
        self.trajectory = trajectory
        self.parent = parent
        self.time = time

    #-- Checks if the node is near the goal state.
    def is_near_goal(self, goal_state, goal_range):
        goal_center = Point(goal_state[0], goal_state[1])

        #-- Create a circle around goal state
        goal_circle_buffer = goal_center.buffer(goal_range)
        state_point = Point(self.state[0], self.state[1])
        if state_point.within(goal_circle_buffer):
            return True
        else:
            return False

    def __repr__(self):
        return repr((self.state[0]))

    def __str__(self):
        return '(%s, %s, %s)' % tuple([str(el) for el in self.state])

#-- The main class for RRT.
class RRT:
    def __init__(self, workspace,  initial_state, goal_state, k, goal_range=1, step_threshold=.05, num_rand_actions=1, max_control_time=5):
        self.workspace = workspace
        self.initial_state = initial_state
        self.goal_state = goal_state
        self.k = k
        self.goal_range = goal_range
        self.step_threshold = step_threshold
        self.num_rand_actions = num_rand_actions
        self.max_control_time = max_control_time

        self.vertices = []

    def build_rrt(self):
        self.vertices.append(RRT_Node(self.initial_state))
        for i in range(self.k):
            if i % 100 == 0:
                alpha = tuple(self.goal_state[:2])
            else:
                #-- Generate random (x, y) point in the workspace
                alpha = (random.uniform(0, self.workspace.dim[0]), random.uniform(0, self.workspace.dim[1]))

            #-- Get Node in the graph closest to alpha
            q_n = self.nearest(alpha)

            #-- Expand nearest Node with random trajectory
            #-- Based on how many explorations for a node, given by user, fill create random action list.
            rand_actions = set()
            while len(rand_actions) < self.num_rand_actions:
                rand_actions.add(random.randint(0,5))

            #-- get a duration of the action by sampling from 0 to max duration time.
            rand_time = random.uniform(0, self.max_control_time)
            for rand_action in rand_actions:
                #-- Build a Planar Trajectory and get the end point configuration of the action.
                rand_traj = PlanarTrajectory(controls_rs, q_n.state[0], q_n.state[1], q_n.state[2], [rand_action], [rand_time])
                rand_config_from_traj = rand_traj.config_at_t(rand_time - .0001)


                #-- Make sure there is no collision
                if self.connect(rand_traj, rand_time - .0001):
                    q_s = RRT_Node(rand_config_from_traj, rand_traj, rand_time - .0001, q_n)
                    self.vertices.append(q_s)
                    #-- If we've reached the goal start backtracking
                    if q_s.is_near_goal(self.goal_state, self.goal_range):
                        print('Found after', i)
                        return backchain(q_s)
        return False

    #-- Get the point with closet euclidean distance
    def nearest(self, alpha):
        distances = []
        for node in self.vertices:
            distances.append((sqrt((node.state[0] - alpha[0])**2 + (node.state[1] - alpha[1])**2), node))
        distances = sorted(distances, key=operator.itemgetter(0))
        return distances[0][1]

    #-- Using the van der Corput Sequence sample the action path and make sure no collisions occur.
    def connect(self, traj, end_time):
        van_sequence = np.array([vdc(i) for i in range(50)])
        for coef in van_sequence:
            t = coef*end_time
            if self.workspace.is_collision(traj.config_at_t(t)):
                return False
            #-- If the sample distance is less than the user specified threshold exit with no collision
            elif sqrt((traj.q[0] - traj.config_at_t(t)[0])**2 + (traj.q[1] - traj.config_at_t(t)[1])**2) < self.step_threshold and t != 0:
                return True
        return True

def backchain(node):
    result = []
    current = node
    while current:
        result.append(current)
        current = current.parent

    result.reverse()
    return result
