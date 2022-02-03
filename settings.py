# -*- coding: utf-8 -*-
# bot by w1cee

import json
import telebot

TOKEN = 'TOKEN'
bot = telebot.TeleBot(TOKEN)
LIST_OF_ADMINS = []  # id of users which can change bot settings
json_file = 'config.json'


@bot.message_handler(commands=['view'])
def statistic(message):
    data = json.load(open(json_file, 'r'))
    list_users = data['name']
    list_users = ' '.join(list_users)
    remind_message = data['text']
    remind_message = ''.join(remind_message)
    day_status = data['day_status']
    day_time = data['day_time']
    bot.send_message(message.chat.id, f'Reminder text:\n'
                                      f'{remind_message}\n'
                                      f'\n'
                                      f'List of users: {list_users}\n'
                                      f'\n'
                                      f'Status of days on/off: {day_status}\n'
                                      f'\n'
                                      f'Time of every day: {day_time}'
                     )


@bot.message_handler(commands=['help'])
def help_command(message):
    bot.send_message(message.chat.id, '/add add user to list\n'
                                      '/del delete user from list\n'
                                      '/day_on enable reminder for the day of the week\n'
                                      '/day_off turn off the reminder for the day of the week\n'
                                      '/settime set the time for the day of the week\n'
                                      '/settext set reminder text\n'
                                      '/view current bot settings'
                     )


@bot.message_handler(commands=['settext'])
def text(message):
    if message.from_user.id in LIST_OF_ADMINS:
        msg = bot.send_message(message.chat.id, 'Send a new reminder text:')
        bot.register_next_step_handler(msg, text_register)
    else:
        bot.send_message(message.chat.id, 'You are not an admin, you will not be able to change the settings of the bot'
                         )


def text_register(message):
    new_text = message.text

    if type(new_text) is str:
        with open(json_file, 'rt', encoding='utf-8') as file:
            data = json.load(file)

        data['text'] = new_text

        with open(json_file, 'wt') as file:
            json.dump(data, file, sort_keys=False, indent=2)

        bot.send_message(message.chat.id, 'Message text successfully changed')
    else:
        bot.send_message(message.chat.id, 'Perhaps you are using the command incorrectly?')


@bot.message_handler(commands=['add'])
def add(message):
    if message.from_user.id in LIST_OF_ADMINS:
        msg = bot.send_message(message.chat.id, 'Send the @nickname of the person you want to add to the list:')
        bot.register_next_step_handler(msg, add_register)
    else:
        bot.send_message(message.chat.id, 'You are not an admin, you will not be able to change the settings of the bot'
                         )


def add_register(message):
    add_worker = message.text

    if type(add_worker) is str and add_worker.startswith('@') and len(add_worker) > 1:
        with open(json_file, 'rt', encoding='utf-8') as file:
            data = json.load(file)
        with open(json_file, 'wt', encoding='utf-8') as file:
            data['name'].append(add_worker)
            json.dump(data, file, indent=2)
        statistic(message)

    else:
        bot.send_message(message.chat.id,
                         'Write @username /add')


@bot.message_handler(commands=['del'])
def delete(message):
    if message.from_user.id in LIST_OF_ADMINS:
        msg = bot.send_message(message.chat.id, 'Send the @nickname of the person you want to remove from the list:')
        bot.register_next_step_handler(msg, delete_register)
    else:
        bot.send_message(message.chat.id, 'You are not an admin, you will not be able to change the settings of the bot'
                         )


def delete_register(message):
    delete_worker = message.text

    with open(json_file, 'rt', encoding='utf-8') as file:
        data = json.load(file)

    if type(delete_worker) is str and delete_worker in data["name"]:
        with open(json_file, 'wt', encoding='utf-8') as file:
            data['name'].remove(delete_worker)
            json.dump(data, file, indent=2)
        statistic(message)

    elif delete_worker not in data["name"]:
        bot.send_message(message.chat.id,
                         'Are you sure this @nickname is on the list?\n'
                         'Perhaps you are using the command incorrectly?')
    else:
        bot.send_message(message.chat.id,
                         'An unexpected error occurred, please try the command again. /del')


