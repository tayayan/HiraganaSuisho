from Board import *

def tac_andmatch(board, sfen):
    tacboard = Board(sfen)
    for i in range(11, 114):
        if tacboard.board[i] != "0" and tacboard.board[i] != 0 and tacboard.board[i] != "/" and tacboard.board[i] != board.board[i]:
            return False
    return True
    
def tac_ormatch(board, sfen):
    tacboard = Board(sfen)
    for i in range(11, 114):
        if tacboard.board[i] != "0" and tacboard.board[i] != 0 and tacboard.board[i] != "/" and tacboard.board[i] == board.board[i]:
            return True
    return False

def enc_match(board):
    #振り飛車の囲い
    if tac_andmatch(board, "sfen 9/9/9/9/9/9/7S1/6G2/9 b - 1") and tac_ormatch(board, "sfen 9/9/9/9/9/9/9/5K1K1/6K2 b - 1"):
        return "銀冠"
    elif tac_andmatch(board, "sfen 9/9/9/9/9/9/5G3/6S2/5G3 b - 1") and tac_ormatch(board, "sfen 9/9/9/9/9/9/9/7K1/6K2 b - 1"):
        return "高美濃"
    elif tac_andmatch(board, "sfen 9/9/9/9/9/9/5S3/4G1S2/5G3 b - 1") and tac_ormatch(board, "sfen 9/9/9/9/9/9/9/7K1/6K2 b - 1"):
        return "ダイヤモンド美濃"
    elif tac_andmatch(board, "sfen 9/9/9/9/9/5S3/5G3/6S2/5G3 b - 1") and tac_ormatch(board, "sfen 9/9/9/9/9/9/9/7K1/6K2 b - 1"):
        return "四枚美濃"
    elif tac_andmatch(board, "sfen 9/9/9/9/9/9/6S2/6S2/5G3 b - 1") and tac_ormatch(board, "sfen 9/9/9/9/9/9/9/7K1/6K2 b - 1"):
        return "大山美濃"
    elif tac_andmatch(board, "sfen 9/9/9/9/9/7P1/5PP2/6SK1/5G3 b - 1"):
        return "ちょんまげ美濃"
    elif tac_andmatch(board, "sfen 9/9/9/9/9/9/9/6SK1/5G3 b - 1") and not tac_ormatch(board, "sfen 9/9/9/9/7P1/7P1/7P1/9/9 b - 1"):
        return "坊主美濃"
    elif tac_andmatch(board, "sfen 9/9/9/9/9/9/7P1/4G1S2/5G3 b - 1") and tac_ormatch(board, "sfen 9/9/9/9/9/9/9/7K1/6K2 b - 1"):
        return "本美濃"
    elif tac_andmatch(board, "sfen 9/9/9/9/9/9/9/6S2/4GG3 b - 1") and tac_ormatch(board, "sfen 9/9/9/9/9/9/9/7K1/6K2 b - 1"):
        return "ヒラメ囲い"
    elif tac_andmatch(board, "sfen 9/9/9/9/9/9/5S1P1/6G2/9 b - 1") and tac_ormatch(board, "sfen 9/9/9/9/9/9/9/7K1/6K2 b - 1"):
        return "木村美濃"
    elif tac_andmatch(board, "sfen 9/9/9/9/9/9/7P1/5SG2/9 b - 1") and tac_ormatch(board, "sfen 9/9/9/9/9/9/9/7K1/6K2 b - 1"):
        return "金美濃"
    elif tac_andmatch(board, "sfen 9/9/9/9/9/9/7P1/4S1S2/5G3 b - 1") and tac_ormatch(board, "sfen 9/9/9/9/9/9/9/7K1/6K2 b - 1"):
        return "銀美濃"
    elif tac_andmatch(board, "sfen 9/9/9/9/9/9/7P1/6S2/5G3 b - 1") and tac_ormatch(board, "sfen 9/9/9/9/9/9/9/7K1/6K2 b - 1"):
        return "片美濃"
    elif tac_andmatch(board, "sfen 9/9/9/9/9/9/9/5GK2/6S2 b - 1"):
        return "金立美濃"
    elif tac_andmatch(board, "sfen 9/9/9/9/9/9/9/5SK2/4G4 b - 1"):
        return "ずれ美濃"
    elif tac_andmatch(board, "sfen 9/9/9/9/9/9/9/5SK2/6G2 b - 1"):
        return "振り飛車エルモ"
    elif tac_andmatch(board, "sfen 9/9/9/9/9/9/9/5SK2/5G3 b - 1"):
        return "早美濃"
    elif tac_andmatch(board, "sfen 9/9/9/9/9/9/6S2/6G2/9 b - 1") and tac_ormatch(board, "sfen 9/9/9/9/9/9/9/5K1K1/6K2 b - 1"):
        return "右矢倉"
    elif tac_andmatch(board, "sfen 9/9/9/9/9/9/9/7SL/7NK b - 1"):
        return "振り飛車穴熊"
    elif tac_andmatch(board, "sfen 9/9/9/9/9/9/9/7S1/6GK1 b - 1") or tac_andmatch(board, "sfen 9/9/9/9/9/9/9/6G2/6SK1 b - 1"):
        return "振り飛車ミレニアム"
    elif tac_andmatch(board, "sfen 9/9/9/9/9/9/9/4GGK2/9 b - 1"):
        return "金無双"
    elif tac_andmatch(board, "sfen 9/9/9/9/9/9/9/3GG4/9 b - 1") and tac_ormatch(board, "sfen 9/9/9/9/9/9/9/5KK2/9 b - 1"):
        return "離れ金無双"
    #対振り飛車の囲い
    elif tac_andmatch(board, "sfen 9/9/9/9/9/9/9/1BK1G4/2SG5 b - 1"):
        return "舟囲い"
    elif tac_andmatch(board, "sfen 9/9/9/9/9/9/9/2KS5/2G6 b - 1"):
        return "エルモ囲い"
    elif tac_andmatch(board, "sfen 9/9/9/9/9/9/1SS6/LGG6/KN7 b - 1"):
        return "ビッグ4"
    elif tac_andmatch(board, "sfen 9/9/9/9/9/9/2S6/LSG6/KNG6 b - 1"):
        return "四枚穴熊"
    elif tac_andmatch(board, "sfen 9/9/9/9/9/9/9/LSG6/KNS6 b - 1"):
        return "松尾流穴熊"
    elif tac_andmatch(board, "sfen 9/9/9/9/9/9/1S7/L8/KN7 b - 1"):
        return "銀冠穴熊"
    elif tac_andmatch(board, "sfen 9/9/9/9/9/9/9/LS7/KN7 b - 1"):
        return "居飛車穴熊"
    elif tac_andmatch(board, "sfen 9/9/9/9/9/9/9/1S7/1KG6 b - 1") or tac_andmatch(board, "sfen 9/9/9/9/9/9/9/2G6/1KS6 b - 1"):
        return "ミレニアム"
    elif tac_andmatch(board, "sfen 9/9/9/9/9/9/1S7/2G6/9 b - 1") and tac_ormatch(board, "sfen 9/9/9/9/9/9/9/1K1KK4/2KKK4 b - 1"):
        return "銀冠"
    elif tac_ormatch(board, "sfen 9/9/9/9/9/9/9/5KK2/9 b - 1") and tac_ormatch(board, "sfen 9/9/9/9/9/9/9/7R1/7R1 b - 1"):
        return "右玉"
    elif tac_andmatch(board, "sfen 9/9/9/9/9/9/1S7/K8/9 b - 1"):
        return "端玉銀冠"
    elif tac_andmatch(board, "sfen 9/9/9/9/9/9/1K7/2S6/3G5 b - 1"):
        return "天守閣美濃"
    elif tac_andmatch(board, "sfen 9/9/9/9/9/9/9/1KS6/3G5 b - 1"):
        return "左美濃"
    elif tac_andmatch(board, "sfen 9/9/9/9/9/9/2S6/2KGG4/9 b - 1"):
        return "ボナンザ囲い"
    elif tac_andmatch(board, "sfen 9/9/9/9/9/9/1S7/2KGG4/9 b - 1"):
        return "銀冠金無双"
    elif tac_andmatch(board, "sfen 9/9/9/9/9/9/P8/KS7/LN7 b - 1"):
        return "串カツ囲い"
    elif tac_andmatch(board, "sfen 9/9/9/9/9/9/9/2KG5/2SG5 b - 1"):
        return "箱入り娘"
    elif tac_andmatch(board, "sfen 9/9/9/9/9/2P6/1P1P5/1BKGG4/2S6 b - 1"):
        return "居飛車金無双"
    #相居飛車の囲い
    elif  tac_andmatch(board, "sfen 9/9/9/9/3P5/3S5/2SG5/2G6/9 b - 1") and tac_ormatch(board, "sfen 9/9/9/9/9/9/9/1K1K5/2KKK4 b - 1"):
        return "菱矢倉"
    elif  tac_andmatch(board, "sfen 9/9/9/9/9/9/2SGS4/2G6/9 b - 1") and tac_ormatch(board, "sfen 9/9/9/9/9/9/9/1K1K5/2KKK4 b - 1"):
        return "総矢倉"
    elif  tac_andmatch(board, "sfen 9/9/9/9/9/9/2SG5/2G6/9 b - 1") and tac_ormatch(board, "sfen 9/9/9/9/9/9/9/1K1K5/2KKK4 b - 1"):
        return "金矢倉"
    elif  tac_andmatch(board, "sfen 9/9/9/9/9/9/2SS5/2G6/9 b - 1") and tac_ormatch(board, "sfen 9/9/9/9/9/9/9/1K1K5/2KKK4 b - 1"):
        return "銀矢倉"
    elif tac_andmatch(board, "sfen 9/9/9/9/9/9/2NG5/1SG6/1K7 b - 1"):
        return "菊水矢倉"
    elif tac_andmatch(board, "sfen 9/9/9/9/9/9/2SG5/2K1G4/9 b - 1"):
        return "土居矢倉"
    elif tac_andmatch(board, "sfen 9/9/9/9/9/9/2SG5/2KG5/9 b - 1"):
        return "天野矢倉"
    elif tac_andmatch(board, "sfen 9/9/9/9/2P6/2S6/3G5/2G6/9 b - 1") and tac_ormatch(board, "sfen 9/9/9/9/9/9/9/1KK6/9 b - 1"):
        return "銀立ち矢倉"
    elif  tac_andmatch(board, "sfen 9/9/9/9/9/9/2S6/2G6/9 b - 1") and tac_ormatch(board, "sfen 9/9/9/9/9/9/9/1K7/2K6 b - 1"):
        return "矢倉"
    elif  tac_andmatch(board, "sfen 9/9/9/9/9/9/3S5/2G6/9 b - 1") and tac_ormatch(board, "sfen 9/9/9/9/9/9/9/1K1K5/2KK5 b - 1"):
        return "雁木"
    elif  tac_andmatch(board, "sfen 9/9/9/9/9/9/2S6/2K6/9 b - 1") and tac_ormatch(board, "sfen 9/9/9/9/9/9/9/1B7/2B6 b - 1"):
        return "早囲い"
    elif tac_andmatch(board, "sfen 9/9/9/9/9/9/9/1BS6/2KG5 b - 1"):
        return "居角左美濃"
    elif tac_andmatch(board, "sfen 9/9/9/9/9/9/9/2G2S3/2SKG4 b - 1"):
        return "中原囲い"
    elif tac_andmatch(board, "sfen 9/9/9/9/9/9/9/2GSG4/3K5 b - 1"):
        return "カニ囲い"
    elif tac_andmatch(board, "sfen 9/9/9/9/9/9/9/2GKG4/2S6 b - 1"):
        return "イチゴ囲い"
    elif tac_andmatch(board, "sfen 9/9/9/9/9/9/9/3SKS3/6G2 b - 1") and tac_ormatch(board, "sfen 9/9/9/9/9/9/9/2G6/2G6 b - 1"):
        return "アヒル囲い"
    elif  tac_andmatch(board, "sfen 9/9/9/9/9/9/9/4K4/9 b - 1") and tac_ormatch(board, "sfen 9/9/9/9/9/9/9/5GG2/5G3 b - 1"):
        return "中住まい"
    elif tac_andmatch(board, "sfen 9/9/9/9/9/9/9/3SRS3/3GKG3 b - 1"):
        return "無敵囲い"
    else:
        return ""

