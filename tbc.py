import telebot
import json
from datetime import date, time, datetime, timedelta
from telebot import types
TOKEN = '8164438665:AAFYA9aYE4Z8lGDVzT3bbseQevmXQ8V2QOw'
bot = telebot.TeleBot(TOKEN)
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, 'Бот для записи на процедуры запущен')




def add_appointment(date, time, client):
    try:
        with open('data.json', 'r', encoding='utf-8') as file:
            data = json.load(file)
    except FileNotFoundError:
        data = {"appointments": [], "review": []}
    new_appointment = {'date': date, 'time': time, 'client': client}
    data['appointments'].append(new_appointment)
    with open('data.json', 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

def add_review(client, text):
    try:
        with open('data.json', 'r', encoding='utf-8') as file:
            data1 = json.load(file)
    except FileNotFoundError:
        data1 = {"appointments": [], "review": []}
    review1 = {'client': client, 'text': text}
    data1['review'].append(review1)
    with open('data.json', 'w', encoding='utf-8') as file:
        json.dump(data1, file, ensure_ascii=False, indent=4)


@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    bot.send_message(call.message.chat.id, 'Выберите время:', reply_markup=generate_keyboard_time())


def generate_keyboard():
    keyboard = types.InlineKeyboardMarkup()
    tday = date.today()
    days =[]
    for i in range (7):
        ndate = tday + timedelta(days= 3+i)
        days.append(ndate)


    for button_text in days:
        button = types.InlineKeyboardButton(text=button_text, callback_data = f"day:{button_text}")
        keyboard.add(button)
    return keyboard

def generate_keyboard_time():
    keyboard = types.InlineKeyboardMarkup()
    time = ["10:00", "12:00", "15:00", "17:00"]

    for button_text_t in time:
        button = types.InlineKeyboardButton(text=button_text_t, callback_data = f"meeting:{button_text_t}")
        keyboard.add(button)
    return keyboard

@bot.message_handler(commands=['make_an_appointment'])
def make_an_appointment(message):
    show_dates(message.chat.id)



@bot.message_handler(commands=['show_dates'])
def show_dates(message):
    bot.send_message(message.chat.id, 'Выберите день:', reply_markup=generate_keyboard())



