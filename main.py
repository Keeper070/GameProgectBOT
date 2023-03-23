
import telebot
import requests
import datetime
import math

from telebot import types

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
          " ", " ", " ",]

#Список крестиков и ноликов
zero_or_x = ["O", "X"]

#Рандомный выбор за кого будет играть игрок
# player_symbol = zero_or_x[random.randint(0, 1)]

# MAX="X"
# #Символ ии
# ai_symbol = ""
#
# if (player_symbol == "X"):
#     ai_symbol = "O"
# else:
#     ai_symbol = "X"

player_symbol = "X"
ai_symbol = "O"

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

#Проверка на ничью
def draw(message):
    if(ground[0] != " " and ground[1] != " " and ground[2] != " " and ground[3] != " " and
       ground[4] != " " and ground[5] != " " and ground[6] != " " and ground[7] != " " and
       ground[8] != " "):
        bot.send_message(message.chat.id,"Ого! У нас ничья! В следующий раз постораюсь отыграться  😉. Если хочешь сыграть еще раз введи команду /newgame")



#Функция с ничьей
def check_draw():
    for i in range(9):
        if (ground[i] == " "):
            return False
        else:
            return True

#Функция очистки поля
def clear():
    global ground
    ground = [" ", " ", " ",
              " ", " ", " ",
              " ", " ", " ", ]

# Инициализация победных линий
victories = [[0,1,2],
             [3,4,5],
             [6,7,8],
             [0,3,6],
             [1,4,7],
             [2,5,8],
             [0,4,8],
             [2,4,6]]

#Выбор игры (крестик или нолик)
@bot.message_handler(commands=['newgame'])
def newgame_command(message: telebot.types.Message):
  #Если вдруг доска не очистилась, то при вводе команды очищаем список
  if (message.text[:1] == '/'):
    clear()

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
        # Ход игрока
        for i in range(9):
            if call.data == str(i):
                if (ground[i] == " "):
                        ground[i] = player_symbol
                else:
                    bot.send_message(call.message.chat.id, "Эта клетка уже занята, выберите другую:")
                    return callbackInline

        # Добавление новой кнопки
        for i in range(9):
            board[i] = types.InlineKeyboardButton(ground[i], callback_data=str(i))

        #Ход бота(рандомный)
        # random_go()

        # Xol АИ
        #Проверки
        if (ground[4] == player_symbol and ground[0] == " " and ground[5] == " "):
            ground[0] = ai_symbol
        elif (ground[2] == player_symbol and ground[1] == " " and ground[4] == " " and ground[5] == " "):
            ground[4] = ai_symbol
        elif (ground[3] == player_symbol and ground[4] == player_symbol and ground[5] == " "):
            ground[5] = ai_symbol
            # elif (ground[6] == player_symbol or ground[8]== player_symbol and ground[4] == " " and ground[7] == player_symbol):
            #     ground[4] = ai_symbol
        elif (ground[4] == player_symbol and ground[8] == player_symbol and ground[0] == " " and ground[8] == " "):
            ground[0] = ai_symbol
        elif (ground[6] == " " and ground[7] == player_symbol and ground[8] == player_symbol):
            ground[6] = ai_symbol
        elif (ground[6] == player_symbol and ground[7] == player_symbol and ground[8] == " "):
            ground[8] = ai_symbol
        elif (ground[8] == player_symbol and ground[7] == player_symbol and ground[6] == " "):
            ground[6] = ai_symbol
        elif (ground[1] == player_symbol and ground[4] == player_symbol and ground[7] == " "):
            ground[7] = ai_symbol
        elif (ground[0] == player_symbol and ground[4] == " "):
            ground[4] = ai_symbol
        elif (ground[2] == player_symbol and ground[4] == player_symbol and ground[6] == " " and ground[5] == " "):
            ground[6] = ai_symbol
        elif (ground[2] == player_symbol and ground[5] == player_symbol and ground[8] == " "):
            ground[8] = ai_symbol
        elif (ground[0] == player_symbol and ground[3] == player_symbol and ground[6] == " "):
            ground[6] = ai_symbol
        elif (ground[4] == player_symbol and ground[5] == player_symbol and ground[3] == " "):
            ground[3] = ai_symbol
        elif (ground[7] == player_symbol and ground[0] == " " and ground[1] == " " and ground[2] == " " and ground[
            3] == " " and ground[4] == " " and ground[5] == " " and ground[6] == " " and ground[8] == " "):
            ground[4] = ai_symbol
        elif (ground[6] == player_symbol and ground[0] == " " and ground[1] == " " and ground[2] == " " and ground[
            3] == " " and ground[4] == " " and ground[5] == " " and ground[7] == " " and ground[8] == " "):
            ground[4] = ai_symbol
        elif (ground[3] == player_symbol and ground[0] == " " and ground[1] == " " and ground[2] == " " and ground[
            4] == " " and ground[5] == " " and ground[6] == " " and ground[7] == " " and ground[8] == " "):
            ground[4] = ai_symbol
        elif(ground[1] == player_symbol and ground[0] == " " and ground[2] == " " and ground[3] == " " and ground[
            4] == " " and ground[5] == " " and ground[6] == " " and ground[7] == " " and ground[8] == " "):
            ground[4]=ai_symbol
        elif (ground[0] == ai_symbol and ground[1] == " " and ground[2] == " " and ground[3] == " " and ground[
            4] == player_symbol and ground[5] == " " and ground[6] == " " and ground[7] == " " and ground[8] == player_symbol):
            ground[2] = ai_symbol
        #
        else:
         best_spot=minimax(ground,ai_symbol)
         for i in range(9):
            if(best_spot == i):
                if(ground[i] == " "):
                    ground[i] = ai_symbol

        # Добавление новой кнопки
        for i in range(9):
            board[i] = types.InlineKeyboardButton(ground[i], callback_data=str(i))

        # Проверки
        for i in range(9):
            # на победу игрока
            win(ground[0], ground[1], ground[2])
            win(ground[3], ground[4], ground[5])
            win(ground[6], ground[7], ground[8])
            win(ground[0], ground[3], ground[6])
            win(ground[1], ground[4], ground[7])
            win(ground[2], ground[5], ground[8])
            win(ground[0], ground[4], ground[8])
            win(ground[6], ground[4], ground[2])
            # на поражение игрока
            lose(ground[0], ground[1], ground[2])
            lose(ground[3], ground[4], ground[5])
            lose(ground[6], ground[7], ground[8])
            lose(ground[0], ground[3], ground[6])
            lose(ground[1], ground[4], ground[7])
            lose(ground[2], ground[5], ground[8])
            lose(ground[0], ground[4], ground[8])
            lose(ground[6], ground[4], ground[2])
        # на ничью
        draw(call.message)

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


