from Board import *
import time
import datetime
import threading
import subprocess
import pickle

#Copyright (c) tayayan
#Released under the MIT license
#https://opensource.org/licenses/mit-license.php

class Shogi:
    book = dict()   #定跡データ
    kif = list()    #棋譜データ
    endturn = None  #終局時の手番
    win = 0         #連勝数
    kif_total = 0   #連続対局数
    lock = threading.RLock()

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
        
        def minmax_in_book(board, book, tt): #定跡内ミニマックス探索
            sfen = board.sfen()
            sfen = sfen[:sfen.rindex(" ")+1] + "0"
            if sfen not in book:
                return 0, None
            
            if sfen in tt:
                return tt[sfen]

            moves = sorted(book[sfen].items(), key=lambda x:x[1], reverse=True) #訪問回数順に並べ替える
            for move in moves:
                move = move[0]
                if move == "resign":
                    score = -1
                elif board.is_sennichite():
                    score = 0
                else:
                    board.push(move)
                    score = -minmax_in_book(board, book, tt)[0]
                    board.pop()
                    if score == 1: #勝つ枝が見つかればbreakしてよい（簡易的なアルファカット）
                        break            
            tt[sfen] = (score, move)
            return score, move

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
        tempbook = dict()
        #1局内の棋譜データ
        tempkif = [Shogi.basesfen]
        #終局したかを確認するための変数
        end = 0
        
        while True: #連続対局
            sfen = board.sfen()
            sfen = sfen[:sfen.rindex(" ")+1] + "0"
            #定跡内ミニマックス探索（本プログラムの核となる部分）
            with Shogi.lock: #同期処理
                score, move = minmax_in_book(board, Shogi.book, dict())
            #定跡内の指し手に勝つ枝があればそれを指す
            if score == 1:
                bestmove = move
            #なければ探索して指す
            else:
                usi("position " + sfen)
                usi("go nodes " + Shogi.nodes)
                while True:
                    line = shogi.stdout.readline()
                    if line[:8] == "bestmove":
                        bestmove = line.split()[1]
                        tempbook[sfen] = bestmove #指し手を定跡に一時保存
                        break

            tempkif.append(bestmove)  #棋譜一時保存

            with Shogi.lock: #同期処理
                if bestmove == "resign": #投了処理
                    #連勝表記
                    if Shogi.endturn == board.turn():
                        Shogi.win += 1
                    else:
                        Shogi.win = 1
                    if board.turn() == -1:
                        print(f"{Shogi.win}連勝(先手) 連続対局数={Shogi.kif_total} 定跡データ局面数={len(Shogi.book)}")
                    elif board.turn() == 1:
                        print(f"{Shogi.win}連勝(後手) 連続対局数={Shogi.kif_total} 定跡データ局面数={len(Shogi.book)}")
                    Shogi.endturn = board.turn()
                
                    #定跡保存
                    for i in tempbook: #訪問回数を保存しつつ登録
                        if i in Shogi.book:
                            if tempbook[i] in Shogi.book[i]:
                                Shogi.book[i][tempbook[i]] += 1
                            else:
                                Shogi.book[i][tempbook[i]] = 1
                        else:
                            Shogi.book[i] = {tempbook[i]:1}
                    end = 1
                    
                elif board.is_sennichite(): #千日手処理
                        tempkif[-1] = "rep_draw"
                        Shogi.win = 0
                        print(f"千日手 連続対局数={Shogi.kif_total} 定跡データ局面数={len(Shogi.book)}")
                        end = 1

                if end == 1: #終局処理
                    #棋譜保存
                    Shogi.kif.append(" ".join(tempkif))
                    #自動棋譜書き出し（100局毎に保存）
                    Shogi.kif_total += 1
                    if Shogi.kif_total % 100 == 0:
                        print("makeautokif...")
                        with open(Shogi.kiffile,"w") as mk:
                            for k in Shogi.kif:
                                mk.write(k + "\n")
                        savebook()
                    #初期化
                    tempkif = [Shogi.basesfen]
                    tempbook.clear()
                    board.set(Shogi.basesfen)
                    end = 0
                    continue
                
            #終局していないので1手進める
            board.push(bestmove)

def makebook(book): #定跡dbファイル作成
    def minmax(board, book, mb, tt):                    
        sfen = board.sfen()
        sfen = sfen[:sfen.rindex(" ")+1] + "0"
        if sfen in tt:
            return tt[sfen]
        moves = sorted(book[sfen].items(), key=lambda x:x[1], reverse=True) 
        for move in moves:
            visit = move[1]
            move = move[0]
            if move == "resign":
                score = -1
            elif board.is_sennichite():
                score = 0
            else:
                board.push(move)
                score = -minmax(board, book, mb, tt)
                board.pop()
                if score == 1:
                    if visit > 1: #訪問回数2回以上の枝を定跡にする。
                        mb.write(sfen + "\n" + move + " None 0 32 " + str(visit) + "\n")
                    break
        tt[sfen] = score
        return score
    with Shogi.lock: #同期処理
        board = Board()
        board.set(Shogi.basesfen)
        with open(Shogi.bookfile,"w") as mb:
            mb.write("#YANEURAOU-DB2016 1.00\n")
            minmax(board, book, mb, dict())
        print("makebookok")


def savebook():
    with Shogi.lock: #同期処理
        with open('book.pickle', 'wb') as file:
            pickle.dump(Shogi.book, file)


def loadbook():
    with Shogi.lock: #同期処理
        with open('book.pickle', 'rb') as file:
            Shogi.book = pickle.load(file)


thread = int(input("並列対局数を入力してね（スレッド数÷4を最大値としてね）\n"))

for i in range(thread): #指定スレッド数だけインスタンスを立ち上げる
    exec("shogi" + str(i) + "=Shogi()")
    exec("t" + str(i) + "=threading.Thread(target=shogi" + str(i) + ".play, daemon=True)")
    exec("t"+ str(i) +".start()")
    time.sleep(0.5)

# loadbook()

print("連続対局開始...")

while True:
    a = input()
    #棋譜手動書き出し
    if a == "makekif":
        with open(Shogi.kiffile,"w") as mk:
            for k in Shogi.kif:
                mk.write(k + "\n")
        print("makekifok")
    #定跡手動書き出し
    if a == "makebook":
        makebook(Shogi.book)
    #保存
    if a == "savebook":
        savebook()
    #読み込み
    if a == "loadbook":
        loadbook()
