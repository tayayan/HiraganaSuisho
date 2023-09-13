from Board import *
import random
import time
import datetime
import threading
import subprocess

#Copyright (c) tayayan
#Released under the MIT license
#https://opensource.org/licenses/mit-license.php

class Shogi:
    book = dict()   #定跡データ
    book0 = None
    kif = list()    #棋譜データ
    endturn = None  #終局時の手番
    win = 0         #連勝数
    kif_total = 0   #連続対局数
    lock = threading.RLock()

    #エンジンパス指定
    engine = input("将棋エンジン（やねうら王etc）のパスを入力してね\n")
    
    #初期局面（ここから連続対局する）
    basesfen = input("usi棋譜（position startposから始まる文字列）を入力してね。入力しなければ平手初期局面\n")
    basesfen = basesfen[9:]
    if len(basesfen) < 13:
        basesfen = "startpos moves"
    else:
        bookboard = Board()
        for i in basesfen.split()[2:]:
            sfen = bookboard.sfen()
            sfen = sfen[:sfen.rindex(" ")+1] + "0"
            book[sfen] = {i:1000}
            bookboard.push(i)

    #定跡読み込み
    readbook = input("やねうら王dbファイルをロードする場合、パスを入力してね（例：standard_book.db）\n")
    if readbook[-3:] == ".db":
        rfile = open(readbook,"r", errors='ignore')
        s = rfile.readline() #「#YANEURAOU-DB2016 1.00」をスキップ
        while True:
            s = rfile.readline().strip()
            if s == "":
                break
            elif s[:4] == "sfen":
                sfen = s[:s.rindex(" ")+1] + "0"
                continue
            else:
                move = s.split()[0]
                
            if sfen in book:
                book[sfen][move] = 1
            else:
                book[sfen] = {move:1}
                
        book_fix = input("定跡の穴探索モード？ b:先手定跡の穴を探す w:後手定跡の穴を探す それ以外:通常モード\n")
        if book_fix == "b" or book_fix == "w":
            book0 = dict()
            for i in book:
                if i.split()[-3] == book_fix:
                    book0[i] = book[i]
            book = dict()

    #探索ノード数
    nodes = input("探索ノード数を入力してね（例：20000000）\n")

    #投了値
    resign_value = input("投了値を入力してね（例：300）\n")

    #千日手処理
    draw = input("千日手はどうする？ b:先手負け w:後手負け それ以外:無視\n")

    #保存ファイルに日時を付ける
    t_delta = datetime.timedelta(hours=9)
    JST = datetime.timezone(t_delta, 'JST')
    now = datetime.datetime.now(JST)
    d = now.strftime('%Y%m%d%H%M%S')
    kiffile = "kif" + d + ".sfen"
    bookfile = "book" + d + ".db"
    bookfile2 = "book" + d + "_2.db"

    def play(self):
        def usi(command): #usiコマンド処理
            shogi.stdin.write(command+"\n")
            shogi.stdin.flush()

        #将棋エンジン（やねうら王）を立ち上げる
        shogi = subprocess.Popen(Shogi.engine, stdin=subprocess.PIPE,
                                               stdout=subprocess.PIPE,
                                               encoding="cp932")

        #初期オプション指定
        usi("setoption name Threads value 4") #1スレッドが一番効率いいけど、同じ棋譜が生じやすいので4とする
        usi("setoption name USI_Hash value 1024")
        usi("setoption name ResignValue value " + Shogi.resign_value)
        usi("isready")

        #初期設定
        board = Board()
        board.set(Shogi.basesfen)
        #1局内の定跡データ（終局して勝敗が決してから一括で親定跡データに保存する。）
        tempbook = []
        #1局内の棋譜データ
        tempkif = [Shogi.basesfen]
        #終局したかを確認するための変数
        end = 0
        
        while True: #連続対局
            sfen = board.sfen()
            sfen = sfen[:sfen.rindex(" ")+1] + "0"
            if Shogi.book0 is not None and sfen in Shogi.book0:
                bestmove = random.choice(list(Shogi.book0[sfen].keys()))
            elif sfen in Shogi.book:
                bestmove = random.choice(list(Shogi.book[sfen].keys())) #複数候補がある場合はランダムで選ぶ
            #なければ探索して指す
            else:
                usi("position " + sfen)
                usi("go nodes " + Shogi.nodes)
                while True:
                    line = shogi.stdout.readline()
                    if line[:8] == "bestmove":
                        bestmove = line.split()[1]
                        break
            tempbook.append((sfen, bestmove)) #指し手を定跡に一時保存
            tempkif.append(bestmove)  #棋譜一時保存

            with Shogi.lock: #同期処理                
                if bestmove == "resign": #投了処理
                    #連勝表記
                    if Shogi.endturn == board.turn():
                        Shogi.win += 1
                    else:
                        Shogi.win = 1
                    if board.turn() == -1:
                        print(str(Shogi.win) + "連勝(先手)")
                    elif board.turn() == 1:
                        print(str(Shogi.win) + "連勝(後手)")
                        
                    if Shogi.win % 10 == 0: #定跡自動書き出し（10連勝ごと）
                        print("makeautobook...")
                        mb = open(Shogi.bookfile,"w")
                        mb.write("#YANEURAOU-DB2016 1.00\n")
                        for b in Shogi.book:            
                            mb.write(b + "\n")
                            moves = sorted(Shogi.book[b].items(), key=lambda x:x[1], reverse=True)
                            for move in moves:
                                mb.write(move[0] + " none 0 32 " + str(move[1]) + "\n")
                        mb.close() 
                    Shogi.endturn = board.turn()

                        
                    #定跡保存
                    loseturn = sfen.split()[-3]
                    bookpass = 0
                    for i in reversed(tempbook):
                        if i[0].split()[-3] == loseturn and bookpass == 0:
                            if i[0] in Shogi.book:
                                Shogi.book[i[0]].pop(i[1], None)
                                if Shogi.book[i[0]] == {}:
                                    Shogi.book.pop(i[0])
                                else:
                                    bookpass = 1
                        elif i[0].split()[-3] != loseturn:
                            if i[0] in Shogi.book:
                                if i[1] in Shogi.book[i[0]]:
                                    Shogi.book[i[0]][i[1]] += 1
                                else:
                                    Shogi.book[i[0]][i[1]] = 1
                            else:
                                Shogi.book[i[0]] = {i[1]:1}                            
                    end = 1
                    
                elif board.is_sennichite(): #千日手処理
                    tempkif[-1] = "rep_draw"
                    Shogi.win = 0
                    print("千日手")
                    
                    #定跡保存    
                    if Shogi.draw == "b" or Shogi.draw == "w":
                        loseturn = Shogi.draw
                        bookpass = 0
                        for i in reversed(tempbook):
                            if i[0].split()[-3] == loseturn and bookpass == 0:
                                if i[0] in Shogi.book:
                                    Shogi.book[i[0]].pop(i[1], None)
                                    if Shogi.book[i[0]] == {}:
                                        Shogi.book.pop(i[0])
                                    else:
                                        bookpass = 1
                            elif i[0].split()[-3] != loseturn:
                                if i[0] in Shogi.book:
                                    if i[1] in Shogi.book[i[0]]:
                                        Shogi.book[i[0]][i[1]] += 1
                                    else:
                                        Shogi.book[i[0]][i[1]] = 1
                                else:
                                    Shogi.book[i[0]] = {i[1]:1}

                    end = 1

                if end == 1: #終局処理
                    #棋譜保存
                    Shogi.kif.append(" ".join(tempkif))
                    #自動棋譜書き出し（100局毎に保存）
                    Shogi.kif_total += 1
                    if Shogi.kif_total % 100 == 0:
                        print("makeautokif...")
                        mk = open(Shogi.kiffile,"w")
                        for k in Shogi.kif:
                            mk.write(k + "\n")
                        mk.close()
                    #初期化
                    tempkif = [Shogi.basesfen]
                    tempbook = []
                    board.set(Shogi.basesfen)
                    end = 0
                    continue
                
            #終局していないので1手進める
            board.push(bestmove)

