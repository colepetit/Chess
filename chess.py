white = 0
black = 1

black_king = '\u2654'
black_queen = '\u2655'
black_rook = '\u2656'
black_bishop = '\u2657'
black_knight = '\u2658'
black_pawn = '\u2659'
white_king = '\u265A'
white_queen = '\u265B'
white_rook = '\u265C'
white_bishop = '\u265D'
white_knight = '\u265E'
white_pawn = '\u265F'

def ctos(col_num):
    if col_num == 0: return 'white'
    elif col_num == 1: return 'black'
    else: return '<color error>'

class Piece:
    def __init__(self, color=white):
        self.name = None
        self.in_square = None
        self.color = color
        self.has_moved = False
    def __str__(self):
        s_name = self.name if self.name is not None else '<no type>'
        s_color = ctos(self.color) if self.color is not None else '<no color>'
        return s_color + ' ' + s_name
    def Move(self, dest):
        sq = self.in_square.board.GetSquare(dest)
        self.in_square.RemovePiece()
        sq.AddPiece(self)
        self.has_moved = True
    def IsLegal(self, dest):
        return True

class Square:
    def __init__(self, name=None):
        self.occ_by = None
        self.board = None
        self.name = name
    def __str__(self):
        return self.name
    def AddPiece(self, occ_piece):
        self.occ_by = occ_piece
        occ_piece.in_square = self
    def RemovePiece(self):
        if self.occ_by is not None:
            self.occ_by.in_square = None
            self.occ_by = None
    def Get_i(self):
        for i in range(8):
            if self in self.board.board[i]: return i
        return -1
    def Get_k(self):
        i = self.Get_i()
        for k in range(8):
            if self == self.board.board[i][k]: return k
        return -1
    def Offset(self, i=0, k=0, pairs=None):
        try:
            if pairs is not None:
                off_list = []
                for pair in pairs:
                    off_list += [self.Offset(i=pair[0], k=pair[1])]
                return off_list
            if type(i) is int and type(k) is int:
                new_i = i + self.Get_i()
                new_k = k + self.Get_k()
                if new_i in range(8) and new_k in range(8):
                    return self.board.board[i + self.Get_i()][k + self.Get_k()]
                return None
            else:
                off_list = []
                if type(i) is not int:
                    for i_ in i:
                        if type(k) is not int:
                            for k_ in k:
                                off_list += [self.Offset(i_, k_)]
                        else:
                            off_list += [self.Offset(i_, k)]
                else:
                    for k_ in k:
                        off_list += [self.Offset(i, k_)]
                return off_list
        except:
            return None

class Board: #TODO: add piece list * rework IsCheck func
    def __init__(self, setup=None):
        self.board = []
        for i in range(8):
            self.board += [[]]
            for k in range(8):
                self.board[i] += [Square(chr(97+i) + str(k+1))]
                self.board[i][k].board = self
        if setup == 'std':
            for i in range(8):
                self.board[i][1].AddPiece(Pawn(white))
                self.board[i][6].AddPiece(Pawn(black))
            for i in [0, 7]:
                self.board[i][0].AddPiece(Rook(white))
                self.board[i][7].AddPiece(Rook(black))
            for i in [1, 6]:
                self.board[i][0].AddPiece(Knight(white))
                self.board[i][7].AddPiece(Knight(black))
            for i in [2, 5]:
                self.board[i][0].AddPiece(Bishop(white))
                self.board[i][7].AddPiece(Bishop(black))
            self.board[3][0].AddPiece(Queen(white))
            self.board[3][7].AddPiece(Queen(black))
            self.board[4][0].AddPiece(King(white))
            self.board[4][7].AddPiece(King(black))
    def __str__(self):
        pic = ''
        for k in range(7, -1, -1):
            for i in range(8):
                piece = self.board[i][k].occ_by
                if piece is not None:
                    p_name = ctos(piece.color) + '_' + piece.name
                    pic += globals()[p_name] + ' '
                elif (i + k) % 2 == 1:
                    pic += '\u2610 '
                else:
                    pic += '  '
            pic += '\n'
        return pic
    def GetSquare(self, square):
        i = ord(square[0]) - 97
        k = int(square[1]) - 1
        return self.board[i][k]
    def GetStr(self, ref):
        if isinstance(ref, Piece):
            ref = ref.in_square
        if not isinstance(ref, Square):
            return "none"
        return chr(97+ref.Get_i()) + str(ref.Get_k()+1)
    def GetPiece(self, square):
        return self.GetSquare(square).occ_by
    def MovePiece(self, piece, dest):
        piece.Move(dest)
    def GetKingLoc(self, color):
        for i in range(8):
            for k in range(8):
                piece = self.board[i][k].occ_by
                if piece is not None and piece.color == color and piece.name == 'king':
                    return chr(97+i) + str(k+1)
        return 'none'
    def IsCheck(self, color):
        king_loc = self.GetKingLoc(color)
        for i in range(8):
            for k in range(8):
                piece = self.board[i][k].occ_by
                if piece is None or piece.color == color: continue
                if piece.IsLegal(king_loc):
                    print('Check found by piece in ' + self.GetStr(piece))
                    return True
        return False

