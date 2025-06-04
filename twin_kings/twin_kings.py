#後手玉2枚でも将棋AIを動くようにした
from Board import *
import time
import subprocess
import threading

class Relay: #共有変数
    switch = 0
    score1 = 0
    score2 = 0
    line1 = ""
    line2 = ""
    lset = set()
    
def usi(command):
    Relay.switch = 0
    if command[:8] == "position":
        b = Board(command)
        Relay.lset = b.legal_moves()
        klist = b.piece_location("k")
        b.board[klist[0]] = "g"        
        shogi.stdin.write("position " + b.sfen() + "\n")
        shogi.stdin.flush()
        b = Board(command)
        b.board[klist[1]] = "g"
        shogi2.stdin.write("position " + b.sfen() + "\n")
        shogi2.stdin.flush()
    else:
        shogi.stdin.write(command+"\n")
        shogi.stdin.flush()
        shogi2.stdin.write(command+"\n")
        shogi2.stdin.flush()

def output(): #エンジン1の出力
    while True:
        Relay.line1 = shogi.stdout.readline()
        if Relay.line1[:8] == "bestmove":
            line0 = line0.split()
            if "cp" in line0:
                Relay.score1 = int(line0[line0.index("cp")+1])
            elif "mate" in line0:
                Relay.score1 = int(line0[line0.index("mate")+1])
            if Relay.switch == 1:
                if Relay.line2.split()[1] in Relay.lset and (Relay.score1 > Relay.score2 or Relay.line1.split()[1] not in Relay.lset):
                    print(Relay.line2, end="", flush=True)
                elif Relay.line1.split()[1] in Relay.lset:
                    print(Relay.line1, end="", flush=True)
                elif Relay.lset != set():
                    print("bestmove " + Relay.lset.pop(), flush=True)
                else:
                    print("bestmove resign", flush=True)
            Relay.switch = 1
            continue
        line0 = Relay.line1
        print(Relay.line1, end="", flush=True)

def output2(): #エンジン2の出力
    while True:
        Relay.line2 = shogi2.stdout.readline()
        if Relay.line2[:8] == "bestmove":
            line0 = line0.split()
            if "cp" in line0:
                Relay.score2 = int(line0[line0.index("cp")+1])
            elif "mate" in line0:
                Relay.score2 = int(line0[line0.index("mate")+1])
            if Relay.switch == 1:
                if Relay.line2.split()[1] in Relay.lset and (Relay.score1 > Relay.score2 or Relay.line1.split()[1] not in Relay.lset):
                    print(Relay.line2, end="", flush=True)
                elif Relay.line1.split()[1] in Relay.lset:
                    print(Relay.line1, end="", flush=True)
                elif Relay.lset != set():
                    print("bestmove " + Relay.lset.pop(), flush=True)
                else:
                    print("bestmove resign", flush=True)
            Relay.switch = 1
            continue
        line0 = Relay.line2


shogi = subprocess.Popen("./YO.exe",
                         stdin=subprocess.PIPE,
                         stdout=subprocess.PIPE,
                         encoding="cp932")

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
    if command == "quit":
        while shogi.poll() is None or shogi2.poll() is None:
            time.sleep(0.5)
        quit()
