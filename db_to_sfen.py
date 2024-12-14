#やねうら王定跡dbファイルを初期局面からのsfen群に変換するプログラム。

from Board import *
import sys

sys.setrecursionlimit(10000)


def db_to_sfen(book):
    kif = ["startpos moves"]
    board = Board()
    sfen = board.sfen()
    sfen = sfen[:sfen.rindex(" ")+1] + "0"
    wfile = open(input("新規sfenファイル名を入力してね\n"), "w")
    s = set()
    w = 0

    def dfs(sfen):
        nonlocal kif, wfile, s, w
        if board.is_sennichite():
            wfile.write(" ".join(kif) + "\n")
            w += 1
            if w % 100 == 0:
                print(str(w)+"棋譜作成済")
            return
        
        elif sfen in book:
            moves = book[sfen]
            for move in moves:
                kif.append(move)
                board.push(move)
                sfen = board.sfen()
                sfen = sfen[:sfen.rindex(" ")+1] + "0"
                if sfen in s:
                    wfile.write(" ".join(kif) + "\n")
                    w += 1
                    if w % 100 == 0:
                        print(str(w)+"棋譜作成済")
                    board.pop()
                    kif = kif[:-1]
                    continue
                else:
                    dfs(sfen)
                board.pop()           
                kif = kif[:-1]
            s.add(sfen)
                
        else:
            moves = board.legal_moves()
            a = 0
            for move in moves:
                board.push(move)
                sfen = board.sfen()
                sfen = sfen[:sfen.rindex(" ")+1] + "0"
                if sfen in book:
                    kif.append(move)
                    if sfen in s:
                        wfile.write(" ".join(kif) + "\n")
                        w += 1
                        if w % 100 == 0:
                            print(str(w)+"棋譜作成済")
                        board.pop()
                        kif = kif[:-1]
                        continue
                    else:
                        dfs(sfen)
                    kif = kif[:-1]
                    a = 1
                board.pop()
            s.add(sfen)
            if a == 0:
                wfile.write(" ".join(kif) + "\n")
                w += 1
                if w % 100 == 0:
                    print(str(w)+"棋譜作成済")
    
    dfs(sfen)
    wfile.close()


db = input("やねうら王dbファイルのパスを入力してね\n")
side = input("先手番定跡のみをsfen化：b 後手番定跡のみをsfen化：w それ以外：入力なし\n")

rfile = open(db,"r",errors='ignore')
s = rfile.readline() #「#YANEURAOU-DB2016 1.00」をスキップ

book = dict()

while True:
    s = rfile.readline().strip()
    if s == "":
        break
    elif s[:4] == "sfen":
        sfen = s[:s.rindex(" ")+1] + "0"
        continue
    else:
        move = s.split()[0]
        if (side == "b" and " w " in sfen) or (side == "w" and " b " in sfen):
            continue
        elif sfen in book:
            book[sfen].add(move)
        else:
            book[sfen] = {move}
            
db_to_sfen(book)
input("完了！\n")
