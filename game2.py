import random

from telebot import TeleBot, types

import config

bot = telebot.TeleBot('6143676529:AAGMqzKk6wDObeCzMTjLxvoPBv2GLrWRYKQ')

users = {}


@bot.message_handler(commands=['start'])
def start(message: types.Message):
    # Если такой юзер уже есть, то просто игнор
    # иначе создаст для него словарь со стейтом
    users.setdefault(message.from_user.id, {'state': 'game'})
    # по факту команда старт единственный способ начать игру,
    # после кнопки стоп, так что придется сделать  вот так
    # чтобы стейт поменялся
    users[message.from_user.id]['state'] = 'game'
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("Камень", "Ножницы", "Бумага").add("Стоп")
    bot.send_message(message.chat.id, text="Привет", reply_markup=markup)


@bot.message_handler(
    func=lambda message: message.text == "Стоп" and users.get(message.from_user.id, {}).get('state') == 'game')
def stop_game(message: types.Message):
    # Сброс стейта. Так бот не будет реагировать на камень ножницы бумагу
    users[message.from_user.id]['state'] = ''
    wins = users[message.chat.id].get("count_win", 0)
    loses = users[message.chat.id].get("count_lose", 0)
    markup = types.ReplyKeyboardRemove()
    bot.send_message(message.chat.id, text=f'Побед:{wins}\nПроигрышей:{loses}', reply_markup=markup)


# Фильтр таков. Хендлер тригерится только на слова камень ножницы бумага и только если у юзера стейт game
@bot.message_handler(
    func=lambda message: message.text in ['Камень', 'Ножницы', 'Бумага'] and users.get(message.from_user.id, {}).get(
        'state') == 'game')
def game(message: types.Message):
    t_list = ['Камень', 'Ножницы', 'Бумага']

    if users[message.from_user.id].get("count_win") is None:
        users[message.from_user.id]["count_win"] = 0
        users[message.from_user.id]["count_lose"] = 0

    random_answer = random.choice(t_list)
    results = {
        "Камень": "Ножницы",
        "Ножницы": "Бумага",
        "Бумага": "Камень"
    }

    if message.text == random_answer:
        bot.send_message(message.chat.id, text=f'Ничья')

    elif results[message.text] == random_answer:
        bot.send_message(message.chat.id, text=f'ПОБЕЕЕЕЕДАААА!!')
        users[message.from_user.id]["count_win"] += 1
    else:
        bot.send_message(message.chat.id, text=f'ПОРАЖЕНИЕ')
        users[message.from_user.id]["count_lose"] += 1


bot.infinity_polling(skip_pending=True)