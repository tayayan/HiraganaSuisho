#Copyright (c) tayayan
#Released under the MIT license
#https://opensource.org/licenses/mit-license.php

class Board:
    def __init__(self, position = None):
        #0～10 空欄
        #11～99 盤面
        #100～106 先手持駒
        #107～113 後手持駒
        #114 手番(1:先手, -1:後手)
        #115 手数
        self.base = ["","","","","","","","","","","",
                     "l","n","s","g","k","g","s","n","l","/",
                     "0","r","0","0","0","0","0","b","0","/",
                     "p","p","p","p","p","p","p","p","p","/",
                     "0","0","0","0","0","0","0","0","0","/",
                     "0","0","0","0","0","0","0","0","0","/",
                     "0","0","0","0","0","0","0","0","0","/",
                     "P","P","P","P","P","P","P","P","P","/",
                     "0","B","0","0","0","0","0","R","0","/",
                     "L","N","S","G","K","G","S","N","L",
                      0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1]
        self.board = self.base.copy()
        #局面履歴
        self.hand = []
        self.history = [self.base[11:115]]
        if position is not None:
            self.set(position)
        
    def sfen(self):
        sfen0 = "".join(self.board[11:100])
        sfen0 = sfen0.replace('000000000','9')\
                     .replace('00000000','8')\
                     .replace('0000000','7')\
                     .replace('000000','6')\
                     .replace('00000','5')\
                     .replace('0000','4')\
                     .replace('000','3')\
                     .replace('00','2')\
                     .replace('0','1')        
        sfen1 = self.board[114]
        if sfen1 == 1:
            sfen1 = "b"
        elif sfen1 == -1:
            sfen1 = "w"
        piece = [self.board[100],"R",
                 self.board[101],"B",
                 self.board[102],"G",
                 self.board[103],"S",
                 self.board[104],"N",
                 self.board[105],"L",
                 self.board[106],"P",
                 self.board[107],"r",
                 self.board[108],"b",
                 self.board[109],"g",
                 self.board[110],"s",
                 self.board[111],"n",
                 self.board[112],"l",
                 self.board[113],"p"]
        sfen2 = ""
        while piece != []:
            if piece[0] == 0:
                del piece[:2]
            elif piece[0] == 1:
                del piece[0]
            else:
                sfen2 += str(piece.pop(0))
        if sfen2 == "":
            sfen2 = "-"
        sfen3 = str(self.board[115])
        return "sfen " + sfen0 + " " + sfen1 + " " + sfen2 + " " + sfen3

    def position(self):
        b = Board()
        b.board[11:115] = self.history[0]
        sfen = b.sfen()
        if sfen == "sfen lnsgkgsnl/1r5b1/ppppppppp/9/9/9/PPPPPPPPP/1B5R1/LNSGKGSNL b - 1":
            sfen = "startpos"
        position = "position " + sfen + " moves " + " ".join(self.hand)
        return position
    
    def turn(self):
        return self.board[114]

    def ply(self):
        return self.board[115]
    
    def is_sennichite(self):
        return self.board[11:115] in self.history[:-1]
        
    def set(self, position):
        position = position.split()
        self.board = self.base.copy()
        if "sfen" in position:
            sfen0 = position[position.index("sfen")+1]
            sfen0 = sfen0.replace('9', '000000000')\
                         .replace('8', '00000000')\
                         .replace('7', '0000000')\
                         .replace('6', '000000')\
                         .replace('5', '00000')\
                         .replace('4', '0000')\
                         .replace('3', '000')\
                         .replace('2', '00')\
                         .replace('1', '0')
            n = 11
            while n != 100:
                if sfen0[0] == "+":
                    self.board[n] = sfen0[:2]
                    sfen0 = sfen0[2:]
                else:
                    self.board[n] = sfen0[0]
                    sfen0 = sfen0[1:]
                n += 1
                
            sfen1 = position[position.index("sfen")+2]
            if sfen1 == "b":
                self.board[114] = 1
            elif sfen1 == "w":
                self.board[114] = -1

            sfen2 = position[position.index("sfen")+3]
            if sfen2 != "-":
                p = ""
                while sfen2 != "":
                    if sfen2[0].isdigit():
                        p += sfen2[0]
                        sfen2 = sfen2[1:]
                        continue
                    if p == "":
                        p = 1
                    else:
                        p = int(p)
                    if sfen2[0] == "R":
                        self.board[100] = p
                    elif sfen2[0] == "B":
                        self.board[101] = p
                    elif sfen2[0] == "G":
                        self.board[102] = p
                    elif sfen2[0] == "S":
                        self.board[103] = p
                    elif sfen2[0] == "N":
                        self.board[104] = p
                    elif sfen2[0] == "L":
                        self.board[105] = p
                    elif sfen2[0] == "P":
                        self.board[106] = p
                    elif sfen2[0] == "r":
                        self.board[107] = p
                    elif sfen2[0] == "b":
                        self.board[108] = p
                    elif sfen2[0] == "g":
                        self.board[109] = p
                    elif sfen2[0] == "s":
                        self.board[110] = p
                    elif sfen2[0] == "n":
                        self.board[111] = p
                    elif sfen2[0] == "l":
                        self.board[112] = p
                    elif sfen2[0] == "p":
                        self.board[113] = p
                    sfen2 = sfen2[1:]
                    p = ""
            self.board[115] = int(position[position.index("sfen")+4])
        self.hand = []
        self.history = [self.board[11:115]]
        if "moves" in position:
            moves = position[position.index("moves")+1:]
            for move in moves:
                self.push(move)
            
    def board_num(self, sfen_num):
        num = sfen_num.translate(str.maketrans({'a':'1','b':'2','c':'3','d':'4','e':'5','f':'6','g':'7','h':'8','i':'9'}))
        num = int(num[1] + str(10 - int(num[0])))
        return num
    
    def sfen_num(self, board_num):
        num = str(10 - int(str(board_num)[1])) + str(board_num)[0].translate(str.maketrans({'1':'a','2':'b','3':'c','4':'d','5':'e','6':'f','7':'g','8':'h','9':'i'}))
        return num

    def piece_location(self, piece):
        l = [i for i, x in enumerate(self.board) if x == piece]
        return l
    
    def push(self, move):
        if move[1] != "*":
            move_from = self.board_num(move[:2])
            move_to = self.board_num(move[2:4])
            if self.board[move_to] != "0":
                if self.board[move_to][-1] == "r":
                    self.board[100] += 1
                elif self.board[move_to][-1] == "b":
                    self.board[101] += 1
                elif self.board[move_to][-1] == "g":
                    self.board[102] += 1
                elif self.board[move_to][-1] == "s":
                    self.board[103] += 1
                elif self.board[move_to][-1] == "n":
                    self.board[104] += 1
                elif self.board[move_to][-1] == "l":
                    self.board[105] += 1
                elif self.board[move_to][-1] == "p":
                    self.board[106] += 1
                elif self.board[move_to][-1] == "R":
                    self.board[107] += 1
                elif self.board[move_to][-1] == "B":
                    self.board[108] += 1
                elif self.board[move_to][-1] == "G":
                    self.board[109] += 1
                elif self.board[move_to][-1] == "S":
                    self.board[110] += 1
                elif self.board[move_to][-1] == "N":
                    self.board[111] += 1
                elif self.board[move_to][-1] == "L":
                    self.board[112] += 1
                elif self.board[move_to][-1] == "P":
                    self.board[113] += 1
            if move[-1] == "+":
                self.board[move_to] = "+" + self.board[move_from]
            else:
                self.board[move_to] = self.board[move_from]
            self.board[move_from] = "0"
        else:
            move_to = self.board_num(move[2:4])
            if self.turn() == 1:
                if move[0] == "R":
                    self.board[100] -= 1
                elif move[0] == "B":
                    self.board[101] -= 1
                elif move[0] == "G":
                    self.board[102] -= 1
                elif move[0] == "S":
                    self.board[103] -= 1
                elif move[0] == "N":
                    self.board[104] -= 1
                elif move[0] == "L":
                    self.board[105] -= 1
                elif move[0] == "P":
                    self.board[106] -= 1
                self.board[move_to] = move[0]
            elif self.turn() == -1:
                if move[0] == "R":
                    self.board[107] -= 1
                elif move[0] == "B":
                    self.board[108] -= 1
                elif move[0] == "G":
                    self.board[109] -= 1
                elif move[0] == "S":
                    self.board[110] -= 1
                elif move[0] == "N":
                    self.board[111] -= 1
                elif move[0] == "L":
                    self.board[112] -= 1
                elif move[0] == "P":
                    self.board[113] -= 1
                self.board[move_to] = move[0].lower()
        self.hand.append(move)
        self.board[114] *= -1
        self.board[115] += 1
        self.history.append(self.board[11:115])
        
    def pop(self):
        if len(self.history) == 1:
            return
        else:
            del self.history[-1]
            self.board[11:115] = self.history[-1]
            del self.hand[-1]
            self.board[115] -= 1
            
    #合法手生成関係
    def direction_N(self, board_num):
        s = set()
        if board_num > 20:
            s.add(board_num - 10)
        return s
    def direction_S(self, board_num):
        s = set()
        if board_num < 90:
            s.add(board_num + 10)
        return s
    def direction_EW(self, board_num):
        s = set()
        if board_num % 10 != 1:
            s.add(board_num - 1)
        if board_num % 10 != 9:
            s.add(board_num + 1) 
        return s
    def direction_NEW(self, board_num):
        s = set()
        if board_num > 20 and board_num % 10 != 1:
            s.add(board_num - 11)
        if board_num > 20 and board_num % 10 != 9:
            s.add(board_num - 9)
        return s
    def direction_SEW(self, board_num):
        s = set()
        if board_num < 90 and board_num % 10 != 1:
            s.add(board_num + 9)
        if board_num < 90 and board_num % 10 != 9:
            s.add(board_num + 11)
        return s
    def direction_KN(self, board_num):
        s = set()
        if board_num > 30 and board_num % 10 != 1:
            s.add(board_num - 21)
        if board_num > 30 and board_num % 10 != 9:
            s.add(board_num - 19)
        return s
    def direction_KS(self, board_num):
        s = set()
        if board_num < 80 and board_num % 10 != 1:
            s.add(board_num + 19)
        if board_num < 80 and board_num % 10 != 9:
            s.add(board_num + 21)
        return s
    def direction_PN(self, board_num):
        s = set()
        while board_num > 20:
            board_num -= 10
            s.add(board_num)
            if self.board[board_num] != "0":
                break
        return s
    def direction_PS(self, board_num):
        s = set()
        while board_num < 90:
            board_num += 10
            s.add(board_num)
            if self.board[board_num] != "0":
                break
        return s
    def direction_PEW(self, board_num):
        s = set()
        a = board_num
        while a % 10 != 1:
            a -= 1
            s.add(a)
            if self.board[a] != "0":
                break
        a = board_num
        while a % 10 != 9:
            a += 1
            s.add(a)
            if self.board[a] != "0":
                break
        return s
    def direction_PB(self, board_num):
        s = set()
        a = board_num
        while a > 20 and a % 10 != 1:
            a -= 11
            s.add(a)
            if self.board[a] != "0":
                break
        a = board_num
        while a > 20 and a % 10 != 9:
            a -= 9
            s.add(a)
            if self.board[a] != "0":
                break
        a = board_num
        while a < 90 and a % 10 != 1:
            a += 9
            s.add(a)
            if self.board[a] != "0":
                break
        a = board_num
        while a < 90 and a % 10 != 9:
            a += 11
            s.add(a)
            if self.board[a] != "0":
                break
        return s
    
    def black_move(self):
        n = 11
        s = set()
        while n != 100:
            p = self.board[n]
            if p == "0":
                pass
            elif p == "P":
                for i in self.direction_N(n):
                    if i > 20:
                        s.add(str(n) + str(i))
                    if i < 40:
                        s.add(str(n) + str(i) + "+")
            elif p == "L":
                for i in self.direction_PN(n):
                    if i > 20:
                        s.add(str(n) + str(i))
                    if i < 40:
                        s.add(str(n) + str(i) + "+")
            elif p == "N":
                for i in self.direction_KN(n):
                    if i > 30:
                        s.add(str(n) + str(i))
                    if i < 40:
                        s.add(str(n) + str(i) + "+")
            elif p == "S":
                for i in self.direction_N(n) | self.direction_NEW(n) | self.direction_SEW(n):
                    s.add(str(n) + str(i))
                    if i < 40 or n < 40:
                        s.add(str(n) + str(i) + "+")
            elif p == "G" or p == "+P" or p == "+L" or p == "+N" or p =="+S":
                for i in self.direction_N(n) | self.direction_S(n) | self.direction_EW(n) | self.direction_NEW(n):
                    s.add(str(n) + str(i))
            elif p == "K":
                for i in self.direction_N(n) | self.direction_S(n) | self.direction_EW(n) | self.direction_NEW(n) | self.direction_SEW(n):
                    s.add(str(n) + str(i))
            elif p == "B":
                for i in self.direction_PB(n):
                    s.add(str(n) + str(i))
                    if i < 40 or n < 40:
                        s.add(str(n) + str(i) + "+")
            elif p == "+B":
                for i in self.direction_PB(n) | self.direction_N(n) | self.direction_S(n) | self.direction_EW(n):
                    s.add(str(n) + str(i))
            elif p == "R":
                for i in self.direction_PN(n) | self.direction_PS(n) | self.direction_PEW(n):
                    s.add(str(n) + str(i))
                    if i < 40 or n < 40:
                        s.add(str(n) + str(i) + "+")
            elif p == "+R":
                for i in self.direction_PN(n) | self.direction_PS(n) | self.direction_PEW(n) | self.direction_NEW(n) | self.direction_SEW(n):
                    s.add(str(n) + str(i))
            n += 1
        return s

    def white_move(self):
        n = 11
        s = set()
        while n != 100:
            p = self.board[n]
            if p == "0":
                pass
            elif p == "p":
                for i in self.direction_S(n):
                    if i < 90:
                        s.add(str(n) + str(i))
                    if i > 70:
                        s.add(str(n) + str(i) + "+")
            elif p == "l":
                for i in self.direction_PS(n):
                    if i < 90:
                        s.add(str(n) + str(i))
                    if i > 70:
                        s.add(str(n) + str(i) + "+")
            elif p == "n":
                for i in self.direction_KS(n):
                    if i < 80:
                        s.add(str(n) + str(i))
                    if i > 70:
                        s.add(str(n) + str(i) + "+")
            elif p == "s":
                for i in self.direction_S(n) | self.direction_NEW(n) | self.direction_SEW(n):
                    s.add(str(n) + str(i))
                    if i > 70 or n > 70:
                        s.add(str(n) + str(i) + "+")
            elif p == "g" or p == "+p" or p == "+l" or p == "+n" or p =="+s":
                for i in self.direction_N(n) | self.direction_S(n) | self.direction_EW(n) | self.direction_SEW(n):
                    s.add(str(n) + str(i))
            elif p == "k":
                for i in self.direction_N(n) | self.direction_S(n) | self.direction_EW(n) | self.direction_NEW(n) | self.direction_SEW(n):
                    s.add(str(n) + str(i))
            elif p == "b":
                for i in self.direction_PB(n):
                    s.add(str(n) + str(i))
                    if i > 70 or n > 70:
                        s.add(str(n) + str(i) + "+")
            elif p == "+b":
                for i in self.direction_PB(n) | self.direction_N(n) | self.direction_S(n) | self.direction_EW(n):
                    s.add(str(n) + str(i))
            elif p == "r":
                for i in self.direction_PN(n) | self.direction_PS(n) | self.direction_PEW(n):
                    s.add(str(n) + str(i))
                    if i > 70 or n > 70:
                        s.add(str(n) + str(i) + "+")
            elif p == "+r":
                for i in self.direction_PN(n) | self.direction_PS(n) | self.direction_PEW(n) | self.direction_NEW(n) | self.direction_SEW(n):
                    s.add(str(n) + str(i))
            n += 1
        return s

    def is_check_bking(self):
        if not "K" in self.board:
            return False
        n = self.board.index("K")
        for i in self.direction_N(n):
            a = self.board[i]
            if (a[0] == "+" and a[1].islower()) or a == "p" or a == "l" or a == "s" or a == "g" or a == "r" or a == "k":
                return True
        for i in self.direction_NEW(n):
            a = self.board[i]
            if (a[0] == "+" and a[1].islower()) or a == "s" or a == "g" or a == "b" or a == "k":
                return True
        for i in self.direction_S(n) | self.direction_EW(n):
            a = self.board[i]
            if (a[0] == "+" and a[1].islower()) or a == "g" or a == "r" or a == "k":
                return True
        for i in self.direction_SEW(n):
            a = self.board[i]
            if a == "s" or a == "b" or a == "+b" or a == "+r" or a == "k":
                return True
        for i in self.direction_KN(n):
            a = self.board[i]
            if a == "n":
                return True
        for i in self.direction_PN(n):
            a = self.board[i]
            if a == "l" or a == "r" or a == "+r":
                return True
        for i in self.direction_PS(n) | self.direction_PEW(n):
            a = self.board[i]
            if a == "r" or a == "+r":
                return True
        for i in self.direction_PB(n):
            a = self.board[i]
            if a == "b" or a == "+b":
                return True
        return False

    def is_check_wking(self):
        if not "k" in self.board:
            return False
        n = self.board.index("k")
        for i in self.direction_S(n):
            a = self.board[i]
            if (a[0] == "+" and a[1].isupper()) or a == "P" or a == "L" or a == "S" or a == "G" or a == "R" or a == "K":
                return True
        for i in self.direction_SEW(n):
            a = self.board[i]
            if (a[0] == "+" and a[1].isupper()) or a == "S" or a == "G" or a == "B" or a == "K":
                return True
        for i in self.direction_N(n) | self.direction_EW(n):
            a = self.board[i]
            if (a[0] == "+" and a[1].isupper()) or a == "G" or a == "R" or a == "K":
                return True
        for i in self.direction_NEW(n):
            a = self.board[i]
            if a == "S" or a == "B" or a == "+B" or a == "+R" or a == "K":
                return True
        for i in self.direction_KS(n):
            a = self.board[i]
            if a == "N":
                return True
        for i in self.direction_PS(n):
            a = self.board[i]
            if a == "L" or a == "R" or a == "+R":
                return True
        for i in self.direction_PN(n) | self.direction_PEW(n):
            a = self.board[i]
            if a[-1] == "R":
                return True
        for i in self.direction_PB(n):
            a = self.board[i]
            if a[-1] == "B":
                return True
        return False

            
    def legal_moves(self):
        s = set()
        if self.turn() == 1:
            for move in self.black_move():
                if not self.board[int(move[2:4])].isupper():
                    piece = self.board[int(move[2:4])]
                    self.board[int(move[2:4])] = self.board[int(move[:2])]
                    self.board[int(move[:2])] = "0"
                    if self.is_check_bking():
                        self.board[int(move[:2])] = self.board[int(move[2:4])]
                        self.board[int(move[2:4])] = piece
                        continue
                    self.board[int(move[:2])] = self.board[int(move[2:4])]
                    self.board[int(move[2:4])] = piece
                    s.add(self.sfen_num(int(move[:2])) + self.sfen_num(int(move[2:4])) + move[4:])
            p = set()
            for i in range(100):
                if self.board[i] == "0":
                    p.add(i)
            if self.board[100] != 0:
                for i in p:
                    self.board[i] = "Q"
                    if self.is_check_bking():
                        self.board[i] = "0"
                        continue
                    self.board[i] = "0"
                    s.add("R*"+self.sfen_num(i))
            if self.board[101] != 0:
                for i in p:
                    self.board[i] = "Q"
                    if self.is_check_bking():
                        self.board[i] = "0"
                        continue
                    self.board[i] = "0"
                    s.add("B*"+self.sfen_num(i))
            if self.board[102] != 0:
                for i in p:
                    self.board[i] = "Q"
                    if self.is_check_bking():
                        self.board[i] = "0"
                        continue
                    self.board[i] = "0"
                    s.add("G*"+self.sfen_num(i))
            if self.board[103] != 0:
                for i in p:
                    self.board[i] = "Q"
                    if self.is_check_bking():
                        self.board[i] = "0"
                        continue
                    self.board[i] = "0"
                    s.add("S*"+self.sfen_num(i))
            if self.board[104] != 0:
                for i in p:
                    if i > 30:
                        self.board[i] = "Q"
                        if self.is_check_bking():
                            self.board[i] = "0"
                            continue
                        self.board[i] = "0"
                        s.add("N*"+self.sfen_num(i))
            if self.board[105] != 0:
                for i in p:
                    if i > 20:
                        self.board[i] = "Q"
                        if self.is_check_bking():
                            self.board[i] = "0"
                            continue
                        self.board[i] = "0"
                        s.add("L*"+self.sfen_num(i))
            if self.board[106] != 0:
                for i in range(100):
                    if self.board[i] == "P":
                        n = i % 10
                        for j in range(10):
                            n += 10
                            p.discard(n)
                #打ち歩詰め処理
                if "k" in self.board:
                    a = self.board.index("k") + 10
                    if a in p:
                        self.board[a] = "P"
                        self.board[114] *= -1
                        if self.legal_moves() == set():
                            p.discard(a)
                        self.board[a] = "0"
                        self.board[114] *= -1
                for i in p:
                    if i > 20:
                        self.board[i] = "Q"
                        if self.is_check_bking():
                            self.board[i] = "0"
                            continue
                        self.board[i] = "0"
                        s.add("P*"+self.sfen_num(i))
        elif self.turn() == -1:
            for move in self.white_move():
                if not self.board[int(move[2:4])].islower():
                    piece = self.board[int(move[2:4])]
                    self.board[int(move[2:4])] = self.board[int(move[:2])]
                    self.board[int(move[:2])] = "0"
                    if self.is_check_wking():
                        self.board[int(move[:2])] = self.board[int(move[2:4])]
                        self.board[int(move[2:4])] = piece
                        continue
                    self.board[int(move[:2])] = self.board[int(move[2:4])]
                    self.board[int(move[2:4])] = piece
                    s.add(self.sfen_num(int(move[:2])) + self.sfen_num(int(move[2:4])) + move[4:])
            p = set()
            for i in range(100):
                if self.board[i] == "0":
                    p.add(i)
            if self.board[107] != 0:
                for i in p:
                    self.board[i] = "q"
                    if self.is_check_wking():
                        self.board[i] = "0"
                        continue
                    self.board[i] = "0"
                    s.add("R*"+self.sfen_num(i))
            if self.board[108] != 0:
                for i in p:
                    self.board[i] = "q"
                    if self.is_check_wking():
                        self.board[i] = "0"
                        continue
                    self.board[i] = "0"
                    s.add("B*"+self.sfen_num(i))
            if self.board[109] != 0:
                for i in p:
                    self.board[i] = "q"
                    if self.is_check_wking():
                        self.board[i] = "0"
                        continue
                    self.board[i] = "0"
                    s.add("G*"+self.sfen_num(i))
            if self.board[110] != 0:
                for i in p:
                    self.board[i] = "q"
                    if self.is_check_wking():
                        self.board[i] = "0"
                        continue
                    self.board[i] = "0"
                    s.add("S*"+self.sfen_num(i))
            if self.board[111] != 0:
                for i in p:
                    if i < 80:
                        self.board[i] = "q"
                        if self.is_check_wking():
                            self.board[i] = "0"
                            continue
                        self.board[i] = "0"
                        s.add("N*"+self.sfen_num(i))
            if self.board[112] != 0:
                for i in p:
                    if i < 90:
                        self.board[i] = "q"
                        if self.is_check_wking():
                            self.board[i] = "0"
                            continue
                        self.board[i] = "0"
                        s.add("L*"+self.sfen_num(i))
            if self.board[113] != 0:
                for i in range(100):
                    if self.board[i] == "p":
                        n = i % 10
                        for j in range(10):
                            n += 10
                            p.discard(n)
                #打ち歩詰め処理
                if "K" in self.board:
                    a = self.board.index("K") - 10
                    if a in p:
                        self.board[a] = "p"
                        self.board[114] *= -1
                        if self.legal_moves() == set():
                            p.discard(a)
                        self.board[a] = "0"
                        self.board[114] *= -1
                for i in p:
                    if i < 90:
                        self.board[i] = "q"
                        if self.is_check_wking():
                            self.board[i] = "0"
                            continue
                        self.board[i] = "0"
                        s.add("P*"+self.sfen_num(i))
        return s

    #利きを数え上げる
    def piece_attack(self, turn = None):
        l = [0] * 100
        b = Board()
        b.board = self.board.copy()
        if turn is not None:
            b.board[114] = turn
        for i in b.legal_moves():
            if i[1] == "*" or len(i) == 5:
                continue
            else:
                l[self.board_num(i[2:4])] += 1
        return l
