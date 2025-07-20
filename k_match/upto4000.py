import os

path = "./"+input("pathを入力してね\n")
files = os.listdir(path)
for i in files:
    if ".csa" not in i:
        continue
    rfile = open(path+"/"+i, "r")
    read1 = rfile.readlines()
    rfile.close()
    rfile = open(path+"/"+i, "r")
    read2 = rfile.read()
    rfile.close()
    
    remove = 0
    
    for j in read1:
        if "black_rate" in j :
            if float(j[j.rfind(":")+1:j.rfind("\n")]) > 3999 and ("summary:toryo" in read2 or "summary:kachi" in read2) and "lose:" in read2:
                remove = 1
                break
        if "white_rate" in j :
            if float(j[j.rfind(":")+1:j.rfind("\n")]) > 3999 and ("summary:toryo" in read2 or "summary:kachi" in read2) and "win:" in read2:
                remove = 1
            break

    if remove == 0:
        os.remove(path+"/"+i)

print("sakujo")
input()
