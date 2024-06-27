import copy

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

class FIXME(Exception):
    pass

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
        if isinstance(dest, str):
            sq = self.in_square.board.GetSquare(dest)
        elif isinstance(dest, Square):
            sq = dest
        else: raise TypeError()
        if sq.occ_by is not None: sq.RemovePiece(True)
        self.in_square.RemovePiece()
        sq.AddPiece(self)
        self.has_moved = True
        sq.board.turn = black if self.color == white else white
    def CanMove(self, dest):
        return False
    def IsLegal(self, dest):
        if not self.CanMove(dest): return False
        b = copy.deepcopy(self.in_square.board)
        b.GetPiece(b.GetStr(self)).Move(dest)
        if b.IsCheck(self.color):
            return False
        return True

class Square:
    def __init__(self, name=None):
        self.occ_by = None
        self.board = None
        self.name = name
    def __str__(self):
        return self.name
    def AddPiece(self, occ_piece, list_upd=False):
        self.occ_by = occ_piece
        occ_piece.in_square = self
        if list_upd:
            self.board.pieces += [occ_piece]
    def RemovePiece(self, list_upd=False):
        if self.occ_by is not None:
            self.occ_by.in_square = None
            if list_upd: self.board.pieces.remove(self.occ_by)
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

class Board: 
    def __init__(self, setup=None):
        self.board = []
        self.pieces = []
        self.turn = white
        self.moves = []
        for i in range(8):
            self.board += [[]]
            for k in range(8):
                self.board[i] += [Square(chr(97+i) + str(k+1))]
                self.board[i][k].board = self
        if setup == 'std':
            for i in range(8):
                self.board[i][1].AddPiece(Pawn(white), True)
                self.board[i][6].AddPiece(Pawn(black), True)
            for i in [0, 7]:
                self.board[i][0].AddPiece(Rook(white), True)
                self.board[i][7].AddPiece(Rook(black), True)
            for i in [1, 6]:
                self.board[i][0].AddPiece(Knight(white), True)
                self.board[i][7].AddPiece(Knight(black), True)
            for i in [2, 5]:
                self.board[i][0].AddPiece(Bishop(white), True)
                self.board[i][7].AddPiece(Bishop(black), True)
            self.board[3][0].AddPiece(Queen(white), True)
            self.board[3][7].AddPiece(Queen(black), True)
            self.board[4][0].AddPiece(King(white), True)
            self.board[4][7].AddPiece(King(black), True)
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
    def Show(self):
        if self.turn == white:
            print(self)
        else:
            pic = ''
            for k in range(8):
                for i in range(7, -1, -1):
                    piece = self.board[i][k].occ_by
                    if piece is not None:
                        p_name = ctos(piece.color) + '_' + piece.name
                        pic += globals()[p_name] + ' '
                    elif (i + k) % 2 == 1:
                        pic += '\u2610 '
                    else:
                        pic += '  '
                pic += '\n'
            print(pic)
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
        for piece in self.pieces:
            if piece is None or piece.color == color: continue
            if piece.CanMove(king_loc):
                return True
        return False
    def Nomen(self, cmd):
        if len(cmd) == 2:
            return self.PawnAdvance(cmd)
        if cmd[0] in ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']:
            return self.PawnCapture(cmd)
        if cmd[0] == 'Q':
            return self.QueenMove(cmd)
        if cmd[0] == 'N':
            return self.KnightMove(cmd)
        if cmd[0] == 'K':
            return self.KingMove(cmd)
        return False
        # move
    def PawnAdvance(self, cmd):
        try:
            dest = cmd
            prev = -1 if self.turn == white else 1
            prev_piece = self.GetSquare(dest).Offset(k=prev).occ_by
            if prev_piece is not None and prev_piece.name == 'pawn' and prev_piece.color == self.turn:
                if prev_piece.IsLegal(dest):
                    prev_piece.Move(dest)
                    self.moves += [cmd]
                    return True
            elif prev_piece is None:
                prev_piece = self.GetSquare(dest).Offset(k=prev*2).occ_by
                if prev_piece is not None and prev_piece.name == 'pawn' and prev_piece.color == self.turn and not prev_piece.has_moved:
                    if prev_piece.IsLegal(dest):
                        prev_piece.Move(dest)
                        self.moves += [cmd]
                        prev_piece.double = len(self.moves)
                        return True
            return False
        except:
            return False
    def PawnCapture(self, cmd):
        if len(cmd) != 4 or cmd[1] != 'x':
            return False
        try:
            dest = cmd[-2:]
            print('branch pawn capture')
            prev = -1 if self.turn == white else 1
            if self.GetSquare(dest).occ_by is None:
                print('branch try passant')
                to_passant = self.GetSquare(dest).Offset(k=prev).occ_by
                if to_passant is None or to_passant.color == self.turn or not isinstance(to_passant, Pawn): return False
                print('to_passant found')
                if to_passant.double != len(self.moves): return False
                print('to_passant valid')
                captor = None
                for i_off in [-1, 1]:
                    print(f'checking {i_off}')
                    capt_sq = to_passant.in_square.Offset(i=i_off)
                    if capt_sq is None or capt_sq.occ_by is None: continue
                    print('capt_sq occupied')
                    if capt_sq.occ_by.color == self.turn and isinstance(capt_sq.occ_by, Pawn) and capt_sq.name[0] == cmd[0]:
                        captor = capt_sq.occ_by
                        break
                if captor is None:
                    return False
                print('captor found')
                if captor.IsLegal(dest):
                    captor.Move(dest)
                    to_passant.in_square.RemovePiece(True)
                    self.moves += [cmd]
                    return True
                return False
            to_capt = self.GetSquare(dest).occ_by
            print('branch not passant')
            if to_capt.color == self.turn: return False
            captor = None
            for i_off in [-1, 1]:
                print(f'checking {i_off}')
                capt_sq = to_capt.in_square.Offset(i=i_off, k=prev)
                if capt_sq is None or capt_sq.occ_by is None: continue
                print('capt_sq occupied')
                if capt_sq.occ_by.color == self.turn and isinstance(capt_sq.occ_by, Pawn) and capt_sq.name[0] == cmd[0]:
                    captor = capt_sq.occ_by
                    break
            if captor is None: return False
            print('captor found')
            if captor.IsLegal(dest):
                to_capt.in_square.RemovePiece(True)
                print('to_capt removed')
                captor.Move(dest)
                self.moves += [cmd]
                return True
            return False
        except:
            return False
    def QueenMove(self, cmd):
        try:
            dest = cmd[-2:]
            capt = True if cmd[1] == 'x' else False
            spec = cmd[2:-2] if capt == 'x' else cmd[1:-2]
            #if spec != '': raise FIXME('FIXME: specification')
            if capt and self.GetSquare(dest).occ_by is None: return False
            if not capt and self.GetSquare(dest).occ_by is not None: return False
            queen = None
            for piece in self.pieces:
                if piece.color == self.turn and isinstance(piece, Queen):
                    if spec == '':
                        if queen is None:
                            queen = piece
                        else:
                            raise FIXME('FIXME: multiple queens found')
                    elif len(spec) == 1:
                        if str(piece.in_square.Get_k() + 1) == spec or piece.in_square.Get_i() + 97 == ord(spec):
                            if queen is None:
                                queen = piece
                            else:
                                raise FIXME('FIXME: multiple queens found')
                    elif len(spec) == 2:
                        if self.GetSquare(dest) == piece.in_square:
                            if queen is None:
                                queen = piece
                            else:
                                raise FIXME('FIXME: multiple queens found')
                    else: return False
            if queen is None: return False
            if queen.IsLegal(dest):
                if capt: self.GetSquare(dest).RemovePiece(True)
                queen.Move(dest)
                self.moves += [cmd]
                return True
            return False
        except FIXME as f:
            print(f)
            return False
        except:
            return False
    def KnightMove(self, cmd):
        try:
            dest = cmd[-2:]
            dest_sq = self.GetSquare(dest)
            capt = True if cmd[1] == 'x' else False
            spec = cmd[2:-2] if capt else cmd[1:-2]
            if capt and dest_sq.occ_by is None: return False
            if not capt and self.GetSquare(dest).occ_by is not None: return False
            knight_list = []
            for sq in dest_sq.Offset(i=[-1, 1], k=[-2, 2]) + dest_sq.Offset(i=[-2, 2], k=[-1, 1]):
                if sq is not None and sq.occ_by is not None and sq.occ_by.color == self.turn and isinstance(sq.occ_by, Knight):
                    if spec == '': knight_list += [sq.occ_by]
                    elif len(spec) == 1:
                        try:
                            if str(sq.Get_k() + 1) == spec or sq.Get_i() + 97 == ord(spec):
                                knight_list += [sq.occ_by]
                        except TypeError:
                            continue
                    elif len(spec) == 2:
                        if self.GetSquare(spec) == sq.occ_by:
                            knight_list += sq.occ_by
            if len(knight_list) != 1: return False
            knight = knight_list[0]
            if knight.IsLegal(dest):
                if capt: self.GetSquare(dest).RemovePiece(True)
                knight.Move(dest)
                self.moves += [cmd]
                return True
            return False
        except:
            return False
    def KingMove(self, cmd):
        try:
            dest = cmd[-2:]
            dest_sq = self.GetSquare(dest)
            capt = True if cmd[1] == 'x' else False
            spec = cmd[2:-2] if capt else cmd[1:-2]
            if capt and dest_sq.occ_by is None: return False
            if not capt and self.GetSquare(dest).occ_by is not None: return False
            king = self.GetPiece(self.GetKingLoc(self.turn))
            if king.IsLegal(dest):
                if capt: dest_sq.RemovePiece(True)
                self.moves += [cmd]
                king.Move(dest)
                return True
            return False
        except:
            return False
    def Castle(self, cmd):
        try:
            if cmd == 'O-O': kingside = True
            elif cmd == 'O-O-O': kingside = False
            else: return False
            king = self.GetPiece(self.GetKingLoc(self.turn))
            if king.has_moved: return False
            i_off = 3 if kingside else -4
            rook_sq = king.in_square.Offset(i=i_off)
            if rook_sq is None: return False
            rook = rook_sq.occ_by
            if not isinstance(rook, Rook) or rook.color != self.turn or rook.has_moved: return False
            check_range = range(1, 3) if kingside else range(-3, 0)
            for sq in king.in_square.Offset(i=check_range):
                if sq.occ_by is not None: return False
            king_off = 2 if kingside else -2
            rook_off = -2 if kingside else 3
            king.Move(king.Offset(i=king_off))
            rook.Move(rook.Offset(i=rook_off))
            self.moves += [cmd]
            return True
        except:
            return False

class Pawn(Piece):
    def __init__(self, color=white):
        super().__init__(color)
        self.name = 'pawn'
        self.double = None
    def CanMove(self, dest):
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
            if dest_sq in this_sq.Offset(i=[-1, 1], k=inc): # FIXME need more specific passant validity checking
                return True
            return False
        except:
            return False

class Rook(Piece):
    def __init__(self, color=white):
        super().__init__(color)
        self.name = 'rook'
    def CanMove(self, dest):
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
    def CanMove(self, dest):
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
    def CanMove(self, dest):
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
                    new_square = this_sq.board.board[i_][k_]
                    legal_list += [new_square]
                    if new_square.occ_by is not None: break
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
    def CanMove(self, dest):
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
                    new_square = this_sq.board.board[i_][k_]
                    diag_list += [new_square]
                    if new_square.occ_by is not None: break
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
    def CanMove(self, dest):
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
        b.Show()
        cmd = input('move:')
        if not b.Nomen(cmd):
            print('Returned False')

#b = Board('std')
#print(b.GetStr(b.board[1][0].occ_by))
Game()