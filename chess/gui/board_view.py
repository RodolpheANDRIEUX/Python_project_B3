import tkinter as tk
from PIL import Image, ImageTk


class BoardView(tk.Frame):
    def __init__(self, master, game):
        super().__init__(master)
        self.game = game
        self.squares = None
        self.square_size = 80
        self.theme = ['#ebecd0', '#739552']
        self.current_selected_square = None
        self.create_widgets()
        self.piece_images = {}
        self.load_images()
        self.update_board(self.game.board)

    def create_widgets(self):
        self.squares = {}
        for i in range(8):
            for j in range(8):
                square = Square(self.theme[(i + j) % 2], self.square_size)
                square.grid(row=i, column=j)
                square.bind('<Button-1>', lambda event, i=i, j=j: self.square_click(i, j))
                self.squares[(i, j)] = square

    def square_click(self, i, j):
        if self.current_selected_square is not None:
            self.squares[self.current_selected_square].deselect()
        self.squares[(i, j)].select()
        self.current_selected_square = (i, j)
        self.game.handle_square_selection(i, j)
        self.update_board(self.game.board)

    def load_images(self):
        pieces = ['bp', 'br', 'bn', 'bb', 'bq', 'bk', 'wp', 'wr', 'wn', 'wb', 'wq', 'wk', 'vm', 'vt']
        for piece in pieces:
            image = Image.open(f"chess/pieces/{piece}.png")
            image = image.resize((self.square_size, self.square_size))
            self.piece_images[piece] = ImageTk.PhotoImage(image)

    def update_board(self, board):
        for i in range(8):
            for j in range(8):
                self.squares[(i, j)].delete('all')
                piece = board.get_piece_at(i, j)
                if piece is not None:
                    self.squares[(i, j)].create_image(
                        self.square_size // 2,
                        self.square_size // 2,
                        image=self.piece_images[f'{piece}'], anchor='center')
                if board.is_valid_move(i, j):
                    if board.get_piece_at(i, j) is not None:
                        self.squares[(i, j)].create_image(
                            self.square_size // 2,
                            self.square_size // 2,
                            image=self.piece_images['vt'], anchor='center')
                    else:
                        self.squares[(i, j)].create_image(
                            self.square_size // 2,
                            self.square_size // 2,
                            image=self.piece_images['vm'], anchor='center')


class Square(tk.Canvas):
    def __init__(self, color, size):
        tk.Canvas.__init__(self, width=size, height=size, bg=color, highlightthickness=0)
        self.size = size
        self.color = color

    def select(self):
        self.config(bg='#b9ca43') if self.color == '#739552' else self.config(bg='#f5f682')

    def deselect(self):
        self.config(bg=self.color)