def bt_match1(board):
    #戦型判定1（一度判定されたら覆らない＆先後判定不要）
    if tac_andmatch(board, "sfen 9/1r7/9/1p7/9/9/9/1+b5R1/2S6 b b 1") and tac_ormatch(board, "sfen 9/9/9/9/7P1/7P1/9/9/9 b - 1"):
        return "一手損角換わり"
    elif tac_andmatch(board, "sfen 9/1r7/9/9/9/9/2S6/1B5R1/9 b - 1") and tac_ormatch(board, "sfen 9/9/9/9/7P1/7P1/7P1/9/9 b - 1"):
        return "矢倉"
    elif tac_andmatch(board, "sfen 9/1r4gb1/6p2/9/1p5P1/9/2P6/1BG4R1/9 b - 1"):
        return "相掛かり"
    elif tac_andmatch(board, "sfen lnsgk1snl/6gb1/p1pppp2p/6R2/9/1rP6/P2PPPP1P/1BG6/LNS1KGSNL w 3P2p 16"):
        return "横歩取り"
    elif tac_andmatch(board, "sfen 9/1r7/9/9/9/9/9/7R1/9 b Bb 1") and tac_ormatch(board, "sfen 9/9/9/9/7P1/7P1/9/9/9 b - 1") and tac_ormatch(board, "sfen 9/9/9/1p7/1p7/9/9/9/9 b - 1"):
        return "角換わり"
    elif tac_andmatch(board, "sfen 9/1r5b1/9/6p2/2P6/9/2N6/1BR6/2S6 b - 1"):
        return "鬼殺し"
    else:
        return ""

