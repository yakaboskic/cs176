#### Code by: Chase Yakaboski (01/24/2019)

import chess
from RandomAI import RandomAI
from HumanPlayer import HumanPlayer
from MinimaxAI import MinimaxAI
from ChessGame import ChessGame, get_random_board
from AlphaBetaAI import AlphaBetaAI

#-- This is a test file detailing certian scenarios of interest. If you want to play chess go to the test_chess.py file.

def run_test_1():
    print('------- Scenario 1: Equivance of Minimax and AlphaBeta --------')
    #-- Scenario 1: Test to make sure MiniMaxAI and AlphaBetaAI are giving the same results
    #-- Here are the various players.
    player_human = HumanPlayer()
    player_mini = MinimaxAI(3, color=True)
    player_alphaBeta = AlphaBetaAI(3, color=True)

    #-- Set up the board in a the following fashion. Remember our AIs are WHITE in these scenarios.
    game = ChessGame(player_human, player_mini)
    game.board.clear_board()
    game.board.set_piece_at(piece=chess.Piece(4, False), square=16)
    game.board.set_piece_at(piece=chess.Piece(2, False), square=8)
    game.board.set_piece_at(piece=chess.Piece(3, False), square=10)
    game.board.set_piece_at(piece=chess.Piece(3, True), square=1)

    #-- Display the board and possible moves.
    print(game)
    print("Possible Moves:")
    for move in game.board.pseudo_legal_moves:
        print(move)

    print('---------------------------')

    #-- Look at the choice for MinimaxAI:
    print('Chosen Move:', player_mini.choose_move(game.board))
    print('---------------------------')

    #-- Look at the choice for AlphaBetaAI:
    print('Chosen Move:', player_alphaBeta.choose_move(game.board))
    print('---------------------------')

    #-- We can see that for the same depth, and same board configuration, we get the same move results for each AI.


def run_test_2():
    print('------- Scenario 2: Take the Win! --------')
    #-- Scenario 2: Test to make dure MiniMax and AlphaBetaAI take the win for a more complicated scenario (4 more checkmate) in a predefined position.
    #-- Here are the various players.
    player_human = HumanPlayer()
    player_mini = MinimaxAI(3, color=True)
    player_alphaBeta = AlphaBetaAI(3, color=True)

    game = ChessGame(player_human, player_mini)
    game.board.reset()
    game.board.push(chess.Move(12,28))
    game.board.push(chess.Move(52, 36))
    game.board.push(chess.Move(5, 26))
    game.board.push(chess.Move(57, 42))
    game.board.push(chess.Move(3, 39))
    game.board.push(chess.Move(62, 45))

    #-- Display Board
    print(game)
    print('---------------------------')

    #-- Look at choice for MiniMaxAI
    print('Chosen Move:', player_mini.choose_move(game.board))
    print('---------------------------')

    #-- Look at choice for AlphaBetaAI
    print('Chosen Move:', player_alphaBeta.choose_move(game.board))
    print('---------------------------')

    #-- Both AIs take the win with the same move.

def run_test_3():
    #-- Re-ordering test in Alpha-Beta Pruning.
    player_alphaBeta_reorder = AlphaBetaAI(3, use_table=False, move_reorder=True)
    player_alphaBeta_noReorder = AlphaBetaAI(3, use_table=False, move_reorder=False)
    print('------ Run With Reorder Table --------')
    game1 = run_game(player_alphaBeta_reorder)

    print('------ Run WithOut Reorder Table --------')
    game2 = run_game(player_alphaBeta_noReorder)

    print('--------- Results ------------')
    print('Total Game fn calls with reorder:', game1.players[1].total_game_calls)
    print('Total Game fn calls without reorder:', game2.players[1].total_game_calls)



def run_test_4():
    #-- Transposition Table Test: Here we run the game for 10 moves for the AlphaBetaAI. We play against a random AI with a set seed in order to replicate results, the first run we use the transposition table and the second we do not. 
    
    #-- Here are the various players.
    player_alphaBeta_Trans = AlphaBetaAI(3, use_table=True)
    player_alphaBeta_noTrans = AlphaBetaAI(3, use_table=False)

    print('------ Run With transposition Table --------')
    game1 = run_game(player_alphaBeta_Trans)

    print('------ Run WithOut transposition Table --------')
    game2 = run_game(player_alphaBeta_noTrans)

    print('--------- Results ------------')
    print('Total Game fn calls with transposition table:', game1.players[1].total_game_calls)
    print('Total Game fn calls without transposition table:', game2.players[1].total_game_calls)

def run_test_5():
    #-- Iterative Deepening Test: Make sure that the deeper you go the better answer you get.
    #-- Set board.
    board = get_random_board(26)
    print(board)

    #-- Set up players
    player2 = MinimaxAI(2, color=True)
    player3 = MinimaxAI(3, color=True)
    player4 = MinimaxAI(4, color=True)
    playera2 = AlphaBetaAI(2, color=True)
    playera3 = AlphaBetaAI(3, color=True)
    playera4 = AlphaBetaAI(4, color=True)

    #-- Get move scores from different depths
    player2.choose_move(board)
    player3.choose_move(board)
    player4.choose_move(board)

    print('---------------------')

    playera2.choose_move(board)
    playera3.choose_move(board)
    playera4.choose_move(board)


def run_game(player2, move_num=20):
    player1 = RandomAI()
    game = ChessGame(player1, player2)
    for _ in range(move_num):
        print(game)
        game.make_move()
    return game



if __name__ == '__main__':
    run_test_1()
    run_test_2()
    run_test_3()
    run_test_4()
    run_test_5()
