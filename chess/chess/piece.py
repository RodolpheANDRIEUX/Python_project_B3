def chess_notation(piece, x, y):
    piece_name = piece[1].upper() if not piece[1] == 'p' else ''
    return piece_name + chr(ord('a') + x) + str(8 - y) + ','


class Piece:
    def __init__(self, color, position):
        self.color = color
        self.position = position

    def valid_moves(self, board):
        pass  # return a list of valid moves

    def select(self):
        pass

    def move(self, i, j):
        print(chess_notation(str(self), j, i))
        self.position = (i, j)

    def __str__(self):
        return f"{self.color[0]} {self.__class__.__name__}"


class King(Piece):
    def __init__(self, color, position):
        super().__init__(color, position)
        self.has_moved = False

    def __str__(self):
        return f"{self.color[0]}k"

    def move(self, i, j):
        print(chess_notation(str(self), j, i))
        self.position = (i, j)
        self.has_moved = True

    def valid_moves(self, board):
        moves = [[False for _ in range(8)] for _ in range(8)]
        i, j = self.position
        for row in range(i - 1, i + 2):
            for col in range(j - 1, j + 2):
                if 0 <= row < 8 and 0 <= col < 8 and (row != i or col != j):
                    if board.get_piece_at(row, col) is None or board.get_piece_at(row, col).color != self.color:
                        moves[row][col] = True
        if not self.has_moved and not board.check == self.color:
            if board.get_piece_at(i, 1) is None and board.get_piece_at(i, 2) is None and board.get_piece_at(i,
                                                                                                            3) is None:
                rook = board.get_piece_at(i, 0)
                if isinstance(rook, Rook) and not rook.has_moved:
                    moves[i][2] = 'castle'
            if board.get_piece_at(i, 5) is None and board.get_piece_at(i, 6) is None:
                rook = board.get_piece_at(i, 7)
                if isinstance(rook, Rook) and not rook.has_moved:
                    moves[i][6] = 'castle'
        return moves


class Queen(Piece):
    def __str__(self):
        return f"{self.color[0]}q"

    def valid_moves(self, board):
        moves = [[False for _ in range(8)] for _ in range(8)]
        i, j = self.position
        directions = [
            (1, 0), (-1, 0), (0, 1), (0, -1),  # vertical and horizontal
            (1, 1), (1, -1), (-1, 1), (-1, -1)  # diagonal
        ]

        for dx, dy in directions:
            nx, ny = i, j
            while True:
                nx += dx
                ny += dy
                if 0 <= nx < 8 and 0 <= ny < 8:
                    piece = board.get_piece_at(nx, ny)
                    if piece is None:
                        moves[nx][ny] = True
                    elif piece.color != self.color:
                        moves[nx][ny] = True
                        break
                    else:
                        break
                else:
                    break
        return moves


class Pawn(Piece):
    def __str__(self):
        return f"{self.color[0]}p"

    def valid_moves(self, board):
        moves = [[False for _ in range(8)] for _ in range(8)]
        i, j = self.position
        direction = -1 if self.color == 'white' else 1
        if 0 <= i + direction < 8 and board.get_piece_at(i + direction, j) is None:
            moves[i + direction][j] = True
            if (i == 1 and self.color == 'black') or (i == 6 and self.color == 'white'):
                if board.get_piece_at(i + 2 * direction, j) is None:
                    moves[i + 2 * direction][j] = True
        for dx in [-1, 1]:
            if 0 <= i + direction < 8 and 0 <= j + dx < 8:
                piece = board.get_piece_at(i + direction, j + dx)
                if piece is not None and piece.color != self.color:
                    moves[i + direction][j + dx] = True
                if board.last_move is not None and isinstance(board.last_move.piece, Pawn):
                    if board.last_move.start_pos[0] == i + 2 * direction and board.last_move.end_pos[0] == i and board.last_move.end_pos[1] == j + dx:
                        moves[i + direction][j + dx] = 'en passant'
        for row in range(8):
            if i + direction == 0 or i + direction == 7:
                if moves[0 if self.color == 'white' else 7][row] is not False:
                    moves[0 if self.color == 'white' else 7][row] = 'promotion'
        return moves


class Bishop(Piece):
    def __str__(self):
        return f"{self.color[0]}b"

    def valid_moves(self, board):
        moves = [[False for _ in range(8)] for _ in range(8)]
        i, j = self.position
        directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
        for dx, dy in directions:
            nx, ny = i, j
            while True:
                nx += dx
                ny += dy
                if 0 <= nx < 8 and 0 <= ny < 8:
                    piece = board.get_piece_at(nx, ny)
                    if piece is None:
                        moves[nx][ny] = True
                    elif piece.color != self.color:
                        moves[nx][ny] = True
                        break
                    else:
                        break
                else:
                    break
        return moves


class Knight(Piece):
    def __str__(self):
        return f"{self.color[0]}n"

    def valid_moves(self, board):
        moves = [[False for _ in range(8)] for _ in range(8)]
        i, j = self.position
        directions = [
            (2, 1), (2, -1), (-2, 1), (-2, -1),
            (1, 2), (1, -2), (-1, 2), (-1, -2)
        ]
        for dx, dy in directions:
            nx, ny = i + dx, j + dy
            if 0 <= nx < 8 and 0 <= ny < 8:
                piece = board.get_piece_at(nx, ny)
                if piece is None or piece.color != self.color:
                    moves[nx][ny] = True
        return moves


class Rook(Piece):
    def __init__(self, color, position):
        super().__init__(color, position)
        self.has_moved = False

    def __str__(self):
        return f"{self.color[0]}r"

    def move(self, i, j):
        print(chess_notation(str(self), j, i))
        self.position = (i, j)
        self.has_moved = True

    def valid_moves(self, board):
        moves = [[False for _ in range(8)] for _ in range(8)]
        i, j = self.position
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        for dx, dy in directions:
            nx, ny = i, j
            while True:
                nx += dx
                ny += dy
                if 0 <= nx < 8 and 0 <= ny < 8:
                    piece = board.get_piece_at(nx, ny)
                    if piece is None:
                        moves[nx][ny] = True
                    elif piece.color != self.color:
                        moves[nx][ny] = True
                        break
                    else:
                        break
                else:
                    break
        return moves
