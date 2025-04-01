import copy
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import pygame
from chess.chess.move import Move
from chess.chess.piece import King, Queen, Pawn, Bishop, Rook, Knight


def play_mp3(file_path):
    pygame.mixer.init()
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()


def initialize_board():
    grid = [[None for _ in range(8)] for _ in range(8)]
    for i in range(8):
        grid[1][i] = Pawn('black', (1, i))
        grid[6][i] = Pawn('white', (6, i))
    grid[0][4] = King('black', (0, 4))
    grid[7][4] = King('white', (7, 4))
    grid[0][3] = Queen('black', (0, 3))
    grid[7][3] = Queen('white', (7, 3))
    grid[0][0] = Rook('black', (0, 0))
    grid[0][7] = Rook('black', (0, 7))
    grid[7][0] = Rook('white', (7, 0))
    grid[7][7] = Rook('white', (7, 7))
    grid[0][1] = Knight('black', (0, 1))
    grid[0][6] = Knight('black', (0, 6))
    grid[7][1] = Knight('white', (7, 1))
    grid[7][6] = Knight('white', (7, 6))
    grid[0][2] = Bishop('black', (0, 2))
    grid[0][5] = Bishop('black', (0, 5))
    grid[7][2] = Bishop('white', (7, 2))
    grid[7][5] = Bishop('white', (7, 5))
    play_mp3('chess/sounds/move.mp3')
    return grid


class Board:
    def __init__(self):
        self.check = None  # store the color of the player in check if any
        self.pieces = initialize_board()
        self.parallel_universe = initialize_board()  # used to imagine the terrible consequences of a move
        self.valid_moves = [[False for _ in range(8)] for _ in range(8)]
        self.selected_piece = None
        self.last_move = None
        self.end_game = None  # None, white (won), black (won), draw

    def move_piece(self, move):
        self.pieces[move.end_pos[0]][move.end_pos[1]] = move.piece
        self.pieces[move.start_pos[0]][move.start_pos[1]] = None
        move.piece.position = move.end_pos

    def undo_move(self, move):
        self.pieces[move.start_pos[0]][move.start_pos[1]] = move.piece
        self.pieces[move.end_pos[0]][move.end_pos[1]] = None
        move.piece.position = move.start_pos

    def play(self, i, j):
        move = Move(self.selected_piece.position, (i, j), self.selected_piece)
        self.move_piece(move)
        play_mp3('chess/sounds/move.mp3')
        self.selected_piece.move(i, j)
        if self.valid_moves[i][j] == 'castle':
            self.castle(i, j)
        if self.valid_moves[i][j] == 'en passant':
            self.en_passant(i, j)
        if self.valid_moves[i][j] == 'promotion':
            print("promotion")
            self.promote(i, j)
        self.last_move = move
        self.analyse_board()  # check, checkmate, stalemate

    def handle_square_selection(self, i, j, player):
        if self.end_game is not None:
            return
        if self.selected_piece is not None:
            if self.is_valid_move(i, j):
                self.play(i, j)
                self.unselect()
                return True
        self.unselect()
        selection_request = self.get_piece_at(i, j)
        if selection_request is not None and selection_request.color == player:
            self.select_piece(i, j)

    def select_piece(self, i, j):
        self.selected_piece = self.pieces[i][j]
        self.selected_piece.select()
        self.valid_moves = self.selected_piece.valid_moves(self)
        for i in range(8):
            for j in range(8):
                if self.valid_moves[i][j]:
                    move = Move(self.selected_piece.position, (i, j), self.selected_piece)
                    if not self.king_safe(move):
                        self.valid_moves[i][j] = False

    def unselect(self):
        self.selected_piece = None
        self.valid_moves = [[False for _ in range(8)] for _ in range(8)]

    def get_piece_at(self, i, j):
        return self.pieces[i][j]  # return the piece object at i,j

    def is_valid_move(self, i, j):
        return self.valid_moves[i][j]  # return True if there is a valid move active on the board at i, j (also
        # 'castle' and 'en passant' moves)

    def king_safe(self, move):
        temp_pieces = copy.deepcopy(self.pieces)
        self.move_piece(move)
        safe = True
        for i in range(8):
            for j in range(8):
                piece = self.get_piece_at(i, j)
                if piece is not None and piece.color != move.piece.color:
                    valid_enemy_moves = piece.valid_moves(self)
                    for row in range(8):
                        for col in range(8):
                            if not valid_enemy_moves[row][col] is False:
                                piece_threatened = self.get_piece_at(row, col)
                                if isinstance(piece_threatened, King) and piece_threatened.color == move.piece.color:
                                    safe = False
                                    break
        self.undo_move(move)
        self.pieces = temp_pieces
        return safe

    def castle(self, i, j):
        if i == 0:
            if j == 2:
                print("O-O-O")
                rook = self.get_piece_at(0, 0)
                rook_move = Move((0, 0), (0, 3), rook)
                self.move_piece(rook_move)
                rook.move(0, 3)
            elif j == 6:
                print("O-O")
                rook = self.get_piece_at(0, 7)
                rook_move = Move((0, 7), (0, 5), rook)
                self.move_piece(rook_move)
                rook.move(0, 5)
        elif i == 7:
            if j == 2:
                print("O-O-O")
                rook = self.get_piece_at(7, 0)
                rook_move = Move((7, 0), (7, 3), rook)
                self.move_piece(rook_move)
                rook.move(7, 3)
            elif j == 6:
                print("O-O")
                rook = self.get_piece_at(7, 7)
                rook_move = Move((7, 7), (7, 5), rook)
                self.move_piece(rook_move)
                rook.move(7, 5)
        else:
            print("Invalid castle move")

    def analyse_board(self):
        self.check_check()
        self.check_checkmate()  # and stalemate

    def check_check(self):
        for i in range(8):
            for j in range(8):
                piece = self.get_piece_at(i, j)
                if piece is not None and piece.color == self.selected_piece.color:  # for every piece of the current p
                    valid_moves = piece.valid_moves(self)
                    for row in range(8):
                        for col in range(8):
                            if not valid_moves[row][col] is False and self.get_piece_at(row, col) is not None:  # for
                                # every valid move that takes
                                if isinstance(self.get_piece_at(row, col), King):
                                    self.check = self.selected_piece.color == 'white' and 'black' or 'white'
                                    print(f"{self.check} king in check")
                                    return
        self.check = None

    def check_checkmate(self):
        for i in range(8):
            for j in range(8):
                piece = self.get_piece_at(i, j)
                enemy = self.selected_piece.color == 'white' and 'black' or 'white'
                if piece is not None and piece.color == enemy:
                    valid_moves = piece.valid_moves(self)
                    for row in range(8):
                        for col in range(8):
                            if not valid_moves[row][col] is False:
                                move = Move((i, j), (row, col), piece)
                                if self.king_safe(move):
                                    return
        if self.check is not None:
            self.end_game = "white" if self.check == 'black' else "black"
            print(f"{self.check} king in checkmate")
        else:
            self.end_game = 'draw'
            print("stalemate")

    def promote(self, i, j):
        self.pieces[i][j] = Queen(self.selected_piece.color, (i, j))

    def en_passant(self, i, j):
        pawn_to_eliminate_direction = 1 if self.selected_piece.color == 'white' else -1
        self.pieces[i + pawn_to_eliminate_direction][j] = None
