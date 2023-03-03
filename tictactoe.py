#Алгоритм игры крестики нолики

import symbols as symb
import answers as ans

from telegram import InlineKeyboardButton, InlineKeyboardMarkup

player = symb.symbol0
ai=symb.symbolX

#Победные комбинации
def win(ai, player):
    if (((ai[0] == player) and (ai[4] == player) and (ai[8] == player)) or
            ((ai[2] == player) and (ai[4] == player) and (ai[6] == player)) or
            ((ai[0] == player) and (ai[1] == player) and (ai[2] == player)) or
            ((ai[3] == player) and (ai[4] == player) and (ai[5] == player)) or
            ((ai[6] == player) and (ai[7] == player) and (ai[8] == player)) or
            ((ai[0] == player) and (ai[3] == player) and (ai[6] == player)) or
            ((ai[1] == player) and (ai[4] == player) and (ai[7] == player)) or
            ((ai[2] == player) and (ai[5] == player) and (ai[8] == player))):
        return True
    return False

#Количество свободных клеток (на которые можно ходить)
def countUndefinedCells(cellArray):
    counter = 0
    for i in cellArray:
        if i == symb.symbolDef:
            counter += 1
    return counter

# Cделать данные для первой игры
def newGame(update, _):
    data = ''
    for i in range(0, 9):
        data += symb.symbolDef


