from Board import *
import random

board = Board()

while True:
    cmd = input()
    
    if cmd == "usi":
        print("id name Random_Player")
        print("usiok")

    elif cmd == "isready":
        print("readyok")

    elif cmd[:8] == "position":
        board.set(cmd)

    elif cmd[:2] == "go":
        moves = board.legal_moves()
        if moves == set():
            print("bestmove resign")
        else:
            print("bestmove " + random.choice(list(moves)))

    elif cmd == "quit":
        break