class Pawn(Piece):
    def __init__(self, color=white):
        super().__init__(color)
        self.name = 'pawn'
    def IsLegal(self, dest):
        try:
            this_sq = self.in_square
            dest_sq = this_sq.board.GetSquare(dest)
            inc = 1 if self.color == white else -1
            if dest_sq.occ_by is not None:
                if dest_sq.occ_by.color == self.color:
                    return False
                if dest_sq in this_sq.Offset(i=[-1, 1], k=inc):
                    return True
                return False
            if dest_sq == this_sq.Offset(k=inc):
                return True
            if dest_sq == this_sq.Offset(k=inc*2) and this_sq.Offset(k=inc).occ_by == None and not this_sq.occ_by.has_moved:
                return True
            return False
        except:
            return False

class Rook(Piece):
    def __init__(self, color=white):
        super().__init__(color)
        self.name = 'rook'
    def IsLegal(self, dest):
        try:
            this_sq = self.in_square
            dest_sq = this_sq.board.GetSquare(dest)
            if dest_sq.occ_by is not None and dest_sq.occ_by.color == self.color:
                return False
            this_i = this_sq.Get_i()
            this_k = this_sq.Get_k()
            if dest_sq in this_sq.Offset(i=0, k=range(0 - this_k, 8 - this_k)):
                k_off = dest_sq.Get_k() - this_k
                step = 1 if k_off > 0 else -1
                for sq in this_sq.Offset(i=0, k=range(step, k_off, step)):
                    if sq.occ_by is not None:
                        return False
                return True
            elif dest_sq in this_sq.Offset(i=range(0 - this_i, 8 - this_i), k=0):
                i_off = dest_sq.Get_i() - this_i
                step = 1 if i_off > 0 else -1
                for sq in this_sq.Offset(i=range(step, i_off, step), k=0):
                    if sq.occ_by is not None:
                        return False
                return True            
            return False
        except:
            return False

class Knight(Piece):
    def __init__(self, color=white):
        super().__init__(color)
        self.name = 'knight'
    def IsLegal(self, dest):
        try:
            this_sq = self.in_square
            dest_sq = this_sq.board.GetSquare(dest)
            if dest_sq.occ_by is not None and dest_sq.occ_by.color == self.color:
                return False
            if dest_sq in this_sq.Offset(i=[-2, 2], k=[-1, 1]) + this_sq.Offset(i=[-1, 1], k=[-2, 2]):
                return True
            return False
        except:
            return False

class Bishop(Piece):
    def __init__(self, color=white):
        super().__init__(color)
        self.name = 'bishop'
    def IsLegal(self, dest):
        try:
            this_sq = self.in_square
            dest_sq = this_sq.board.GetSquare(dest)
            if dest_sq.occ_by is not None and dest_sq.occ_by.color == self.color:
                return False
            this_i = this_sq.Get_i()
            this_k = this_sq.Get_k()
            legal_list = []
            for inc in [[-1, -1], [-1, 1], [1, -1], [1, 1]]:
                i_ = this_i + inc[0]
                k_ = this_k + inc[1]
                while i_ in range(8) and k_ in range(8):
                    legal_list += [this_sq.board.board[i_][k_]]
                    i_ += inc[0]
                    k_ += inc[1]
            if dest_sq in legal_list:
                return True        
            return False
        except:
            return False

class Queen(Piece):
    def __init__(self, color=white):
        super().__init__(color)
        self.name = 'queen'
    def IsLegal(self, dest):
        try:
            this_sq = self.in_square
            dest_sq = this_sq.board.GetSquare(dest)
            if dest_sq.occ_by is not None and dest_sq.occ_by.color == self.color:
                return False
            this_i = this_sq.Get_i()
            this_k = this_sq.Get_k()
            if dest_sq in this_sq.Offset(i=0, k=range(0 - this_k, 8 - this_k)):
                k_off = dest_sq.Get_k() - this_k
                step = 1 if k_off > 0 else -1
                for sq in this_sq.Offset(i=0, k=range(step, k_off, step)):
                    if sq.occ_by is not None:
                        return False
                return True
            elif dest_sq in this_sq.Offset(i=range(0 - this_i, 8 - this_i), k=0):
                i_off = dest_sq.Get_i() - this_i
                step = 1 if i_off > 0 else -1
                for sq in this_sq.Offset(i=range(step, i_off, step), k=0):
                    if sq.occ_by is not None:
                        return False
                return True
            diag_list = []
            for inc in [[-1, -1], [-1, 1], [1, -1], [1, 1]]:
                i_ = this_i + inc[0]
                k_ = this_k + inc[1]
                while i_ in range(8) and k_ in range(8):
                    diag_list += [this_sq.board.board[i_][k_]]
                    i_ += inc[0]
                    k_ += inc[1]
            if dest_sq in diag_list:
                return True   
            return False
        except:
            return False

class King(Piece):
    def __init__(self, color=white):
        super().__init__(color)
        self.name = 'king'
    def IsLegal(self, dest):
        try:
            this_sq = self.in_square
            dest_sq = this_sq.board.GetSquare(dest)
            if dest_sq.occ_by is not None and dest_sq.occ_by.color == self.color:
                return False
            if dest_sq in this_sq.Offset(i=[-1, 0, 1], k=[-1, 0, 1]):
                return True
            return False
        except:
            return False

def Game():
    b = Board('std')
    while 1:
        print('\n')
        print(b)
        cmd = input('move:')
        src, dest = cmd.split(' ')
        piece = b.GetPiece(src)
        if piece.IsLegal(dest):
            old_loc = b.GetStr(piece)
            b.MovePiece(piece, dest)
            if b.IsCheck(piece.color):
                print('Illegal move--into check.\n')
                b.MovePiece(piece, old_loc)
        else:
            print('Illegal move.\n')

#b = Board('std')
#print(b.GetStr(b.board[1][0].occ_by))
Game()