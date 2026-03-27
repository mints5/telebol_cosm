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
def handle_callback_query(call):
    if call.data.startswith("day:"):
        chosen_date = call.data.split(":")[1]
        bot.send_message(call.message.chat.id, f"Вы выбрали дату: {chosen_date}")
        bot.send_message(call.message.chat.id, 'Выберите время:', reply_markup=generate_keyboard_time(chosen_date))
    if call.data.startswith("appointment:"):
        chosen_time = call.data.split(",")[2]
        chosen_date = call.data.split(":")[1]
        add_appointment(chosen_date, chosen_time, call.message.chat.id)
        bot.send_message(call.message.chat.id, f"ждем вас  {chosen_date} в {chosen_time}")
    if call.data.startswith("noday:"):
        bot.send_message(call.messege.chat.id,'выберите другой день для записи')


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

def generate_keyboard_time(chosen_date):
    keyboard = types.InlineKeyboardMarkup()
    times = ["10:00", "12:00", "15:00", "17:00"]
    with open('data.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
        for i in data['appointments']:
            if i['data'] == chosen_date:
                times.remove(i['time'])
    if not times:
        button = types.InlineKeyboardButton(text='мест не осталось', callback_data = f"noday:{chosen_date}")
        keyboard.add(button)
        return keyboard



    for button_text_t in times:
        button = types.InlineKeyboardButton(text=button_text_t, callback_data = f"appointment, {chosen_date}, {button_text_t}")
        keyboard.add(button)
    return keyboard

@bot.message_handler(commands=['make_an_appointment'])
def make_an_appointment(message):
    show_dates(message)



@bot.message_handler(commands=['show_dates'])
def show_dates(message):
    bot.send_message(message.chat.id, 'Выберите день:', reply_markup=generate_keyboard())

@bot.message_handler(commands=['add_review'])
def add_r(message):
    bot.send_message(message.chat.id, "Напишите отзыв")
    bot.register_next_step_handler(message, add_review)
    add_review(message.chat.id, message.text)

if __name__ == '__main__':
    bot.polling(none_stop=True)


