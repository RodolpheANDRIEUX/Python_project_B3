import os

from chess.chess.ai import Ai
from chess.chess.board import Board
from chess.chess.player import Player
import pandas as pd


def not_algebraic_notation(move):
    return 'abcdefgh'[move.start_pos[1]] + str(8 - move.start_pos[0]) + ', ' + 'abcdefgh'[move.end_pos[1]] + str(
        8 - move.end_pos[0])


class Game:
    def __init__(self, player, board_view=None):
        self.board_view = board_view
        self.player_number = player
        self.board = Board()
        self.players = self.init_players()
        self.moves = pd.Series([])
        self.current_turn = "white"

    def init_players(self):
        if self.player_number == 2:
            return [Player("white"), Player("black")]
        if self.player_number == 1:
            return [Player(self.board), Ai(self.board)]
        if self.player_number == 0:
            return [Ai(self.board, color='white'), Ai(self.board)]

    def switch_turn(self):
        self.current_turn = "black" if self.current_turn == "white" else "white"

    def handle_square_selection(self, i, j):
        if self.board.handle_square_selection(i, j, self.current_turn):  # if move was played eventually
            self.save_move(self.board.last_move)
            if self.board.end_game is not None:
                self.save_game()
                return
            self.switch_turn()
            if self.player_number == 1:
                self.ai_plays()
            if self.board.end_game is not None:
                self.save_game()

    def ai_plays(self):
        if self.current_turn == "black":
            move = self.players[1].play_random()
        else:
            move = self.players[0].play_random()
        self.board.select_piece(move.piece.position[0], move.piece.position[1])
        self.board.play(move.end_pos[0], move.end_pos[1])
        self.board.unselect()
        self.save_move(move)
        self.switch_turn()

    def save_move(self, move):
        event = not_algebraic_notation(move)
        self.moves = pd.concat([self.moves, pd.Series([event])], ignore_index=True)

    def save_game(self):
        if self.board.end_game == 'white':
            self.moves = pd.concat([pd.Series(['1 - 0']), self.moves], ignore_index=True)
        if self.board.end_game == 'black':
            self.moves = pd.concat([pd.Series(['0 - 1']), self.moves], ignore_index=True)
        if self.board.end_game == 'draw':
            self.moves = pd.concat([pd.Series(['0 - 0']), self.moves], ignore_index=True)

        if 'games.csv' in os.listdir():
            existing_games = pd.read_csv('games.csv', sep=';', index_col=0)
            self.moves.name = existing_games.shape[1] + 1
            self.moves = pd.concat([existing_games, self.moves], axis=1)
        else:
            self.moves.name = 1
        self.moves.to_csv('games.csv', sep=';')
