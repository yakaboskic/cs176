import numpy as np


class Solution:
    '''
    Generic Solution class with problem specific printing methods. 
    '''
    def __init__(self, problem):
        self.problem = problem
        self.updates = []
        self.updates_smoothed = []
        self.final = None
        self.final_smoothed = None


    def robot_string(self):
        string = 'Maze:\n\n'
        string += self.problem.maze.__str__()
        string += '\nFinal Distribution (Unsmoothed):\n'
        for x in range(self.problem.maze.width):
            for y in range(self.problem.maze.height):
                string += '\t(%s, %s): %s\n' % (x, y, self.final[self.problem.maze.index(x, y)])
        #if self.final_smoothed is not None:
        #    string += '\nFinal Distribution (Smoothed):\n'
        #    for x in range(self.problem.maze.width):
        #        for y in range(self.problem.maze.height):
        #            string += '\t(%s, %s): %s\n' % (x, y, self.final_smoothed[self.problem.maze.index(x, y)])
        return string

    def umbrella_string(self):
        string = '\nFinal Distribution (Unsmoothed):\n'
        string += '\tRain: %s\n' % (self.final[0])
        string += '\tNot Rain: %s\n' % (self.final[1])
        if self.final_smoothed is not None:
            string += '\nFinal Distribution (Smoothed):\n'
            string += '\tRain: %s\n' % (self.final_smoothed[0])
            string += '\tNot Rain: %s\n' % (self.final_smoothed[1])
        return string

    def __str__(self):
        if self.problem.name == 'umbrella':
            return self.umbrella_string()
        else:
            return self.robot_string()


class HMM:
    '''
    Hidden Markov Model Class.
        A problem object needs a transition model, sensor model, and initial state.
    '''
    def __init__(self, problem):
        self.problem = problem
        self.solution = Solution(problem)

    def reason(self, evidence):
        '''
        This is just the forward half of the forward-backward algorithm. Just reasons forward in time. 
        '''
        prior_state = self.problem.initial_state
        for e_ in evidence:
            new_state = self.forward(prior_state, e_)
            self.solution.updates.append(new_state)

            prior_state = new_state
        self.solution.final = prior_state

        return self.solution

    #def viterbi(self, evidence):
    #    v_ = forward(self.problem.initial_state, evidence[0])
    #    for i in range(1, len(evidence)):
    #        v_p = np.array([-np.Inf, -np.inf])
    #        for j in range(len(v_)):
    #            for k in range(len(v_)):
    #                v_p[0] = max(v_p[0], np.matmul(self.get_observation_matrix(evidence[i])v_[0]*self.problem.transition_model[j,k]

    def forward_backward(self, evidence):
        '''
        Implementation of Forward-Backward Algorithm, psuedocode on page 586 of text. 
        '''
        #-- Set initial states
        fv_ = self.problem.initial_state
        self.solution.updates.append(fv_)
        b_ = np.ones((len(fv_),))

        #-- Conduct Forward recursion and save in solution object
        for e_ in evidence:
            fv_ = self.forward(fv_, e_)
            self.solution.updates.append(fv_)

        #-- Conduct Backward recursion
        for i in range(len(evidence), 0, -1):
            #-- Need to look at update i + 1 since we are off by one index. 
            sv_ = self.normalize(self.solution.updates[i] * b_)
            b_ = self.backward(b_, evidence[i-1])
            self.solution.updates_smoothed.append(sv_)

        #-- reverse the order.
        self.solution.updates_smoothed.reverse()

        #-- Bookkeeping
        self.solution.final = self.solution.updates[-1]
        self.solution.final_smoothed = self.solution.updates_smoothed[-1]

        return self.solution


    def forward(self, last_state, new_evidence):
        '''
        Matrix Implementation of equation 5.12 in text.
        '''
        p_state = np.matmul(self.problem.transition_model, last_state)
        p_state = np.matmul(self.get_observation_matrix(self.problem.sensor_model[:, new_evidence]), p_state)
        return self.normalize(p_state)

    def backward(self, b_message, evidence):
        '''
        Matrix Implementation of equation 5.13 in text
        '''
        p_state = np.matmul(self.get_observation_matrix(self.problem.sensor_model[:, evidence]), b_message)
        p_state = np.matmul(self.problem.transition_model, p_state)
        return self.normalize(p_state)

    #-- Takes a column vector based on the observation and constructs a diagonal matrix.
    def get_observation_matrix(self, column_vector):
        return np.diag(column_vector)


    def normalize(self, probability_vector):
        return probability_vector/sum(probability_vector)

