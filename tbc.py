import telebot
import json
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