def bt_match2(board):
    #戦型判定2（一度判定されたら覆らない＆先後判定必要）
    if tac_andmatch(board, "sfen 9/9/9/9/9/9/7P1/3R5/9 b - 1"):
        return "四間飛車"
    elif tac_andmatch(board, "sfen 9/9/9/9/9/9/7P1/2R6/9 b - 1"):
        return "三間飛車"
    elif tac_andmatch(board, "sfen 9/9/9/9/9/9/7P1/1R7/9 b - 1"):
        return "向かい飛車"
    elif tac_andmatch(board, "sfen 9/9/9/9/9/9/7P1/4R4/9 b - 1"):
        return "中飛車"
    elif tac_andmatch(board, "sfen 2sgk4/1r5s1/3ppp3/6p2/5B3/9/9/9/9 w - 1"):
        return "筋違い角"
    else:
        return ""


def tac_match1(board):
    #作戦判定1（作戦判定＆先後判定不要）
    if tac_andmatch(board, "sfen 9/9/9/9/9/9/9/5G3/7R1 b - 1"):
        return "4八金・2九飛車型"
    elif tac_andmatch(board, "sfen 1r7/3g5/9/9/9/9/9/9/9 b - 1"):
        return "6二金・8一飛車型"
    elif tac_andmatch(board, "sfen 9/1r7/9/9/5N1P1/9/2S6/7R1/5G3 b Bb 1") and tac_ormatch(board, "sfen 9/9/9/9/9/9/9/5SS2/9 b - 1") and tac_ormatch(board, "sfen 9/9/9/9/9/9/9/3K5/4K4 b - 1"):
        return "4五桂速攻"
    elif tac_andmatch(board, "sfen 9/1r7/9/9/2P6/9/3P5/1BR6/9 b - 1") and not tac_ormatch(board, "sfen 9/9/9/9/6p2/9/9/9/9 b - 1"):
        return "早石田"
    else:
        return ""

