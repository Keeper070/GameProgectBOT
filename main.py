
import telebot
import requests
import datetime

from telebot import types

import symbols as symb
import answers as ans
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from random import random

#Токен бота
bot = telebot.TeleBot('6143676529:AAGMqzKk6wDObeCzMTjLxvoPBv2GLrWRYKQ')
#Токен погоды
open_weather_token ="477235890e9d958619a2fcead20bf9e6"

#Список команд /help
command_list = \
    'Полный список команд:\n' \
    '/register [username] - войти в чат\n' \
    'Вы также можете выбрать или изменить свой псевдоним, введя его после команды\n' \
    'По умолчанию будет использоваться ваше имя\n' \
    '/showusers - показать зарегистрированных пользователей\n' \
    '/message [id/"all"] - написать сообщение пользователю\n' \
    'Для отправки личного сообщения введите id пользователя после команды\n' \
    'Для отправки всеобщего сообщения напишите "all" без кавычек после команды\n' \
    '/newgame - начать новую игру (Пока в разработке)\n' \
    '/weather - узнать погоду в своем городе \n'\
    '/time -узнать текущее время \n'\
    '/quit - выйти из чата\n' \
    '\n'\
    'P.S: Чтобы не вводить команду на клавиатуре, просто нажмите на нее'

#Словарь ответов на некоторые сообщения
dictionaryAnswer={
    "Привет бот: " :"Привет!",
    "Привет Гринч" : "Привет",
    "Как дела?" : "Нормально. Как у вас?",
    "Как дела Гринч?" : "Хорошо :)",
    "Что ты умеешь?" : "Я умею много чего, лучше посмотри список команд (/help)",
    "Пока бот" : "Счастливо!",
    "Пока" : "Пока :(",
    "Пока Гринч" : "Пока"
}


registered_users: {int: str} = {}

# Команда приветствия
@bot.message_handler(commands=['start'])
def start_command(message):
    bot.send_message(
        message.from_user.id,
        'Привет.Это Бот Гринч,я пока что нахожусь на обучении, но уже знаю парочку команд\n' +
        'Если ты хочешь узнать список команд отправь сообщение /help')

# Команда получения списка команд
@bot.message_handler(commands=['help'])
def start_command(message):
    bot.send_message(message.from_user.id, command_list)

# Команда регистрации в чате
@bot.message_handler(commands=['register'])
def register_command(message: telebot.types.Message):
    user_input = message.text.split()
    # То, что ввел пользователь после команды, если что-то вообще ввел, иначе его имя
    username = user_input[1] if len(user_input) > 1 else message.from_user.first_name
    registered_users[message.from_user.id] = username
    bot.send_message(message.from_user.id, 'Вы вошли в чат как ' + username)

# Команда получения списка пользователей
@bot.message_handler(commands=['showusers'])
def show_users_command(message: telebot.types.Message):
    # Если список пуст
    if len(registered_users.values()) == 0:
        bot.send_message(message.from_user.id, 'В чате пока никого нет')
        return
    output = ''
    # Составляем список всех участников
    for registered_user in registered_users.items():
        output += registered_user[1] + '\\[`' + str(registered_user[0]) + '`]' + '\n'
    bot.send_message(message.from_user.id, output, parse_mode='Markdown')

