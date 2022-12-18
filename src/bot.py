import telebot
from geopy import geocoders
import requests
import datetime
from telebot import types

# emoji
cityscape = "🏙"
sun = "☀"
thermometr = '🌡'
umbrella = '☂'
wave_hand = '👋'
calendar = '📅'
data_all = {'user_id': '00000'}
degree_sign = u'\N{DEGREE SIGN}'

def geo_pos(city: str):
    geolocator = geocoders.Nominatim(user_agent="telebot")
    location = geolocator.geocode(city)
    latitude = str(location.latitude)
    longitude = str(location.longitude)
    return latitude, longitude


def get_weather(city: str):
    res = requests.get("http://api.openweathermap.org/data/2.5/find",
                       params={'lat': str(geo_pos(city)[0]), 'lon': str(geo_pos(city)[1]),
                               'type': 'like', 'units': 'metric', 'APPID': "aee03afe0ed04072dcaf918fcf3ba110",
                               'lang': 'ru'})
    data = res.json()
    return data


def give_weather_now(city: str):
    data = get_weather(city)
    degree_sign = u'\N{DEGREE SIGN}'
    main_data = data['list'][0]
    data_final = {}
    data_final['temp_real'] = str(main_data['main']['temp'])
    data_final['temp_feels'] = str(main_data['main']['feels_like'])
    data_final['pressure'] = str(round(main_data['main']['pressure'] * 100 / 101325 * 760))
    data_final['humidity'] = str(main_data['main']['humidity']) + '%'
    data_final['wind_speed'] = str(main_data['wind']['speed'])
    wind_degree_to_count = main_data['wind']['deg']
    if (337.5 <= wind_degree_to_count <= 360) or (0 <= wind_degree_to_count <= 22.5):
        data_final['wind_degree'] = 'северный'
    elif 22.5 < wind_degree_to_count < 67.5:
        data_final['wind_degree'] = 'северо-восточный'
    elif 67.5 <= wind_degree_to_count <= 112.5:
        data_final['wind_degree'] = 'восточный'
    elif (112.5 < wind_degree_to_count < 157.5):
        data_final['wind_degree'] = 'юго-восточный'
    elif (157.5 <= wind_degree_to_count <= 202.5):
        data_final['wind_degree'] = 'южный'
    elif (202.5 < wind_degree_to_count < 247.5):
        data_final['wind_degree'] = 'юго-западный'
    elif (247.5 <= wind_degree_to_count <= 292.5):
        data_final['wind_degree'] = 'западный'
    else:
        data_final['wind_degree'] = 'северо-западный'
    data_final['rain'] = main_data['rain']
    data_final['snow'] = main_data['snow']
    data_final['description'] = main_data['weather'][0]['description']
    return data_final


def get_weather_days(city: str):
    res = requests.get("http://api.openweathermap.org/data/2.5/forecast",
                       params={'lat': str(geo_pos(city)[0]), 'lon': str(geo_pos(city)[1]),
                               'type': 'like', 'units': 'metric', 'APPID': "aee03afe0ed04072dcaf918fcf3ba110",
                               'lang': 'ru'})
    data = res.json()
    return data


