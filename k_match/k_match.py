from Board import *

def piece_match(board, sfen):
    tacboard = Board(sfen)
    for i in range(11, 100):
        if tacboard.board[i] != "0" and tacboard.board[i] != "/" and board.board[i] == "0":
            return False
    return True

def no_piece_match(board, sfen):
    tacboard = Board(sfen)
    for i in range(11, 100):
        if tacboard.board[i] != "0" and tacboard.board[i] != "/" and board.board[i] != "0":
            return False
    return True
    
def k_match(board, board2):
    #「K」がマッチするか調べる。
    if piece_match(board, "sfen 9/9/9/9/9/P1G6/SG7/SG7/L1G6 b - 1") and no_piece_match(board, "sfen 9/9/9/9/9/1N7/2N6/2N6/1N7 b - 1"):
        print(board2.position())
        return True
    elif piece_match(board, "sfen 9/9/9/9/9/1P1G5/1SG6/1SG6/1L1G5 b - 1") and no_piece_match(board, "sfen 9/9/9/9/9/2N6/3N5/3N5/2N6 b - 1"):
        print(board2.position())
        return True
    elif piece_match(board, "sfen 9/9/9/9/9/2P1G4/2SG5/2SG5/2L1G4 b - 1") and no_piece_match(board, "sfen 9/9/9/9/9/3N5/4N4/4N4/3N5 b - 1"):
        print(board2.position())
        return True
    elif piece_match(board, "sfen 9/9/9/9/9/3P1G3/3SG4/3SG4/3L1G3 b - 1") and no_piece_match(board, "sfen 9/9/9/9/9/4N4/5N3/5N3/4N4 b - 1"):
        print(board2.position())
        return True
    elif piece_match(board, "sfen 9/9/9/9/9/4P1G2/4SG3/4SG3/4L1G2 b - 1") and no_piece_match(board, "sfen 9/9/9/9/9/5N3/6N2/6N2/5N3 b - 1"):
        print(board2.position())
        return True
    elif piece_match(board, "sfen 9/9/9/9/9/5P1G1/5SG2/5SG2/5L1G1 b - 1") and no_piece_match(board, "sfen 9/9/9/9/9/6N2/7N1/7N1/6N2 b - 1"):
        print(board2.position())
        return True
    elif piece_match(board, "sfen 9/9/9/9/9/6P1G/6SG1/6SG1/6L1G b - 1") and no_piece_match(board, "sfen 9/9/9/9/9/7N1/8N/8N/7N1 b - 1"):
        print(board2.position())
        return True
    return False

def invert_sfen(sfen):
    sfenlist = sfen.split()
    #盤面を反転
    chars = list(sfenlist[1])
    i = 0
    while i < len(chars) - 1:
        if chars[i] == '+':
            chars[i], chars[i + 1] = chars[i + 1], chars[i]
            i += 2
        else:
            i += 1
    chars = "".join(chars)
    sfenlist[1] = chars[::-1].swapcase()
    #手番を反転
    if sfenlist[2] == "b":
        sfenlist[2] = "w"
    elif sfenlist[2] == "w":
        sfenlist[2] = "b"
    #持駒を反転
    sfenlist[3] = sfenlist[3].swapcase()
    #sfenlistを結合
    return " ".join(sfenlist)

rfile = open("4000.sfen", "r")
usilist = rfile.readlines()

for usi in usilist:
    b = Board()
    position = usi.split()
    moves = position[position.index("moves")+1:]
    if len(moves) > 64:
        moves = moves[:64]
    for move in moves:
        if move == "resign":
            break
        b.push(move)
        if k_match(b, b):
            break
        b2 = Board(invert_sfen(b.sfen()))
        if k_match(b2, b):
            break
