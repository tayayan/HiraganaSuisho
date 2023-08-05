#USIと標準入出力を介してやりとりするプログラム

import subprocess
import threading

def usi(command):
    shogi.stdin.write(command+"\n")
    shogi.stdin.flush()

def output():
    while True:
        line = shogi.stdout.readline()
        print(line, end="", flush=True)
        
shogi = subprocess.Popen("./YO.exe",
                         stdin=subprocess.PIPE,
                         stdout=subprocess.PIPE,
                         encoding="UTF-8")

t = threading.Thread(target=output, daemon=True)
t.start()

while True:
    command = input()
    usi(command)
    if command == "quit":
        quit()
