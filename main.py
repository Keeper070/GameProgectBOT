
import telebot
import requests
import datetime

from telebot import types

import symbols as symb
import answers as ans
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import random

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

#Игра крестики нолики

winbool = False
losebool = False
drawbool=False

#Словарь доски, где хранится кнопка и ее callback data
board={}

#Поле
ground = [" ", " ", " ",
          " ", " ", " ",
          " ", " ", " ", ]

player_symbol='x'
ai_symbol='0'

#Функция победы
def win(cell_1, cell_2, cell_3):
    if cell_1 == player_symbol and cell_2 == player_symbol and cell_3 == player_symbol:
        print("win")
        global winbool
        winbool = True

#Функция поражения
def lose(cell_1, cell_2, cell_3):
    if cell_1 == ai_symbol and cell_2 == ai_symbol and cell_3 == ai_symbol:
        print("lose")
        global losebool
        losebool = True

#Функция с ничьей
def draw(cell_1, cell_2, cell_3,cell_4, cell_5, cell_6,cell_7, cell_8, cell_9):
    if cell_1 != ai_symbol and cell_2 != ai_symbol and cell_3 != ai_symbol and cell_4 != ai_symbol and cell_5 != ai_symbol and cell_6 != ai_symbol and  cell_7 != ai_symbol and cell_8 != ai_symbol and cell_9 != ai_symbol:
        if cell_1 != player_symbol and cell_2 != player_symbol and cell_3 != player_symbol and cell_4 != player_symbol and cell_5 != player_symbol and cell_6 != player_symbol and  cell_7 != player_symbol and cell_8 != player_symbol and cell_9 != player_symbol:
            print("draw")
            global drawbool
            drawbool = True
#Функция очистки поля
def clear():
    global ground
    ground = [" ", " ", " ",
              " ", " ", " ",
              " ", " ", " ", ]

#Выбор игры (крестик или нолик)
@bot.message_handler(commands=['newgame'])
def newgame_command(message: telebot.types.Message):

  board = {}
  bot.send_message(message.chat.id, "Игра началась")

  #Создаем клавиатуру
  global keyboard
  keyboard=types.InlineKeyboardMarkup(row_width=3)

  #Добавляем в словарь доски кнопки клавиатуры
  for i in range(9):
      board[i] = types.InlineKeyboardButton(ground[i], callback_data=str(i))

  keyboard.row(board[0], board[1], board[2])
  keyboard.row(board[3], board[4], board[5])
  keyboard.row(board[6], board[7], board[8])
  #Отрисовываем кнопки
  bot.send_message(message.chat.id, "Выбери клетку", reply_markup=keyboard)

#Обработка кнопок
@bot.callback_query_handler(func=lambda call: True)
def callbackInline(call):
    if (call.message):
        #Рандомный ход для бота
        random_cell = random.randint(0, 8)
        if ground[random_cell] == player_symbol:
            random_cell = random.randint(0, 8)
        if ground[random_cell] == ai_symbol:
            random_cell = random.randint(0, 8)
        if ground[random_cell] == " ":
            ground [random_cell] = ai_symbol
        # Ход игрока
        for i in range(9):
            if call.data == str(i):
                if (ground[i] == " "):
                    ground[i] = player_symbol

            #Проверка на победу игрока
            win(ground[0], ground[1], ground[2])
            win(ground[3], ground[4], ground[5])
            win(ground[6], ground[7], ground[8])
            win(ground[0], ground[3], ground[6])
            win(ground[1], ground[4], ground[7])
            win(ground[2], ground[5], ground[8])
            win(ground[0], ground[4], ground[8])
            win(ground[6], ground[4], ground[2])
            #Проверка на поражение игрока
            lose(ground[0], ground[1], ground[2])
            lose(ground[3], ground[4], ground[5])
            lose(ground[6], ground[7], ground[8])
            lose(ground[0], ground[3], ground[6])
            lose(ground[1], ground[4], ground[7])
            lose(ground[2], ground[5], ground[8])
            lose(ground[0], ground[4], ground[8])
            lose(ground[6], ground[4], ground[2])
            #Ничья
            draw(ground[0], ground[1], ground[2],
                 ground[3], ground[4], ground[5],
                 ground[6], ground[7], ground[8])

            #Добавление новой кнопки
            board[i] = types.InlineKeyboardButton(ground[i], callback_data=str(i))

        keyboard = types.InlineKeyboardMarkup(row_width=3)
        keyboard.row(board[0], board[1], board[2])
        keyboard.row(board[3], board[4], board[5])
        keyboard.row(board[6], board[7], board[8])
        #Замена предыдущего сообщения(клава) бота на вновь пересозданную
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Я сходил.Теперь твой ход",
                              reply_markup=keyboard)
        #Если игрок победил
        global winbool
        if winbool:
            clear()
            bot.send_message(call.message.chat.id, "Я проиграл 😞. Эх, все-таки ты обыграл меня. Если хочешь сыграть еще раз введи команду /newgame")
            winbool = False

        #Если игрок проиграл
        global losebool
        if losebool:
            clear()
            bot.send_message(call.message.chat.id, "Я выиграл  😀. Если хочешь сыграть еще раз введи команду /newgame")
            losebool = False
        #Если ничья
        global drawbool
        if drawbool:
            clear()
            bot.send_message(call.message.chat.id, "Ого! У нас ничья! В следующий раз постораюсь отыграться  😉. Если хочешь сыграть еще раз введи команду /newgame")
            drawbool=False


# Точка входа
def main():
    bot.polling()

#Запуск
main()