# Рандомный ход для бота
def random_go():
    random_cell = random.randint(0, 8)
    if ground[random_cell] == player_symbol:
        random_cell = random.randint(0, 8)
    if ground[random_cell] == ai_symbol:
        random_cell = random.randint(0, 8)
    if ground[random_cell] == " ":
        ground[random_cell] = ai_symbol

#Возврат индексов пустых клеток доски
def empty_indeces(board):
     list_null_board=[]
     for i in range(9):
         if(board[i] == " "):
             list_null_board.append(i)
     return list_null_board

#Проверка на победу для алгоритма минимакс
def winning(board, player):
  if(
    (board[0] == player and board[1] == player and board[2] == player) or
    (board[3] == player and board[4] == player and board[5] == player) or
    (board[6] == player and board[7] == player and board[8] == player) or
    (board[0] == player and board[3] == player and board[6] == player) or
    (board[1] == player and board[4] == player and board[7] == player) or
    (board[2] == player and board[5] == player and board[8] == player) or
    (board[0] == player and board[4] == player and board[8] == player) or
    (board[2] == player and board[4] == player and board[6] == player)
    ):
      return True
  else :
      return False

#Алгоритм минимакс для АИ
def minimax(board,player):
    global best_move
    #доступные клетки
    avail_spots=empty_indeces(board)
    #Проверка на терминальное состояние(победа, поражение или ничья)
    if(winning(board,player_symbol)):
        return -10
    elif(winning(board,ai_symbol)):
        return 10
    elif(len(avail_spots) == 0):
        return 0

    #Список для хранения индекса на который будем ставить O
    move_win=[]
    #Список для очков каждого хода
    moves=[]
    #Цикл по всем доступным клеткам
    for i in range(len(avail_spots)):
        #Словарь ходов
        move={}
        #Задаем индекс пустой клетки
        move['index']=board[avail_spots[i]]
        #Совершить ход за текущего игрока
        board[avail_spots[i]] = player

        #Получить очки, заработанные после вызова минимакса от противника текущего игрока
        if player == ai_symbol:
            #Результат минимакс
            result=minimax(board,player_symbol)
            #Записываем результат в словарь
            move['score']=result
        else:
            result=minimax(board,ai_symbol)
            move['score'] = result

        #Добавить индекс поля в который будем ходить
        move_win.append(avail_spots[i])
        #Очистить клетку
        board[avail_spots[i]] = move['index']
        #Положить словарь очков в список
        moves.append(move['score'])

        #Если это ход ИИ, пройти циклом по ходам и выбрать ход с наибольшим колличеством очков
        if(player == ai_symbol):
            #Присваиваем очень маленькое число
            best_score=-10000
            #Tсли ход move приносит больше очков, чем bestScore, алгоритм запоминает этот move
            for i in range(len(moves)):
                if(moves[i] > best_score):
                    best_score=moves[i]
                    best_move=i
        #Иначе пройти циклом по ходам и выбрать ход с наименьшим количеством очков
        else:
            best_score=10000
            for i in range(len(moves)):
                if(moves[i]<best_score):
                    best_score=moves[i]
                    best_move=i

    #Вернуть индекс выбранного хода
    return move_win[best_move]

# Точка входа
def main():
    bot.polling()

#Запуск
main()