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

player=0
ai=0

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
       msg= bot.send_message(callback_query.message.chat.id,'Отличный выбор!Давай начнем')
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


# #Оценка состояния
# def score(board):
#     if win(board,player):
#         return -10
#     elif win(board,ai):
#         return 10
#     else:
#         return 0

 def init_board(self):
     self.board = ['  '] * 10


def get_board(self):
     return self.board

def get_drawn_board(self, board):
        row_0 = '✎\n'
        row_1 = self.board[7] + '|' + self.board[8] + '|' + \
            self.board[9] + '\n'
        row_2 = '--+--+--\n'
        row_3 = self.board[4] + '|' + self.board[5] + '|' + \
            self.board[6] + '\n'
        row_4 = '--+--+--\n'
        row_5 = self.board[1] + '|' + self.board[2] + '|' + \
            self.board[3] + '\n'

        drawn_board = row_0 + row_1 + row_2 + row_3 + row_4 + row_5

        return drawn_board