def tac_match2(board):
    #作戦判定2（作戦判定＆先後判定必要）
    if tac_andmatch(board, "sfen 9/9/9/9/9/7S1/9/9/9 b - 1") and tac_ormatch(board, "sfen 9/9/9/9/9/9/7R1/7R1/7R1 b - 1"):
        return "棒銀"
    elif tac_andmatch(board, "sfen 9/9/9/9/9/5SP2/5P3/9/9 b - 1") and tac_ormatch(board, "sfen 9/9/9/9/9/7R1/7R1/7R1/7R1 b - 1"):
        return "早繰り銀"
    elif tac_andmatch(board, "sfen 9/9/9/9/9/4SP3/4P4/9/9 b - 1") and tac_ormatch(board, "sfen 9/9/9/9/9/7R1/7R1/7R1/7R1 b - 1"):
        return "腰掛け銀"
    elif tac_andmatch(board, "sfen 9/9/9/9/9/9/9/5R3/9 b - 1") and not tac_ormatch(board, "sfen 9/9/9/9/9/9/9/6KK1/5KK2 b - 1"):
        return "右四間飛車"
    elif tac_andmatch(board, "sfen 9/9/9/9/9/7R1/9/9/9 b - 1") and not tac_ormatch(board, "sfen 9/9/9/9/9/9/7P1/9/9 b - 1"):
        return "浮き飛車"
    elif tac_andmatch(board, "sfen 9/9/9/9/9/9/9/8R/9 b - 1") and tac_ormatch(board, "sfen 9/9/9/9/9/8L/8L/9/9 b - 1"):
        return "雀刺し"
    elif tac_andmatch(board, "sfen 9/9/9/9/9/2PP5/9/3R5/9 b - 1") and tac_ormatch(board, "sfen 9/9/9/9/9/9/9/5KKK1/4K1KKK b - 1"):
        return "ノーマル四間飛車"
    elif tac_andmatch(board, "sfen 9/9/9/9/9/2PP5/9/2R6/9 b - 1") and tac_ormatch(board, "sfen 9/9/9/9/9/9/9/5KKK1/4K1KKK b - 1"):
        return "ノーマル三間飛車"
    elif tac_andmatch(board, "sfen 9/9/9/9/9/2P6/3P5/3R5/9 b Bb 1") and tac_ormatch(board, "sfen 9/9/9/9/9/9/9/5KKK1/4K1KKK b - 1"):
        return "角交換四間飛車"
    elif tac_andmatch(board, "sfen 9/9/9/9/9/2P6/3P5/2R6/9 b Bb 1") and tac_ormatch(board, "sfen 9/9/9/9/9/9/9/5KKK1/4K1KKK b - 1"):
        return "角交換三間飛車"
    elif tac_andmatch(board, "sfen 9/1r7/9/9/9/2P6/3P5/4R4/9 b - 1") and tac_ormatch(board, "sfen 9/9/9/9/4P4/4P4/9/9/9 b - 1") and tac_ormatch(board, "sfen 9/9/9/9/9/9/9/5KKK1/4K1KKK b - 1"):
        return "ゴキゲン中飛車"
    elif tac_andmatch(board, "sfen 9/9/9/9/2P6/2R6/7P1/9/9 b - 1") and tac_ormatch(board, "sfen 9/9/9/9/9/9/9/5KKK1/4K1KKK b - 1"):
        return "石田流"
    elif tac_andmatch(board, "sfen 9/9/9/9/9/9/B1P6/4R4/9 b - 1") and tac_ormatch(board, "sfen 9/9/9/9/9/9/9/5KKK1/4K1KKK b - 1"):
        return "端角中飛車"
    else:
        return ""
        
