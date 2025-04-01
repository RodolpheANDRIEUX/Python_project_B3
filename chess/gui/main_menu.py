import time
import tkinter as tk

import pandas as pd
from PIL import Image, ImageTk

from chess.chess.game import Game
from chess.chess.move import Move
from chess.gui.board_view import BoardView


def notation_to_coord(move):
    start, end = move.split(', ')
    start_x = 8 - int(start[1])
    start_y = ord(start[0]) - ord('a')
    end_x = 8 - int(end[1])
    end_y = ord(end[0]) - ord('a')
    return (start_x, start_y), (end_x, end_y)


class MainMenu(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Chess")
        self.background_color = '#312e2b'
        self.title_image = Image.open('chess/gui/Title.png')
        self.title_image = ImageTk.PhotoImage(self.title_image)
        self.canvas = tk.Canvas(self, width=self.title_image.width(), height=self.title_image.height())
        self.canvas.create_image(0, 0, anchor='nw', image=self.title_image)
        self.canvas.config(bg=self.background_color, highlightthickness=0)
        self.canvas.grid(row=0, column=0)
        self.menu = MyFrame(self)
        self.configure(bg=self.background_color)
        self.menu.grid(row=1, column=0, padx=200, pady=20)

    def init_game(self, player, review=None):
        for widget in self.winfo_children():
            widget.destroy()
        game = Game(player)
        board_view = BoardView(self, game)
        board_view.grid()
        if player == 0:
            if review is not None:
                self.review(review, game, view=board_view)
            else:
                self.train(game, view=board_view)
                self.init_game(player)

    def train(self, game, view=None, move=0):
        view.update_board(game.board)
        view.update()
        while game.board.end_game is None and move < 1000:
            game.ai_plays()
            view.update_board(game.board)
            view.update()
            move += 1
        if game.board.end_game is not None:
            game.save_game()

    def review(self, review, game, view):
        view.update_board(game.board)
        view.update()
        time.sleep(1)
        games = pd.read_csv('games.csv', sep=';')
        game_to_review = games.iloc[:, review]
        game_to_review = game_to_review.dropna()
        game_to_review = game_to_review.drop(0)
        print(game_to_review)
        for line in game_to_review:
            start_pos, end_pos = notation_to_coord(line)
            piece = game.board.get_piece_at(start_pos[0], start_pos[1])
            move = Move(start_pos, end_pos, piece)
            game.board.select_piece(move.piece.position[0], move.piece.position[1])
            game.board.play(move.end_pos[0], move.end_pos[1])
            game.board.unselect()
            view.update_board(game.board)
            view.update()
            time.sleep(1)


class MyButton(tk.Button):

    def __init__(self, master, id):
        self.id = id
        tk.Button.__init__(self, master, text=self.id)
        self.configure(width=15, height=1)
        self.configure(bg='#81b64c', fg='#ffffff')
        self.configure(font=('Arial', 25, 'bold'))
        self.configure(command=self.function)
        self.configure(activebackground='#b9ca43', activeforeground='#ffffff')
        self.configure(relief=tk.FLAT, bd=5)
        self.configure(cursor='hand2')

    def function(self):
        if self.id == '0 joueur':
            self.master.master.init_game(0)
        elif self.id == '1 joueur':
            self.master.master.init_game(1)
        elif self.id == '2 joueurs':
            self.master.master.init_game(2)
        elif self.id == 'review':
            self.master.master.init_game(0, review=65)


class MyFrame(tk.Frame):

    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.button_list = [MyButton(self, id) for id in ('0 joueur', '1 joueur', '2 joueurs', 'review')]
        self.configure(bg='#3c3b39')
        for k, button in enumerate(self.button_list):
            button.grid(row=k, column=0, padx=20, pady=20)
