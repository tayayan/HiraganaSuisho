#評価値を閾値にしたusiリレープログラム

import os
import subprocess
import threading

class Relay: #リレー用の変数
    switch = 0
    
def usi(command):
    if command[:2] == "go": #リレー部分。goコマンドはどちらかにしか送らない
        if Relay.switch == 0:
            shogi.stdin.write(command+"\n")
            shogi.stdin.flush()
        elif Relay.switch == 1:
            shogi2.stdin.write(command+"\n")
            shogi2.stdin.flush()
    else: #他のコマンドは両者に送る
        shogi.stdin.write(command+"\n")
        shogi.stdin.flush()
        shogi2.stdin.write(command+"\n")
        shogi2.stdin.flush()

def output(): #エンジン1の出力
    while True:
        line = shogi.stdout.readline()
        if line[:8] == "bestmove": #bestmoveが出力されたとき、直前の評価値を読み、1500以上であればエンジンを切り替える
            line0 = line0.split()
            score = int(line0[line0.index("cp")+1])
            if score >= 1500:
                Relay.switch = 1
        line0 = line
        print(line, end="", flush=True)

def output2(): #エンジン2の出力
    while True:
        line = shogi2.stdout.readline()
        if Relay.switch == 1: #エンジンが切り替わっているときのみ出力する
            print(line, end="", flush=True)


os.chdir("./engine1") #engine1フォルダに置かれているエンジンを読み込む
shogi = subprocess.Popen("./YO.exe",
                         stdin=subprocess.PIPE,
                         stdout=subprocess.PIPE,
                         encoding="cp932")
os.chdir("..")
os.chdir("./engine2") #engine2フォルダに置かれているエンジンを読み込む
shogi2 = subprocess.Popen("./YO.exe",
                         stdin=subprocess.PIPE,
                         stdout=subprocess.PIPE,
                         encoding="cp932")


t = threading.Thread(target=output, daemon=True)
t.start()
t2 = threading.Thread(target=output2, daemon=True)
t2.start()


while True:
    command = input()
    usi(command)
    if command[:8] == "gameover": #対局終了時にエンジンを戻す
        Relay.switch = 0
    if command == "quit":
        quit()
