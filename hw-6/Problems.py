from mazeworld.Maze import Maze
import numpy as np
from time import sleep


class UmbrellaProblem:
    '''
    Implemenation of Umbrella World.
        Used to check answers with book. 
    '''
    def __init__(self, deterministic_sensor=False):
        self.name = 'umbrella'
        self.initial_state = np.array([.5, .5])
        self.transition_model = np.array([[.7, .3], [.3, .7]])
        self.sensor_model = np.array([[.1, .9], [.8, .2]])


class RobotProblem:
    '''
    Robot Problem Class.
        - Loads in a colored maze file and builds a transition matrix and sensor model and initial state based on the maze parameters. 
    '''
    def __init__(self, maze_file, deterministic_sensor=False):
        self.name = 'robot'
        self.maze_file = maze_file
        self.maze = Maze(maze_file)

        #-- Uniform initial state based on maze size. 
        self.initial_state = [1/(self.maze.height*self.maze.width) for i in range(self.maze.height*self.maze.width)]

        actions = [(1,0), (-1,0), (0,1), (0,-1)]
        neighbors = dict()
        for x in range(self.maze.width):
            for y in range(self.maze.height):
                neighbors[self.maze.index(x, y)] = []
                for action in actions:
                    x1 = x + action[0]
                    y1 = y + action[1]
                    if self.maze.is_floor(x1, y1):
                        neighbors[self.maze.index(x, y)].append(self.maze.index(x1, y1))

        #-- Initialize a Transition Matrix
        self.transition_model = np.zeros((len(self.initial_state), len(self.initial_state)))
        for i in range(len(self.initial_state)):
            #-- Probability that you stay in the same cell:
            prob_stay = .2 + .2*(4 - len(neighbors[i]))
            self.transition_model[i, i] = prob_stay
            #-- Probability that you transition to a neighbor:
            for j in neighbors[i]:
                self.transition_model[i, j] = .2

        self.color_map = {0: 'r', 1: 'b', 2: 'g', 3: 'y'}
        self.inverse_color_map = {s: i for i, s in self.color_map.items()}

        #-- Initialize Sensor Model
        self.sensor_model = np.zeros((len(self.initial_state), 4))
        for x in range(self.maze.width):
            for y in range(self.maze.height):
                ind = self.maze.index(x, y)
                if self.maze.is_floor(x, y):
                    cell_color = self.maze.map[ind]
                    for color in range(4):
                        if cell_color == self.color_map[color]:
                            if deterministic_sensor:
                                self.sensor_model[ind, color] = 1.0
                            else:
                                self.sensor_model[ind, color] = 0.88
                        else:
                            if deterministic_sensor:
                                self.sensor_model[ind, color] = 0.0
                            else:
                                self.sensor_model[ind, color] = 0.04


    def get_ground_truth(self, path):
        truth = []
        for state in path:
            color = self.maze.map[self.maze.index(state[0], state[1])]
            truth.append(self.inverse_color_map[color])
        return truth


    def animate_path(self, path, solution):
        print('Time: %s' % 0)
        print(str(self.maze))
        string = '\nDistribution (Unsmoothed):\n'
        for x in range(solution.problem.maze.width):
            for y in range(solution.problem.maze.height):
                string += '\t(%s, %s): %s\n' % (x, y, solution.updates[0][solution.problem.maze.index(x, y)])
        print(string)
        for i, state in enumerate(path):
            print('Time: %s' % (i+1))
            self.maze.robotloc = tuple(state)
            print(str(self.maze))
            string = '\nDistribution (Unsmoothed):\n'
            for x in range(solution.problem.maze.width):
                for y in range(solution.problem.maze.height):
                    string += '\t(%s, %s): %s\n' % (x, y, solution.updates[i+1][solution.problem.maze.index(x, y)])
            if solution.final_smoothed is not None:
                string += '\nDistribution (Smoothed):\n'
                for x in range(solution.problem.maze.width):
                    for y in range(solution.problem.maze.height):
                        string += '\t(%s, %s): %s\n' % (x, y, solution.updates_smoothed[i][solution.problem.maze.index(x, y)])
            print(string)
            sleep(1)
