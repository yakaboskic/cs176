#### Code by: Chase Yakaboski (01/24/2019)

import chess
import copy
import operator
from math import inf
import random

class MinimaxAI():
    def __init__(self, depth, use_table=True, color=False):
        random.seed(2)
        self.color = color
        self.depth = depth
        self.num_calls = 0
        self.heuristic_fn = self.material_heuristic
        self.total_game_calls = 0
        self.transpositionTable = dict()
        self.use_table = use_table

    def choose_move(self, board):
        #-- Run Minimax
        best_move, best_move_dict, num_calls = self.minimax_decision(board)

        #-- Print Results
        print("Minimax AI recommending move " + str(best_move))
        print("Best Move score = " + str(best_move_dict[best_move]))
        print("Number of Calls to Minimax On turn fn = " + str(num_calls))
        print("Number of Calls to Minimax Game = " + str(self.total_game_calls))
        return best_move

    def minimax_decision(self, board):
        self.num_calls = 0

        #-- Get legal moves
        moves = list(board.legal_moves)
        #-- Initialize a best move dictionary to keep the current best move values.
        best_move_dict = dict()

        #-- Iterative Deepening Loop
        for i in range(1, self.depth + 1):
            #--Start of Minimax
            for move in moves:
                #-- Get the min value
                move_score = self.min_value(board, move, i)

                #-- If move is not in the best move dictionary put it in.
                if move in best_move_dict:
                    if best_move_dict[move] <= move_score:
                        best_move_dict[move] = move_score
                #-- Else update the move_score
                else:
                    best_move_dict[move] = move_score

                #-- Undo the move.
                board.pop()

        #-- Get the score of the best move.
        best_score = max(best_move_dict.values())
        #-- If we want to use a Transposition Table hash the board state's best score.
        if self.use_table:
            self.transpositionTable[hash(str(board))] = best_score

        #-- Get all moves with the same score and choose a random move. Found that this helps converge faster to winning.
        best_moves = [k for k, v in best_move_dict.items() if v == best_score]
        best_move = random.choice(best_moves)

        #-- Add the number of calls to Minimax to the total number of calls for the entire game.
        self.total_game_calls += self.num_calls

        return best_move, best_move_dict, self.num_calls

    def min_value(self, board, move, depth):
        #-- Increase number of calls by 1 and push the move.
        self.num_calls += 1
        board.push(move)

        #-- Run cutoff test.
        if self.cutoff_test(board, depth):
            return self.heuristic_fn(board)

        #-- If we've seen the state before just return the that states value from the transposition table. If we're not using the table this will do nothing.
        if hash(str(board)) in self.transpositionTable:
            return self.transpositionTable[hash(str(board))]

        value = inf
        #-- For all children of this new board state call the max_value().
        for child in list(board.legal_moves):
            value = min(value, self.max_value(board, child, depth - 1))
            #-- Undo the move.
            board.pop()

        return value

    def max_value(self, board, move, depth):
        #-- Increase number of calls by 1 and push the move.
        self.num_calls += 1
        board.push(move)

        #-- Run cutoff test.
        if self.cutoff_test(board, depth):
            return self.heuristic_fn(board)

        #-- If we've seen the state before just return the that states value from the transposition table. If we're not using the table this will do nothing.
        if hash(str(board)) in self.transpositionTable:
            return self.transpositionTable[hash(str(board))]

        value = -inf
        #-- For all children of this new board state call the max_value().
        for child in list(board.legal_moves):
            value = max(value, self.min_value(board, child, depth - 1))
            #-- Undo the move.
            board.pop()

        return value

    def cutoff_test(self, board, depth):
        #-- If the game is over or we've reached max depth.
        if board.is_game_over() or depth == 0:
            return True
        else:
            return False

    def material_heuristic(self, board):
        #-- Dictionary of piece index with associated value.
        cost_dict = {1:1, 2:3, 3:3, 4:5, 5:9, 6:90}

        #-- Initialize total cost
        total_cost = 0

        #-- Material Huerstic = AI's pieces - Opponent's pieces with associated costs.
        total_cost +=  sum([cost_dict[piece]*(len(board.pieces(piece, self.color))-len(board.pieces(piece, not self.color))) for piece in range(1,7)])

        #-- If the move gets opponent in check add 100 value, if AI gets in check take 100 away.
        if board.is_check():
            if board.turn is not self.color:
                total_cost += 100
            else:
                total_cost -= 100

        #-- If the move gets opponent in checkimate add 1000 value, if AI gets in check take 1000 away.
        if board.is_checkmate():
            if board.turn is not self.color:
                total_cost += 1000
            else:
                total_cost -= 1000

        return total_cost
