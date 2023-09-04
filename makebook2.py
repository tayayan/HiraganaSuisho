from Board import *
import time
import datetime
import threading
import subprocess
from collections import defaultdict

#Copyright (c) tayayan
#Released under the MIT license
#https://opensource.org/licenses/mit-license.php

class Shogi:
    book = defaultdict(set)   #定跡データ
    kif = list()    #棋譜データ
    endturn = None  #終局時の手番
    win = 0         #連勝数
    kif_total = 0   #連続対局数

    #エンジンパス指定
    engine = input("将棋エンジン（やねうら王etc）のパスを入力してね\n")
    
    #初期局面（ここから連続対局する）
    basesfen = input("usi棋譜（position startposから始まる文字列）を入力してね\n")
    basesfen = basesfen[9:]

    #探索ノード数
    nodes = input("探索ノード数を入力してね（例：20000000）\n")

    #投了値
    resign_value = input("投了値を入力してね（例：300）\n")

    #保存ファイルに日時を付ける
    t_delta = datetime.timedelta(hours=9)
    JST = datetime.timezone(t_delta, 'JST')
    now = datetime.datetime.now(JST)
    d = now.strftime('%Y%m%d%H%M%S')
    kiffile = "kif" + d + ".sfen"
    bookfile = "book" + d + ".db"

    def play(self):
        def usi(command): #usiコマンド処理
            shogi.stdin.write(command+"\n")
            shogi.stdin.flush()

        #将棋エンジン（やねうら王）を立ち上げる
        shogi = subprocess.Popen(Shogi.engine, stdin=subprocess.PIPE,
                                               stdout=subprocess.PIPE,
                                               encoding="UTF-8")

        #初期オプション指定
        usi("setoption name Threads value 4") #1スレッドが一番効率いいけど、同じ棋譜が生じやすいので4とする
        usi("setoption name USI_Hash value 1024")
        usi("setoption name ResignValue value " + Shogi.resign_value)
        usi("isready")

        #初期設定
        board = Board()
        board.set(Shogi.basesfen)
        #1局内の定跡データ（終局時に一括で親定跡データに保存する。都度保存だとミニマックス探索が壊れるため）
        tempbook = []
        #1局内の棋譜データ
        tempkif = [Shogi.basesfen]
        #終局したかを確認するための変数
        end = 0
        
        while True: #連続対局
            sfen = board.sfen()
            sfen = sfen[:sfen.rindex(" ")+1] + "0"
            if sfen in Shogi.book:
                bestmove = list(Shogi.book[sfen])[0]
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
                Shogi.endturn = board.turn()
                
                #定跡保存
                loseturn = sfen.split()[-3]
                bookpass = 0
                for i in reversed(tempbook):
                    if i[0].split()[-3] == loseturn and bookpass == 0:
                        Shogi.book[i[0]].discard(i[1])
                        if Shogi.book[i[0]] == set():
                            Shogi.book.pop(i[0])
                        else:
                            bookpass = 1
                    elif i[0].split()[-3] != loseturn:
                        Shogi.book[i[0]].add(i[1])
                end = 1
                
            elif board.is_sennichite(): #千日手処理
                tempkif[-1] = "rep_draw"
                Shogi.win = 0
                print("千日手")
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

for i in range(thread): #指定スレッド数だけインスタンスを立ち上げる
    exec("shogi" + str(i) + "=Shogi()")
    exec("t" + str(i) + "=threading.Thread(target=shogi" + str(i) + ".play, daemon=True)")
    exec("t"+ str(i) +".start()")
    time.sleep(0.5)

print("連続対局開始...")

while True:
    a = input()
    #棋譜手動書き出し
    if a == "makekif":
        mk = open(Shogi.kiffile,"w")
        for k in Shogi.kif:
            mk.write(k + "\n")
        mk.close()
        print("makekifok")
    if a == "makebook":
        mb = open(Shogi.bookfile,"w")
        mb.write("#YANEURAOU-DB2016 1.00\n")
        for b in Shogi.book:            
            mb.write(b + "\n")
            mb.write(list(Shogi.book[b])[0] + " none 0 32 1\n")
        mb.close()