thread = int(input("並列対局数を入力してね（スレッド数÷4を最大値としてね）\n"))

print("\n「makekif」  コマンド：現在までの棋譜ファイル手動作成")
print("「makebook」 コマンド：現在までの定跡ファイル手動作成")
print("「makebook2」コマンド：現在までの定跡ファイル手動作成、訪問回数2回以上・上位の手のみを記録\n")

for i in range(thread): #指定スレッド数だけインスタンスを立ち上げる
    exec("shogi" + str(i) + "=Shogi()")
    exec("t" + str(i) + "=threading.Thread(target=shogi" + str(i) + ".play, daemon=True)")
    exec("t"+ str(i) +".start()")
    time.sleep(0.5)

print("連続対局開始...")


def book_to_sfen(book): #定跡データを棋譜化する
    kif = ["startpos moves"]
    board = Board()
    sfen = board.sfen()
    sfen = sfen[:sfen.rindex(" ")+1] + "0"
    wfile = open(input("sfenファイル保存名を入力してね\n"), "w")

    def dfs(sfen):
        nonlocal kif, wfile
        if board.is_sennichite():
            wfile.write(" ".join(kif) + "\n")
        
        if sfen in book:
            move = book[sfen]
            kif.append(move)
            board.push(move)
            sfen = board.sfen()
            sfen = sfen[:sfen.rindex(" ")+1] + "0"
            dfs(sfen)
            board.pop()           
            kif = kif[:-1]
                
        else:
            moves = board.legal_moves()
            a = 0
            for move in moves:
                board.push(move)
                sfen = board.sfen()
                sfen = sfen[:sfen.rindex(" ")+1] + "0"
                if sfen in book:
                    kif.append(move)
                    dfs(sfen)
                    kif = kif[:-1]
                    a = 1
                board.pop()
            if a == 0:
                wfile.write(" ".join(kif) + "\n")    
    dfs(sfen)
    wfile.close()

