from Board import *

board = Board()

board.set("sfen lnsgk2nl/1r4gs1/p1pppp1pp/6p2/1p5P1/2P6/PPSPPPP1P/7R1/LN1GKGSNL b Bb 13") #sfen局面で指定
#board.set("position startpos moves 2g2f 8c8d 2f2e 8d8e 7g7f 4a3b 8h7g 3c3d 7i8h 2b7g+ 8h7g 3a2b") #棋譜でも指定できる

print(board.turn())              #手番。先手 = 1, 後手 = -1
print(board.is_sennichite())     #棋譜内の重複局面の有無
print(board.legal_moves())       #合法手生成

move = board.legal_moves().pop() #合法手はset型に格納している。ここではランダムに一手取り出してみる。
board.push(move)                 #一手進める。

print(board.sfen())              #sfen出力
board.pop()                      #一手戻す。
