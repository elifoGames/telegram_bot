import telebot
import json
import os

from telebot import types

bot = telebot.TeleBot('5718250559:AAH9ReiCcFkejXublomPW_TWuUDYyN181sQ')

#@bot.message_handler()
#def ivan(message):
#    bot.send_message(6237634317, message.text)

@bot.message_handler(commands=["start"])
def start(message):
    if message.from_user.language_code == "ru":
        mess = f"Добрый день, <b>{message.from_user.first_name}</b>. Этот бот запоминает каждое отправленное ему сообщение. Администратор бота(владелец ElifoGames) имеет доступ к сообщениям. Прочитать все сообщения: /read, Очистить все сообщения /clean"
    else:
        mess = f"Hello, <b>{message.from_user.first_name}</b>. This bot remembers every message sent to it. Bot's administrator (ElifoGames owner) has access to messages. Read all messages: /read, Clean all messages /clear"
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    start = types.KeyboardButton('/start')
    read = types.KeyboardButton('/read')
    clean = types.KeyboardButton('/clear')
    ban = types.KeyboardButton('/ban')
    unban = types.KeyboardButton('/unban')
    read_alien = types.KeyboardButton('/read_alien')
    with open("admins.json", "r") as infile:
        admins = json.load(infile)
    if message.from_user.id in admins or message.from_user.username in admins:
        markup.add(start, read, clean, ban, unban, read_alien)
    else:
        markup.add(start, read, clean)

    bot.send_message(message.chat.id, mess, parse_mode="html", reply_markup = markup)

@bot.message_handler(commands=["clear"])
def read(message):
    file_name = str(message.from_user.id) + ".json"
    if os.path.exists(file_name):
        os.remove(file_name)
    if message.from_user.language_code == "ru":
        mess = f"История очищена..."
    else:
        mess = f"History cleared..."
    bot.send_message(message.chat.id, mess)

@bot.message_handler(commands=["read"])
def read(message):
    file_name = str(message.from_user.id) + ".json"
    if os.path.exists(file_name):
        with open(file_name, "r") as infile:
            data = json.load(infile)
    else:
        data = {}
    if message.from_user.language_code == "ru":
        mess = f"Список запросов: {str(list(data.values()))}"
    else:
        mess = f"List of requites: {str(list(data.values()))}"
    bot.send_message(message.chat.id, str(list(data.values())))

@bot.message_handler(commands=["ban"])
def ban(message):
    with open("admins.json", "r") as infile:
        admins = json.load(infile)
    if message.from_user.id in admins or message.from_user.username in admins:
        with open("banned_accounts.json", "r") as infile:
            ban = json.load(infile)

        ban[message.text.lstrip('/ban ')] = ""

        with open("banned_accounts.json", "w") as outfile:
            json.dump(ban, outfile)
        if message.from_user.language_code == "ru":
            mess = f"{message.text.lstrip('/ban ')} забанен"
        else:
            mess = f"{message.text.lstrip('/ban ')} is banned"
        bot.send_message(message.chat.id, mess)
    else:
        if message.from_user.language_code == "ru":
            mess = f"Вы не админ."
        else:
            mess = f"You are not an admin."
        bot.send_message(message.chat.id, mess)

@bot.message_handler(commands=["unban"])
def unban(message):
    with open("admins.json", "r") as infile:
        admins = json.load(infile)
    if message.from_user.id in admins or message.from_user.username in admins:
        with open("banned_accounts.json", "r") as infile:
            ban = json.load(infile)
        ban[message.text.lstrip('/unban ')] = ""
        del ban[message.text.lstrip('/unban ')]

        with open("banned_accounts.json", "w") as outfile:
            json.dump(ban, outfile)
        
        if message.from_user.language_code == "ru":
            mess = f"{message.text.lstrip('/unban ')} разбанен"
        else:
            mess = f"{message.text.lstrip('/unban ')} is unbanned"
        
        bot.send_message(message.chat.id, mess)
        bot.send_message(message.text.lstrip('/unban '), mess)
    else:
        if message.from_user.language_code == "ru":
            mess = f"Вы не админ."
        else:
            mess = f"You are not an admin."
        bot.send_message(message.chat.id, mess)

@bot.message_handler(commands=["read_alien"])
def read(message):
    with open("admins.json", "r") as infile:
        admins = json.load(infile)
    if message.from_user.id in admins or message.from_user.username in admins:
        file_name = str(message.text.lstrip('/read_alien ')) + ".json"
        if os.path.exists(file_name):
            with open(file_name, "r") as infile:
                data = json.load(infile)
        else:
            data = {}
        if message.from_user.language_code == "ru":
            mess = f"Список запросов: {str(list(data.values()))}"
        else:
            mess = f"List of requites: {str(list(data.values()))}"
        bot.send_message(message.chat.id, str(list(data.values())))

@bot.message_handler()
def text(message):
    with open("banned_accounts.json", "r") as infile:
        ban = json.load(infile)
    if message.from_user.id not in ban and message.from_user.username not in ban:
        file_name = str(message.from_user.id) + ".json"
        if os.path.exists(file_name):
            with open(file_name, "r") as infile:
                data = json.load(infile)
        else:
            data = {"first_name": message.from_user.first_name, "last_name": message.from_user.last_name, "nicname": message.from_user.username}
        data[message.id] = message.text
        with open(file_name, "w") as outfile:
            json.dump(data, outfile)
        if message.from_user.language_code == "ru":
            mess = f"Хорошо, ваш запрос: {message.text}"
        else:
            mess = f"Ok, your request: {message.text}"
        bot.send_message(message.chat.id, mess)
    else:
        if message.from_user.language_code == "ru":
            bot.send_message(message.chat.id, "Вы были заблокированы.")
        else:
            bot.send_message(message.chat.id, "You have been blocked.")

bot.polling(none_stop=True)