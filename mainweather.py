import requests
import datetime
import telebot
#для красивого вывода в print'е
from pprint import pprint

#Токен погоды
open_weather_token ="477235890e9d958619a2fcead20bf9e6"
#Токен бота
bot = telebot.TeleBot('6143676529:AAGMqzKk6wDObeCzMTjLxvoPBv2GLrWRYKQ')


#Получение погоды
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
        bot.send_message(message.from_user.id,'Проверьте правильность введенного города')