def give_weather_days(city: str):
    data = get_weather_days(city)
    main_data = data['list']
    data_final = {'day0': {}, 'day1': {}, 'day2': {}, 'day3': {}, 'day4': {}}
    degree_sign = u'\N{DEGREE SIGN}'
    for i in range(0, len(main_data), 8):
        data_final[f'day{str(i // 8)}']['temp_real'] = str(main_data[i]['main']['temp'])
        data_final[f'day{str(i // 8)}']['temp_feels'] = str(main_data[i]['main']['feels_like'])
        data_final[f'day{str(i // 8)}']['pressure'] = str(round(main_data[i]['main']['pressure'] * 100 / 101325 * 760))
        data_final[f'day{str(i // 8)}']['humidity'] = str(main_data[i]['main']['humidity']) + '%'
        data_final[f'day{str(i // 8)}']['wind_speed'] = str(main_data[i]['wind']['speed'])
        wind_degree_to_count = main_data[i]['wind']['deg']
        if (337.5 <= wind_degree_to_count <= 360) or (0 <= wind_degree_to_count <= 22.5):
            data_final[f'day{str(i // 8)}']['wind_degree'] = 'северный'
        elif (22.5 < wind_degree_to_count < 67.5):
            data_final[f'day{str(i // 8)}']['wind_degree'] = 'северо-восточный'
        elif (67.5 <= wind_degree_to_count <= 112.5):
            data_final[f'day{str(i // 8)}']['wind_degree'] = 'восточный'
        elif (112.5 < wind_degree_to_count < 157.5):
            data_final[f'day{str(i // 8)}']['wind_degree'] = 'юго-восточный'
        elif (157.5 <= wind_degree_to_count <= 202.5):
            data_final[f'day{str(i // 8)}']['wind_degree'] = 'южный'
        elif (202.5 < wind_degree_to_count < 247.5):
            data_final[f'day{str(i // 8)}']['wind_degree'] = 'юго-западный'
        elif (247.5 <= wind_degree_to_count <= 292.5):
            data_final[f'day{str(i // 8)}']['wind_degree'] = 'западный'
        else:
            data_final[f'day{str(i // 8)}']['wind_degree'] = 'северо-западный'
        data_final[f'day{str(i // 8)}']['description'] = main_data[i]['weather'][0]['description']
    return data_final


def print_weather_now(city: str):
    data = give_weather_now(city)
    precipitation = ''
    if (data['rain'] == None) and (data['snow'] == None):
        precipitation = 'Осадков нет'
    elif data['rain'] != None:
        precipitation = 'Идет дождь'
    else:
        precipitation = 'Идет снег'
    result = f'Погода в городе {city.title()} сейчас: \n' \
             f'На улице {data["description"]}\n' \
             f'Температура воздуха {round(float(data["temp_real"]))}{degree_sign}C, ощущается как {round(float(data["temp_feels"]))} {degree_sign}C \n' \
             f'Ветер {data["wind_degree"]}, {round(float(data["wind_speed"]))} м/с \n' \
             f'Атмосферное давление {data["pressure"]} мм рт.ст. \n' \
             f'Влажность воздуха {data["humidity"]}'

    return result


def print_weather_days(city: str):
    data = give_weather_days(city)
    first = datetime.date.today()
    days = ['Сегодня', 'Завтра']
    for i in range(2, 5):
        days.append(
            str((first + datetime.timedelta(days=i)).day) + '.' + str((first + datetime.timedelta(days=i)).month))
    result = [0, 0, 0, 0, 0]
    for i in range(len(days)):
        result[i] = f'{calendar}{days[i]}: {data[f"day{i}"]["description"]} \n' \
                    f'температура {round(float(data[f"day{i}"]["temp_real"]))}{degree_sign}C \n' \
                    f'ощущается как {round(float(data[f"day{i}"]["temp_feels"]))}{degree_sign}C \n' \
                    f'ветер {data[f"day{i}"]["wind_degree"]}, {round(float(data[f"day{i}"]["wind_speed"]))} м/с \n' \
                    f'влажность {data[f"day{i}"]["humidity"]}\n' \
                    f'атмосферное давление {data[f"day{i}"]["pressure"]} мм рт.ст.'
    new_result = '\n\n'.join(result)

    return new_result


def print_tips(city: str):
    data_for_tips = give_weather_now(city)
    result = ''
    if data_for_tips['rain'] != None:
        result += 'Возьмите зонтик, на улице дождь \n'
    if (5 <= float(data_for_tips['wind_speed']) < 10) and (float(data_for_tips['temp_real']) < 10):
        result += 'На улице ветрено, наденьте шарф \n'
    if float(data_for_tips['wind_speed']) >= 10:
        result += 'На улице сильный ветер, будьте осторожны \n'
    if float(data_for_tips['pressure']) < 750:
        result += 'Атмосферное давление низкое, возможно ухудшение самочувствия \n'
    if float(data_for_tips['pressure']) > 770:
        result += 'Атмосферное давление высокое, возможно ухудшение самочувствия'
    return result


