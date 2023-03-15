#Алгоритм игры крестики нолики

from random import random

import telebot
from telebot import types # для указание типов

import answers
import main
import symbols as symb
import answers as ans

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update

bot = telebot.TeleBot(main.bot)


players = []

#Выбор игры (крестик или нолик)
@bot.message_handler(commands=['newgame'])
def newgame_command(message: telebot.types.Message):
    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(telebot.types.InlineKeyboardButton(text=symb.symbolX, callback_data='x'))
    markup.add(telebot.types.InlineKeyboardButton(text=symb.symbol0, callback_data='o'))

    if message.text == '/newgame':
        msg = bot.send_message(message.chat.id, text='Выбери за кого будешь играть', reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def step(callback_query: telebot.types.CallbackQuery):
    if callback_query.data == 'x':
       ai = symb.symbol0
       player = symb.symbolX
       chat(callback_query.message,ai,player)
       # msg= bot.send_message(callback_query.message.from_user.id,'Отличный выбор!Давай начнем: {}'.format(a))
    elif callback_query.data == 'o':
        msg = bot.send_message(callback_query.message.chat.id, 'Хммм, лааадно, пусть будет по твоему')

#Победные комбинации
def win(arr, who):
    if (((arr[0] == who) and (arr[4] == who) and (arr[8] == who)) or
            ((arr[2] == who) and (arr[4] == who) and (arr[6] == who)) or
            ((arr[0] == who) and (arr[1] == who) and (arr[2] == who)) or
            ((arr[3] == who) and (arr[4] == who) and (arr[5] == who)) or
            ((arr[6] == who) and (arr[7] == who) and (arr[8] == who)) or
            ((arr[0] == who) and (arr[3] == who) and (arr[6] == who)) or
            ((arr[1] == who) and (arr[4] == who) and (arr[7] == who)) or
            ((arr[2] == who) and (arr[5] == who) and (arr[8] == who))):
        return True
    return False

bot_send=True
def make_bot_true():
    global bot_send
    bot_send = True

def make_bot_false():
    global bot_send
    bot_send = False
ai=symb.symbol0
player=symb.symbolX
def check_win(board):
    for i in range(3):
        if board[i][1] == board[i][0] and board[i][1] == board[i][2] and board[i][1] != symb.symbolDef:
            return True, board[i][0]
    for i in range(3):
        if board[1][i] == board[0][i] and board[1][i] == board[2][i] and board[1][i] !=  symb.symbolDef:
            return True, board[1][i]
    for i in range(2):
        if board[0][0] == board[1][1] and board[1][1] !=  symb.symbolDef and board[1][1] == board[2][2]:
            return True, board[0][0]
        elif board[1][1] !=  symb.symbolDef and board[1][1] == board[0][2] and board[0][2] == board[2][0]:
            return True, board[1][1]
    if board[0][0] !=  symb.symbolDef and board[1][0] !=  symb.symbolDef and board[2][0] !=  symb.symbolDef and board[1][0] !=  symb.symbolDef and board[1][
        1] !=  symb.symbolDef and board[1][2] !=  symb.symbolDef and board[2][0] !=  symb.symbolDef and board[2][1] !=  symb.symbolDef and board[2][2] !=  symb.symbolDef:
        return None, None
    return False, False




def plus_hod():
    global hod
    hod += 1

def chat(message,ai,player):
    board = [[symb.symbolDef] * 3 for i in range(3)]
    hod = 0
    keyboard = types.InlineKeyboardMarkup(row_width=3)
    b1 = types.InlineKeyboardButton(text=symb.symbolDef, callback_data=1)
    b2 = types.InlineKeyboardButton(text=symb.symbolDef, callback_data=2)
    b3 = types.InlineKeyboardButton(text=symb.symbolDef, callback_data=3)
    b4 = types.InlineKeyboardButton(text=symb.symbolDef, callback_data=4)
    b5 = types.InlineKeyboardButton(text=symb.symbolDef, callback_data=5)
    b6 = types.InlineKeyboardButton(text=symb.symbolDef, callback_data=6)
    b7 = types.InlineKeyboardButton(text=symb.symbolDef, callback_data=7)
    b8 = types.InlineKeyboardButton(text=symb.symbolDef, callback_data=8)
    b9 = types.InlineKeyboardButton(text=symb.symbolDef, callback_data=9)
    keyboard.add(b1, b2, b3, b4, b5, b6, b7, b8, b9)
    if bot_send:
        make_bot_false()
        us1_mes = bot.send_message(message.chat.id, 'Играйте! Ты - крестик! Ты  играешь против бота Гринч', reply_markup=keyboard)
        # bot.register_next_step_handler(us1_mes,newgame_command)