# Команда отправки сообщения
@bot.message_handler(commands=['message'])
def tell_command(message: telebot.types.Message):
    # Если пользователь ещё не зашел
    if message.from_user.id not in registered_users.keys():
        bot.send_message(
            message.from_user.id,
            'Вы ещё не вошли в чат, пожалуйста, войдите, используя команду /register')
        return
    # Разбиваем ввод пользователя на команду + адресат + текст
    user_input = message.text.split(maxsplit=2)
    if len(user_input) < 2:
        bot.send_message(message.from_user.id, 'Введите пользователя')
        return
    addressee = user_input[1]
    username = registered_users[message.from_user.id]
    # Если хочет отправить всеобщее сообщение
    if len(user_input) < 3:
        bot.send_message(message.from_user.id, 'Введите текст сообщения')
        return
    if addressee.lower() == 'all':
        for target_user_id in registered_users.keys():
            bot.send_message(target_user_id, username + ': ' + user_input[2])
        return
    # Если хочет отправить личное сообщение
    if addressee.isdecimal():
        target_id = int(addressee)
        if target_id in registered_users.keys():
            bot.send_message(target_id, username + ': ' + user_input[2])
            return
    # Если что-то не то ввёл
    bot.send_message(
        message.from_user.id,
        'Пользователь не найден'
        'Если вы хотите отправить сообщение, которое увидят все пользователи введите "all" после команды')

# Команда выхода из чата
@bot.message_handler(commands=['quit'])
def quit_command(message: telebot.types.Message):
    # Если пытается выйти из чата, не заходя в него
    if message.from_user.id not in registered_users:
        bot.send_message(message.from_user.id, 'Вы ещё не входили в чат')
        return
    # Если нормально выходит
    else:
        registered_users.pop(message.from_user.id)
        bot.send_message(message.from_user.id, 'Вы вышли из чата')


# Команда погоды
@bot.message_handler(commands=['weather'])
def weather_command(message: telebot.types.Message):
    msg=bot.send_message(message.from_user.id, "Введите название города:")
    bot.register_next_step_handler(msg,getWeather)

#Получение погоды
def getWeather(message):

    city=message.text
    #Словарь сиволов для красивой информации о погоде
    dictionaryCodeToSmile = {
        "Clear": "Ясно ☀",
        "Clouds": "Облачно 🌥",
        "Rain": "Дождь 🌧",
        "Thunderstorm": "Гроза ⚡",
        "Drizzle": "Морось 💧",
        "Snow": "Снег ❄",
        "Mist": "Туман 🌫"

    }
    try:
            req=requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={open_weather_token}&units=metric")
            data=req.json()

            # Перебор словаря
            weatherSmile = data["weather"][0]["main"]
            if weatherSmile in dictionaryCodeToSmile:
                ws = dictionaryCodeToSmile[weatherSmile]
            else:
                ws = 'Не могу понять что там, выгляни в окно'

            city=data["name"]
            weatherNow= data["main"]["temp"]
            weatherMax=data["main"]["temp_max"]
            weatherMin=data["main"]["temp_min"]
            humidity=data["main"]["humidity"]
            wind=data["wind"]["speed"]
            sunrise=datetime.datetime.fromtimestamp(data["sys"]["sunrise"])
            sunset = datetime.datetime.fromtimestamp(data["sys"]["sunset"])

            bot.send_message(message.from_user.id,f'Погода в городе: {city}\n'
                  f'Температура воздуха сейчас: {weatherNow} C° {ws}\n'
                  f'Максимальная температура воздуха за день: {weatherMax} C°\n'
                  f'Минимальная температура воздуха за день: {weatherMin} C°\n'
                  f'Влажность: {humidity} %\n'
                  f'Скорость ветра: {wind} м/c\n'
                  f'Рассвет: {sunrise}\n'
                  f'Закат: {sunset}\n'
                  f'Продуктивного вам дня'
                  )
    except Exception as ex:
        if(message.text[:1] == '/'):
            bot.send_message(message.from_user.id, 'Возможно вы случайно ввели команду, если нет, то повторите ее еще раз')
        else:
          while message.text[:1] != '/':
            msg = bot.send_message(message.from_user.id, 'Проверьте правильность введенного города и введите название города повторно')
            bot.register_next_step_handler(msg, getWeather)
            break


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


#Команда текущего времени
@bot.message_handler(commands=['time'])
def time_command(message: telebot.types.Message):
    bot.send_message(message.from_user.id, "Текущее время в твоем городе : \n"
                                f"---{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}---")


# Точка входа
def main():
    bot.infinity_polling()

#Запуск
main()