TOKEN = '5871029941:AAH15Zi9tFkwEZft9GSvj3a-dKNo6P0VWDE'
weather_id = "aee03afe0ed04072dcaf918fcf3ba110"
bot = telebot.TeleBot(TOKEN)
data = {}


@bot.message_handler(commands=['start', 'help', 'tips'])
def command_answers(message):
    if message.text == '/start':
        bot.send_message(message.from_user.id,wave_hand)
        bot.send_message(message.from_user.id,
                         "Привет! Этот бот умеет отображать погоду в любом городе мира \n"
                         "Чтобы ознакомиться с тем, как он работает, введите /help ")
        data_all[str(message.from_user.id)] = {'city': '', 'tips': True }
    if message.text == '/help':
        bot.send_message(message.from_user.id,
                         f'{cityscape} Чтобы получить данные по погоде в интересующем вас городе, отправьте боту его название. \n '
                         f'{sun} Вам будет предложено выбрать, хотите вы получить погоду в городе в данный момент '
                         f'времени '
                         'или на следующие 5 дней.\n'
                         f'{umbrella} Также бот умеет давать рекомендации, по тому как одеваться и как надо себя вести при определенной погоде. Если вы хотите отключить эту функцию, отправьте боту сообщение /tips'
                         )
    if message.text == '/tips':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Да")
        btn2 = types.KeyboardButton("Нет")
        markup.add(btn1, btn2)
        bot.send_message(message.from_user.id, "Хотите ли вы получать рекомендации от бота?".format(message.from_user), reply_markup=markup)

@bot.message_handler(content_types=['text'])
def send_weather(message):
    try:
        geolocator = geocoders.Nominatim(user_agent="telebot")
        location = geolocator.geocode(message.text)
        if message.text == 'Погода сейчас':
            markup = telebot.types.ReplyKeyboardRemove()
            s = print_tips(data_all[str(message.from_user.id)]['city'])
            bot.send_message(message.from_user.id, print_weather_now(data_all[str(message.from_user.id)]['city']), reply_markup = markup)
            if data_all[str(message.from_user.id)]['tips'] == True and s != '':
                bot.send_message(message.from_user.id, s)
        elif message.text == 'Прогноз на 5 дней':
            markup = telebot.types.ReplyKeyboardRemove()
            result = print_weather_days(data_all[str(message.from_user.id)]['city'])
            bot.send_message(message.from_user.id, result, reply_markup=markup)
        elif message.text == 'Да':
            markup = telebot.types.ReplyKeyboardRemove()
            data_all[str(message.from_user.id)]['tips'] = True
            bot.send_message(message.from_user.id, 'Рекомендации включены', reply_markup=markup)
        elif message.text == 'Нет':
            markup = telebot.types.ReplyKeyboardRemove()
            data_all[str(message.from_user.id)]['tips'] = False
            bot.send_message(message.from_user.id, 'Рекомендации выключены', reply_markup=markup)
        elif location != None:
            data_all[str(message.from_user.id)]['city'] = message.text
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = types.KeyboardButton("Погода сейчас")
            btn2 = types.KeyboardButton("Прогноз на 5 дней")
            markup.add(btn1,btn2)
            bot.send_message(message.from_user.id, 'Какой прогноз вы хотите увидеть?'.format(message.from_user), reply_markup=markup)
        else:
            bot.send_message(message.from_user.id, 'Я не знаю такого города, попробуйте еще раз')
    except:
        markup = telebot.types.ReplyKeyboardRemove()
        bot.send_message(message.from_user.id, 'Что-то пошло не так, попробуйте перезапустить бота с помощью команды /start', reply_markup = markup)


bot.polling(none_stop=True, interval=0)
