from kif_to_usi import *
import os

path = "./"+input("pathを入力してね\n")
files = os.listdir(path)
wfile = open("test.sfen", "w")
for i in files:
    if ".csa" not in i:
        continue
    rfile = open(path+"/"+i, "r")
    csa_string = rfile.read()
    rfile.close()
    sfen = csa_to_usi(csa_string)
    wfile.write(sfen + "\n")

wfile.close()

input("end!")
