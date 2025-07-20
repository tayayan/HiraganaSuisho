#KIF形式、CSA形式をUSI形式の棋譜にする

def kif_to_usi(kif_string):
    def sfen_num(board_num):
        num = board_num[0] + board_num[1].translate(str.maketrans({'1':'a','2':'b','3':'c','4':'d','5':'e','6':'f','7':'g','8':'h','9':'i'}))
        return num

    def borad_num(sfen_num):
        num = sfen_num.translate(str.maketrans({'一':'a','二':'b','三':'c','四':'d','五':'e','六':'f','七':'g','八':'h','九':'i','１':'1','２':'2','３':'3','４':'4','５':'5','６':'6','７':'7','８':'8','９':'9'}))
        return num

    def piece_to_spiece(piece):
        spiece = piece.translate(str.maketrans({'飛':'R','角':'B','金':'G','銀':'S','桂':'N','香':'L','歩':'P'}))
        return spiece

    moves = ["position startpos", "moves"]
    n = 1
    kif = kif_string.split("\n")
    for line in kif:
        if "手合割：" in line:
            if "平手" in line:
                moves[0] = "position startpos"
            elif "香落ち" in line:
                moves[0] = "position sfen lnsgkgsn1/1r5b1/ppppppppp/9/9/9/PPPPPPPPP/1B5R1/LNSGKGSNL w - 1"
            elif "右香落ち" in line:
                moves[0] = "position sfen 1nsgkgsnl/1r5b1/ppppppppp/9/9/9/PPPPPPPPP/1B5R1/LNSGKGSNL w - 1"
            elif "角落ち" in line:
                moves[0] = "position sfen lnsgkgsnl/1r7/ppppppppp/9/9/9/PPPPPPPPP/1B5R1/LNSGKGSNL w - 1"
            elif "飛車落ち" in line:
                moves[0] = "position sfen lnsgkgsnl/7b1/ppppppppp/9/9/9/PPPPPPPPP/1B5R1/LNSGKGSNL w - 1"
            elif "飛香落ち" in line:
                moves[0] = "position sfen lnsgkgsn1/7b1/ppppppppp/9/9/9/PPPPPPPPP/1B5R1/LNSGKGSNL w - 1"
            elif "二枚落ち" in line:
                moves[0] = "position sfen lnsgkgsnl/9/ppppppppp/9/9/9/PPPPPPPPP/1B5R1/LNSGKGSNL w - 1"
            elif "四枚落ち" in line:
                moves[0] = "position sfen 1nsgkgsn1/9/ppppppppp/9/9/9/PPPPPPPPP/1B5R1/LNSGKGSNL w - 1"
            elif "六枚落ち" in line:
                moves[0] = "position sfen 2sgkgs2/9/ppppppppp/9/9/9/PPPPPPPPP/1B5R1/LNSGKGSNL w - 1"
            elif "八枚落ち" in line:
                moves[0] = "position sfen 3gkg3/9/ppppppppp/9/9/9/PPPPPPPPP/1B5R1/LNSGKGSNL w - 1"
            elif "十枚落ち" in line:
                moves[0] = "position sfen 4k4/9/ppppppppp/9/9/9/PPPPPPPPP/1B5R1/LNSGKGSNL w - 1"
            continue
        line_list = line.split()
        if line_list and line_list[0] == str(n):
            n += 1
            third = ""
            move = line_list[1]
            if move == "投了":
                moves.append("resign")
                continue
            elif move == "千日手":
                moves.append("rep_draw")
                continue
            elif move == "入玉勝ち":
                moves.append("win")
                continue

            if move == "同":
                move = line_list[2]
                if move[move.index("(")-1] == "成":
                    third = "+"
                first = sfen_num(move[move.index("(")+1:move.index(")")])
            elif "打" in move:
                piece = move[move.index("打")-1]
                p = piece_to_spiece(piece)
                first = p + "*"
                second = borad_num(move[:2])
            else:
                first = sfen_num(move[move.index("(")+1:move.index(")")])
                if move[move.index("(")-1] == "成":
                    third = "+"
                second = borad_num(move[:2])
            moves.append(first + second + third)

    if moves[-1] == moves[-2]:
        del moves[-1]
    usi = " ".join(moves)
    return usi

def csa_to_usi(csa_string):
    def sfen_num(board_num):
        num = board_num[0] + board_num[1].translate(str.maketrans({'1':'a','2':'b','3':'c','4':'d','5':'e','6':'f','7':'g','8':'h','9':'i'}))
        return num
    def piece_to_spiece(piece):
        spiece = piece.replace('HI','R')\
                      .replace('KA','B')\
                      .replace('KI','G')\
                      .replace('GI','S')\
                      .replace('KE','N')\
                      .replace('KY','L')\
                      .replace('FU','P')  
        return spiece

    moves = ["position startpos", "moves"]
    board = [""]*100
    board[11],board[91],board[22],board[82],board[28],board[88],board[19],board[99] = "KY","KY","KA","HI","HI","KA","KY","KY"
    csa = csa_string.split("\n")
    for line in csa:
        if line == "":
            continue
        third = ""
        if line == "+":
            continue
        if line[0] == "+" or line[0] == "-":
            first = sfen_num(line[1:3])
            second = sfen_num(line[3:5])
            if first == "00":
                first = piece_to_spiece(line[5:7]) + "*"
            elif line[5:7] == "TO" and board[int(line[1:3])] == "FU":
                third = "+"
            elif line[5:7] == "NY" and board[int(line[1:3])] == "KY":
                third = "+"
            elif line[5:7] == "NK" and board[int(line[1:3])] == "KE":
                third = "+"
            elif line[5:7] == "NG" and board[int(line[1:3])] == "GI":
                third = "+"
            elif line[5:7] == "UM" and board[int(line[1:3])] == "KA":
                third = "+"
            elif line[5:7] == "RY" and board[int(line[1:3])] == "HI":
                third = "+"
            moves.append(first + second + third)
            board[int(line[3:5])] = line[5:7]
        elif line == "%TORYO":
            moves.append("resign")
        elif line == "%SENNICHITE":
            moves.append("rep_draw")
        elif line == "%KACHI":
            moves.append("win")
            
    if moves[-1] == moves[-2]:
        del moves[-1]
    usi = " ".join(moves)
    return usi