def invert_sfen(sfen):
    sfenlist = sfen.split()
    #盤面を反転
    chars = list(sfenlist[1])
    i = 0
    while i < len(chars) - 1:
        if chars[i] == '+':
            chars[i], chars[i + 1] = chars[i + 1], chars[i]
            i += 2
        else:
            i += 1
    chars = "".join(chars)
    sfenlist[1] = chars[::-1].swapcase()
    #手番を反転
    if sfenlist[2] == "b":
        sfenlist[2] = "w"
    elif sfenlist[2] == "w":
        sfenlist[2] = "b"
    #持駒を反転
    sfenlist[3] = sfenlist[3].swapcase()
    #sfenlistを結合
    return " ".join(sfenlist)

position = input("positionから始まる棋譜データを入力してね！\n")
bt = sente_bt = gote_bt = tac = tac2 = sente_tac = sente_tac2 = gote_tac = gote_tac2 = sente_enc = sente_enc2 = gote_enc = gote_enc2 = ""
if "moves" in position:
    b = Board(position[:position.index("moves")-1])
    position = position.split()
    moves = position[position.index("moves")+1:]
    for move in moves:
        b.push(move)
        #戦型判定
        if bt == "":
            bt = bt_match1(b)
            if bt != "":
                print("戦型：" + bt + "(" + str(b.ply()-1) + "手目)")
            else:
                if sente_bt == "":
                    sente_bt = bt_match2(b)
                    if sente_bt != "":
                        print("戦型（先手）：" + sente_bt + "(" + str(b.ply()-1) + "手目)")
                if gote_bt == "":
                    b2 = Board(invert_sfen(b.sfen()))
                    gote_bt = bt_match2(b2)
                    if gote_bt != "":
                        print("戦型（後手）：" + gote_bt + "(" + str(b.ply()-1) + "手目)")

        #作戦判定
        tac = tac_match1(b)
        if tac != tac2:
            print("作戦：" + tac + "(" + str(b.ply()-1) + "手目)")
            tac2 = tac
        sente_tac = tac_match2(b)
        if sente_tac != sente_tac2:
            print("作戦（先手）：" + sente_tac + "(" + str(b.ply()-1) + "手目)")
            sente_tac2 = sente_tac
        b2 = Board(invert_sfen(b.sfen()))
        gote_tac = tac_match2(b2)
        if gote_tac != gote_tac2:
            print("作戦（後手）：" + gote_tac + "(" + str(b.ply()-1) + "手目)")
            gote_tac2 = gote_tac

        #囲い判定
        sente_enc = enc_match(b)
        if sente_enc != sente_enc2:
            print("囲い（先手）：" + sente_enc + "(" + str(b.ply()-1) + "手目)")
            sente_enc2 = sente_enc    
        gote_enc = enc_match(b2)
        if gote_enc != gote_enc2:
            print("囲い（後手）：" + gote_enc + "(" + str(b.ply()-1) + "手目)")
            gote_enc2 = gote_enc
input()