@bot.message_handler(commands=['day_on'])
def day_on(message):
    if message.from_user.id in LIST_OF_ADMINS:
        msg = bot.send_message(message.chat.id, 'Day of the week number:')
        bot.register_next_step_handler(msg, day_on_register)
    else:
        bot.send_message(message.chat.id, 'You are not an admin, you will not be able to change the settings of the bot'
                         )


def day_on_register(message):
    number_of_day_on = message.text

    if number_of_day_on in str(list(range(8))) and type(number_of_day_on) is str:
        with open(json_file, 'rt', encoding='utf-8') as file:
            data = json.load(file)

        data['day_status'][f'day_{number_of_day_on}'] = "ON"

        with open(json_file, "wt", encoding='utf-8') as file:
            json.dump(data, file, indent=2)
        bot.send_message(message.chat.id, 'Now a reminder will come on that day.')
        statistic(message)

    elif number_of_day_on not in str(list(range(8))):
        bot.send_message(message.chat.id,
                         'There are 7 days in a week, try using the command again.\n'
                         'Perhaps you are using the command incorrectly? /day_on')

    else:
        bot.send_message(message.chat.id, 'An unexpected error occurred, please try the command again. /day_on')


@bot.message_handler(commands=['day_off'])
def day_off(message):
    if message.from_user.id in LIST_OF_ADMINS:
        msg = bot.send_message(message.chat.id, 'Day of the week number:')
        bot.register_next_step_handler(msg, day_off_register)
    else:
        bot.send_message(message.chat.id, 'You are not an admin, you will not be able to change the settings of the bot'
                         )


def day_off_register(message):
    number_of_day_off = message.text

    if number_of_day_off in str(list(range(8))) and type(number_of_day_off) is str:
        with open(json_file, 'rt', encoding='utf-8') as file:
            data = json.load(file)

        data['day_status'][f'day_{number_of_day_off}'] = 'OFF'

        with open(json_file, 'wt', encoding='utf-8') as file:
            json.dump(data, file, indent=2)
        bot.send_message(message.chat.id, 'Now on this day there will be no reminder.')
        statistic(message)

    elif number_of_day_off not in str(list(range(8))):
        bot.send_message(message.chat.id,
                         'There are 7 days in a week, try using the command again.\n'
                         'Perhaps you are using the command incorrectly? /day_off')

    else:
        bot.send_message(message.chat.id, 'An unexpected error occurred, please try the command again. /day_off')


@bot.message_handler(commands=['settime'])
def set_time(message):
    if message.from_user.id in LIST_OF_ADMINS:
        msg = bot.send_message(message.chat.id, 'Day of the week number:')
        bot.register_next_step_handler(msg, set_time_register)
    else:
        bot.send_message(message.chat.id, 'You are not an admin, you will not be able to change the settings of the bot'
                         )


number_of_day = 0  # variable to pass to another function


def set_time_register(message):
    global number_of_day
    number_of_day = message.text
    if number_of_day in str(list(range(8))) and type(number_of_day) is str:
        msg = bot.send_message(message.chat.id, 'Enter time in HH:MM format')
        bot.register_next_step_handler(msg, set_time_second_register)
        return number_of_day
    else:
        bot.send_message(message.chat.id,
                         'There are 7 days in a week, try using the command again.\n'
                         'Perhaps you are using the command incorrectly? /settime')


def set_time_second_register(message):
    day_time = message.text
    if type(day_time) is str and day_time[2] == ':' \
            and len(day_time) == 5 \
            and day_time[0] in str(list(range(3))) \
            and day_time[3] in str(list(range(7))) \
            and day_time[4] in str(list(range(10))):

        with open(json_file, 'rt', encoding='utf-8') as file:
            data = json.load(file)

        data['day_time'][f'day_{number_of_day}'] = day_time + ':00'

        with open(json_file, 'wt', encoding='utf-8') as file:
            json.dump(data, file, indent=2)

        bot.send_message(message.chat.id, f'Время {number_of_day} day of the week changed: {day_time}')
        statistic(message)
    else:
        bot.send_message(message.chat.id,
                         'Enter the time in HH:MM format.\n'
                         'Perhaps you are using the command incorrectly? /settime')


bot.infinity_polling()
