# pip3 install python-chess


import chess
from RandomAI import RandomAI
from HumanPlayer import HumanPlayer
from MinimaxAI import MinimaxAI
from AlphaBetaAI import AlphaBetaAI
from ChessGame import ChessGame


import sys


#player1 = HumanPlayer()
player1 = RandomAI()
#player2 = MinimaxAI(3)
player2 = AlphaBetaAI(3)

game = ChessGame(player1, player2)

while not game.is_game_over():
    print(game)
    game.make_move()
print('Result', game.board.result())

#print(hash(str(game.board)))