while True:
    a = input()
    #棋譜手動書き出し
    if a == "makekif":
        with Shogi.lock:
            mk = open(Shogi.kiffile,"w")
            for k in Shogi.kif:
                mk.write(k + "\n")
            mk.close()
            print("makekifok")

    #最善手棋譜書き出し
    if a == "makekifb":
        with Shogi.lock:
            d = dict()
            for i in Shogi.book:
                if i.split()[-3] == "b":
                    moves = sorted(Shogi.book[i].items(), key=lambda x:x[1], reverse=True)
                    if moves[0][1] > 1:
                        d[i] = moves[0][0]
            book_to_sfen(d)                        
            print("makekifbok")

    if a == "makekifw":
        with Shogi.lock:
            d = dict()
            for i in Shogi.book:
                if i.split()[-3] == "w":
                    moves = sorted(Shogi.book[i].items(), key=lambda x:x[1], reverse=True)
                    if moves[0][1] > 1:
                        d[i] = moves[0][0]
            book_to_sfen(d)                        
            print("makekifbok")

    #定跡手動書き出し
    if a == "makebook":
        with Shogi.lock:
            mb = open(Shogi.bookfile,"w")
            mb.write("#YANEURAOU-DB2016 1.00\n")
            for b in Shogi.book:                
                moves = sorted(Shogi.book[b].items(), key=lambda x:x[1], reverse=True)
                mb.write(b + "\n")
                for move in moves:
                    mb.write(move[0] + " none 0 32 " + str(move[1]) + "\n")
            mb.close()
            print("makebookok")

    if a == "makebook2":
        with Shogi.lock:
            mb = open(Shogi.bookfile2,"w")
            mb.write("#YANEURAOU-DB2016 1.00\n")
            for b in Shogi.book:                
                moves = sorted(Shogi.book[b].items(), key=lambda x:x[1], reverse=True)
                if moves[0][1] > 1:
                    mb.write(b + "\n")
                    mb.write(moves[0][0] + " none 0 32 " + str(moves[0][1]) + "\n")
            mb.close()
            print("makebook2ok")
