from math import pi, sqrt
import random
import numpy as np

import matplotlib.pyplot as plt

from astar_search import astar_search
from GraphRobotArm import animate_workspace

'''
Calculates the angular distance on a n-dimensional toriod space.
'''
def angular_distance(c1, c2):
    di = [abs(c2[i] - c1[i]) for i in range(len(c1))]
    for i in range(len(di)):
        if di[i] > pi:
            di[i] = (2*pi) - di[i]
    return sqrt(sum(np.array(di)**2))

def get_direction_vector(c1, c2):
    vector = [c2[i] - c1[i] if abs(c2[i] - c1[i]) < pi else -((c1[i] - c2[i]) % (2*pi)) for i in range(len(c1))]
    return vector

def get_midpoint(c1, c2):
    d_vector = get_direction_vector(c1, c2)
    print('d_vector', d_vector)
    theta = [(c1[i] + (d_vector[i]*.5)) % (2*pi) 
             if (c1[i] + (d_vector[i]*.5)) > 0 
             else 2*pi + ((c1[i] + (d_vector[i]*.5))) for i in range(len(c1))]
    print('theta', theta)
    return theta

def normalize(edge):
    v1, v2 = edge
    if v1 > v2:
        v2, v1 = v1, v2
    return (v1, v2)

'''
Returns van der Corput sequence
(cite: https://rosettacode.org/wiki/Van_der_Corput_sequence)
'''
def vdc(n, base=2):
    vdc, denom = 0,1
    while n:
        denom *= base
        n, remainder = divmod(n, base)
        vdc += remainder / denom
    return vdc

class PRM:
    def __init__(self, N, k, workspace, delta_q=.05):
        self.k = k
        self.workspace = workspace
        self.delta_q = delta_q
        self.vertices = []
        self.edges = set()

        #-- Builds PRM: Follows psuedo-code in Planning Algorithms Text.
        i = 0
        while i < N:
            alpha_i = self.workspace.c_space_fun()
            if not self.workspace.is_collision(alpha_i):
                self.vertices.append(alpha_i)
                for q in self.neighborhood(alpha_i):
                    if q != alpha_i and self.connect(alpha_i, q):
                        self.edges.add(normalize((tuple(alpha_i), tuple(q))))
                        i += 1


    '''
    Returns neighborhood of new vertex based on angular distance.
    '''
    def neighborhood(self, vertex):
        neighbor_distances = []
        for v in self.vertices:
            neighbor_distances.append((angular_distance(vertex, v), v))
        neighbor_distances.sort()
        if len(neighbor_distances) < self.k:
            return [v for dist, v in neighbor_distances]
        else:
            return [v for dist, v in neighbor_distances[:self.k]]

    '''
    Checking that path is free using the van der Corput-based sampling on the path.
    '''
    def connect(self, v1, v2):
        van_sequence = np.array([vdc(i) for i in range(50)])
        c_sequence = van_sequence
        thetas = []

        #-- Create a vector in c-space based on the given vertices v1 and v2
        vector = get_direction_vector(v1, v2)
        for weight in c_sequence:
            #-- get a theta on the line connecting v1 and v2 that corresponds to the van der Corput weight distance away from v1 but still on the line.
            #-- Start from v1 and v2 to connect path. This will try to connect both ways on the graph.
            theta = [(v1[i] + (vector[i]*weight)) % (2*pi) 
                     if (v1[i] + (vector[i]*weight)) > 0 
                     else 2*pi + ((v1[i] + (vector[i]*weight))) for i in range(len(v1))]
            thetas.append(theta)
            if self.workspace.is_collision(theta):
                return False
            elif angular_distance(v1, theta) < self.delta_q and weight != 0:
                return True
        return True

    def query(self, initial_state, goal_state):
        #-- Set up initial and goal state variables for astar search
        self.start_state = initial_state
        self.goal_state = goal_state

        #-- Connect the Initial and Goal state to the graph.
        for state in [initial_state, goal_state]:
            if not self.workspace.is_collision(state):
                self.vertices.append(state)
                for q in self.neighborhood(state):
                    if q != state and self.connect(state, q):
                        self.edges.add(normalize((tuple(state), tuple(q))))

        #-- Run astar search on the graph.
        solution = astar_search(self, self.angular_distance_heuristic)
        return solution

    #-- Calculates angular distance
    def angular_distance_heuristic(self, next_state):
        return angular_distance(next_state, self.goal_state)

    #-- Calculates Euclidean Distance of Hand.
    def euclid_distance_hand(self, next_state):
        self.workspace.robot_arm.set_joint_angles(self.goal_state)
        goal_coord = self.workspace.robot_arm.get_joint_coordinates()[-1]

        self.workspace.robot_arm.set_joint_angles(next_state)
        state_coord = self.workspace.robot_arm.get_joint_coordinates()[-1]

        return sqrt(sum(np.array([goal_coord[i] - state_coord[i] for i in range(len(state_coord))])**2))

    def goal_test(self, state):
        if state == self.goal_state:
            return True
        return False

    def get_successors(self, state):
        successors = []
        for edge in self.edges:
            if edge[0] == state:
                successors.append(edge[1])
            elif edge[1] == state:
                successors.append(edge[0])
        return successors

    def __str__(self):
        return 'PRM for Robot Arm'

