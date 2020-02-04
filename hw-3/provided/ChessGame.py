### Code by: Chase Yakaboski (01/24/2019)

import chess
import random
import copy

class ChessGame:
    def __init__(self, player1, player2):
        self.board = chess.Board()
        self.players = [player1, player2]

    def make_move(self):

        player = self.players[1 - int(self.board.turn)]
        move = player.choose_move(self.board)

        self.board.push(move)  # Make the move

    def is_game_over(self):
        return self.board.is_game_over()

    def __str__(self):

        column_labels = "\n----------------\na b c d e f g h\n"
        board_str =  str(self.board) + column_labels

        # did you know python had a ternary conditional operator?
        move_str = "White to move" if self.board.turn else "Black to move"

        return board_str + "\n" + move_str + "\n"

def get_random_board(seed=222):
    #-- set random seed to get reproduciable results
    random.seed(seed)

    #-- Get random number of white and black pieces to be put on the board
    num_white = random.randint(1, 16)
    num_black = random.randint(1, 16)

    #-- Initialize Board
    board = chess.Board()
    board.clear_board()

    #-- List of all open board positions
    open_positions = [i for i in range(64)]
    #-- Shuffle it cause we're just gonna pop them off later. 
    random.shuffle(open_positions)
    #-- Index of all pieces that can be chosen for white and black.
    pieces = [1,1,1,1,1,1,1,1,2,2,3,3,4,4,5]
    other_pieces_white = copy.deepcopy(pieces)
    other_pieces_black = copy.deepcopy(pieces)
    #-- Shuffle so we can just pop off a random piece
    random.shuffle(other_pieces_black)
    random.shuffle(other_pieces_white)
    
    #-- Set positions for Kings
    board.set_piece_at(open_positions.pop(), chess.Piece(6, True))
    board.set_piece_at(open_positions.pop(), chess.Piece(6, False))

    #-- Set other random pieces in random positions
    for _ in range(num_white - 1):
        board.set_piece_at(open_positions.pop(), chess.Piece(other_pieces_white.pop(), True))
    for _ in range(num_black - 1):
        board.set_piece_at(open_positions.pop(), chess.Piece(other_pieces_black.pop(), False))

    return board


