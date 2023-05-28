# -*- coding: utf-8 -*-
# Author: w1cee
import re
import os
import glob
import json
import time
import pytz
import random
import telebot
from datetime import datetime
from threading import Thread
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from bot_config import BOT_TOKEN

TOKEN = BOT_TOKEN
bot = telebot.TeleBot(TOKEN)
LIST_OF_ADMINS = []
GROUP_ID = 0
config_file = 'config.json'
lang = {}
lang_dir_path = 'lang/'
default_language = {
    "lang_name": "English (default)",
    "reminder_text": "Text to remind:",
    "list_of_users": "List of users:",
    "day_status": "Day status on/off:",
    "day_time": "Time for reminder",
    "not_admin": "You are not allowed to use this command.",
    "incorrect_using": "Incorrect data format. The command was not executed.",
    "captcha_fail": "You did not pass the captcha, please try again.",
    "set_text": "Send a new reminder text.",
    "add_user": "Send me the @username of the person you want to add to the list.",
    "del_user": "Send me the @username of someone to be removed from the list.",
    "day_on": "Send me the number of the day of the week you want to be reminded.",
    "day_off": "Send me the number of the day of the week you don't want to be reminded.",
    "set_time": "Send me the number of the day of the week you want to change the reminder time.",
    "time_format": "Send me the time in HH:MM format.",
    "add_admin": "Send me the @username of the new admin.",
    "del_admin": "Send me the @username of the admin to be removed.",
    "solve_captcha": "Solve the captcha to continue.",
    "admin_delete_yourself": "You cannot deprive yourself of administrator rights.",
    "user_not_in_list": "This user is not in the list.",
    "send_id_of_group": "Send me id of new group.",
    "for_admins": "For admins",
    "group_id": "Group id",
    "admins": "Admins",
    "current_lang": "Current language",
    "available_lang": "Available languages",
    "timezone": "Time zone",
    "choose_timezone": "Send me a new timezone.\nThe current list of time zones is in this file:\nhttps://gist.github.com/heyalexej/8bf688fd67d7199be4a1682b3eec7568",
    "choose_timezone_error": "Please enter correct time zone.",
    "help": "/add add user to list\n/del remove the user from the list\n/day_on turn on the reminder for the day of the week\n/day_off turn off the reminder for the day of the week\n/set_time set the time for the day of the week\n/set_text set reminder text\n/add_admin add administrator\n/del_admin remove administrator\n/change_group change group\n/view current bot settings\n/help list of commands"
}


@bot.message_handler(commands=['view'])
def statistic(message):
    with open(config_file, 'rt', encoding='utf-8') as file:
        data = json.load(file)
    list_users = ', '.join(data['workers'])
    remind_message = data['text']
    day_status = [f'{day}: {status}' for day, status in data['day_status'].items()]
    day_status = '\n'.join(day_status)
    day_time = [f'{day}: {time}' for day, time in data['day_time'].items()]
    day_time = '\n'.join(day_time)
    admins = ', '.join(data['admins'])
    available_lang = ', '.join(data['available_lang'])
    bot.send_message(message.chat.id, f"{lang['reminder_text']}\n"
                                      f"{remind_message}\n"
                                      f"\n"
                                      f"{lang['list_of_users']} {list_users}\n"
                                      f"\n"
                                      f"{lang['day_status']}\n{day_status}\n"
                                      f"\n"
                                      f"{lang['day_time']}\n{day_time}"
                     )
    if f'@{message.from_user.username}' in LIST_OF_ADMINS:
        bot.send_message(message.chat.id, f"{lang['for_admins']}:\n"
                                          f"{lang['group_id']}: {GROUP_ID}\n"
                                          f"{lang['admins']}: {admins}\n"
                                          f"{lang['current_lang']}: {lang['lang_name']}\n"
                                          f"{lang['available_lang']}: {available_lang}\n"
                                          f"{lang['timezone']}: {data['timezone']}")


def message_to_remind():
    with open(config_file, 'rt', encoding='utf-8') as file:
        data = json.load(file)
    updated_list = ' '.join(data['workers'])
    text_message = ''.join(data['text'])
    bot.send_message(GROUP_ID,
                     f'{text_message}\n{updated_list}')


@bot.message_handler(commands=['help'])
def help_command(message):
    bot.send_message(message.chat.id, lang['help'])


def admin_check(message):
    if f'@{message.from_user.username}' in LIST_OF_ADMINS:
        return True
    bot.send_message(message.chat.id, lang['not_admin'])
    return False


@bot.message_handler(commands=['set_text'])
def text(message):
    if admin_check(message):
        msg = bot.send_message(message.chat.id, lang['set_text'])
        bot.register_next_step_handler(msg, text_register)


def text_register(message):
    new_text = message.text
    if isinstance(new_text, str):
        with open(config_file, 'rt', encoding='utf-8') as file:
            data = json.load(file)
        data['text'] = new_text
        with open(config_file, 'wt') as file:
            json.dump(data, file, indent=2)
        statistic(message)
    else:
        bot.send_message(message.chat.id, lang['incorrect_using'])


@bot.message_handler(commands=['add'])
def add(message):
    if admin_check(message):
        msg = bot.send_message(message.chat.id, lang['add_user'])
        bot.register_next_step_handler(msg, add_register)


def add_register(message):
    add_worker = message.text
    if isinstance(add_worker, str) and add_worker.startswith('@'):
        with open(config_file, 'rt', encoding='utf-8') as file:
            data = json.load(file)
        with open(config_file, 'wt', encoding='utf-8') as file:
            data['workers'].append(add_worker)
            json.dump(data, file, indent=2)
        statistic(message)
    else:
        bot.send_message(message.chat.id, lang['incorrect_using'])


@bot.message_handler(commands=['del'])
def delete(message):
    if admin_check(message):
        msg = bot.send_message(message.chat.id, lang['del_user'])
        bot.register_next_step_handler(msg, delete_register)


def delete_register(message):
    delete_worker = message.text
    with open(config_file, 'rt', encoding='utf-8') as file:
        data = json.load(file)
    if delete_worker in data['workers']:
        with open(config_file, 'wt', encoding='utf-8') as file:
            data['workers'].remove(delete_worker)
            json.dump(data, file, indent=2)
        statistic(message)
    else:
        bot.send_message(message.chat.id, lang['user_not_in_list'])


@bot.message_handler(commands=['day_on'])
def day_on(message):
    if admin_check(message):
        msg = bot.send_message(message.chat.id, lang['day_on'])
        bot.register_next_step_handler(msg, day_on_register)


def day_on_register(message):
    number_of_day_on = message.text
    if number_of_day_on in [str(x) for x in range(8)]:
        with open(config_file, 'rt', encoding='utf-8') as file:
            data = json.load(file)
        data['day_status'][f'day_{number_of_day_on}'] = "ON"
        with open(config_file, "wt", encoding='utf-8') as file:
            json.dump(data, file, indent=2)
        statistic(message)
    else:
        bot.send_message(message.chat.id, lang['incorrect_using'])


@bot.message_handler(commands=['day_off'])
def day_off(message):
    if admin_check(message):
        msg = bot.send_message(message.chat.id, lang['day_off'])
        bot.register_next_step_handler(msg, day_off_register)


def day_off_register(message):
    number_of_day_off = message.text
    if number_of_day_off in [str(x) for x in range(8)]:
        with open(config_file, 'rt', encoding='utf-8') as file:
            data = json.load(file)
        data['day_status'][f'day_{number_of_day_off}'] = 'OFF'
        with open(config_file, 'wt', encoding='utf-8') as file:
            json.dump(data, file, indent=2)
        statistic(message)

    else:
        bot.send_message(message.chat.id, lang['incorrect_using'])


@bot.message_handler(commands=['set_time'])
def set_time(message):
    if admin_check(message):
        msg = bot.send_message(message.chat.id, lang['set_time'])
        bot.register_next_step_handler(msg, set_time_register)


number_of_day = 0


def set_time_register(message):
    global number_of_day
    number_of_day = message.text
    if number_of_day in [str(x) for x in range(8)]:
        msg = bot.send_message(message.chat.id, lang['time_format'])
        bot.register_next_step_handler(msg, set_time_second_register)
    else:
        bot.send_message(message.chat.id, lang['incorrect_using'])


def set_time_second_register(message):
    if day_time := message.text:
        if match := re.fullmatch(
                r'^([0-1]?[0-9]|[2][0-3]):([0-5][0-9])$', rf'{day_time}'
        ):
            with open(config_file, 'rt', encoding='utf-8') as file:
                data = json.load(file)
            data['day_time'][f'day_{number_of_day}'] = f'{day_time}:00'
            with open(config_file, 'wt', encoding='utf-8') as file:
                json.dump(data, file, indent=2)
            statistic(message)
        else:
            bot.send_message(message.chat.id, lang['incorrect_using'])
    else:
        bot.send_message(message.chat.id, lang['incorrect_using'])


@bot.message_handler(commands=['add_admin'])
def add_admin(message):
    if admin_check(message):
        msg = bot.send_message(message.chat.id, lang['add_admin'])
        bot.register_next_step_handler(msg, add_admin_register)


def add_admin_register(message):
    admin_username = message.text
    if isinstance(admin_username, str) and admin_username.startswith('@'):
        with open(config_file, 'rt', encoding='utf-8') as file:
            data = json.load(file)
        data['admins'].append(admin_username)
        with open(config_file, 'wt', encoding='utf-8') as file:
            json.dump(data, file, indent=2)
        statistic(message)
    else:
        bot.send_message(message.chat.id, lang['incorrect_using'])


@bot.message_handler(commands=['del_admin'])
def del_admin(message):
    if admin_check(message):
        msg = bot.send_message(message.chat.id, lang['del_admin'])
        bot.register_next_step_handler(msg, del_admin_register)


def del_admin_register(message):
    global del_admin_username, num_sum
    del_admin_username = message.text
    if isinstance(del_admin_username, str) and del_admin_username.startswith('@'):
        with open(config_file, 'rt', encoding='utf-8') as file:
            data = json.load(file)
        admins = data['admins']
        if del_admin_username in admins and del_admin_username != f'@{message.from_user.username}':
            num1, num2 = random.randint(1, 100), random.randint(1, 100)
            num_sum = num1 + num2
            msg = bot.send_message(message.chat.id, f"{lang['solve_captcha']}\n"
                                                    f'{num1}+{num2}')
            bot.register_next_step_handler(msg, del_admin_confirmation)
        elif del_admin_username == f'@{message.from_user.username}':
            bot.send_message(message.chat.id, lang['admin_delete_yourself'])
        else:
            bot.send_message(message.chat.id, lang['user_not_in_list'])
    else:
        bot.send_message(message.chat.id, lang['incorrect_using'])


num_sum = 0
del_admin_username = 0


def del_admin_confirmation(message):
    try:
        if int(message.text) == num_sum:
            with open(config_file, 'rt', encoding='utf-8') as file:
                data = json.load(file)
            admins = data['admins']
            admins.remove(del_admin_username)
            data['admins'] = admins
            with open(config_file, 'wt', encoding='utf-8') as file:
                json.dump(data, file, indent=2)
            statistic(message)
        else:
            bot.send_message(message.chat.id, lang['captcha_fail'])
    except Exception:
        bot.send_message(message.chat.id, lang['incorrect_using'])


@bot.message_handler(commands=['change_group'])
def change_group(message):
    if admin_check(message):
        msg = bot.send_message(message.chat.id, lang['send_id_of_group'])
        bot.register_next_step_handler(msg, change_group_register)


def change_group_register(message):
    global GROUP_ID
    try:
        with open(config_file, 'rt', encoding='utf-8') as file:
            data = json.load(file)
        group_id = int(message.text)
        data['group_id'] = group_id
        GROUP_ID = group_id
        for day in data['day_status']:
            data['day_status'][day] = 'OFF'
        for day in data['day_time']:
            data['day_time'][day] = '17:50:00'
        with open(config_file, 'wt', encoding='utf-8') as file:
            json.dump(data, file, indent=2)
        statistic(message)
    except Exception:
        bot.send_message(message.chat.id, lang['incorrect_using'])


@bot.message_handler(commands=['set_lang'])
def choose_language(message):
    if json_files := [
        f for f in os.listdir(lang_dir_path) if f.endswith('.json')
    ]:
        markup = InlineKeyboardMarkup()
        markup.row_width = 1
        for filename in glob.iglob(f'{lang_dir_path}*.json', recursive=True):
            filename = filename[5:]
            with open(f'{lang_dir_path}{filename}', 'rt', encoding='utf-8') as file:
                data = json.load(file)
                markup.add(InlineKeyboardButton(data['lang_name'], callback_data=filename))
        bot.send_message(message.chat.id, 'Choose your language', reply_markup=markup)
    else:
        bot.send_message(message.chat.id, 'Only default language is available.')


@bot.message_handler(commands=['change_timezone'])
def change_timezone(message):
    if admin_check(message):
        msg = bot.send_message(message.chat.id, lang['choose_timezone'])
        bot.register_next_step_handler(msg, change_timezone_register)


def change_timezone_register(message):
    if message.text in pytz.all_timezones:
        with open(config_file, 'rt', encoding='utf-8') as file:
            data = json.load(file)
        with open(config_file, 'wt', encoding='utf-8') as file:
            data['timezone'] = message.text
            json.dump(data, file, indent=2)
        statistic(message)
    else:
        bot.send_message(message.chat.id, lang['choose_timezone_error'])


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    with open(config_file, 'rt', encoding='utf-8') as file:
        data = json.load(file)
    bot.answer_callback_query(call.id, '✅')
    data['lang_file'] = call.data
    with open(config_file, 'wt', encoding='utf-8') as file:
        json.dump(data, file, indent=2)


def telegram_bot_polling():
    bot.infinity_polling()


def variables_updater():
    global LIST_OF_ADMINS, GROUP_ID, lang
    json_files = [f for f in os.listdir(lang_dir_path) if f.endswith('.json')]
    with open(config_file, 'rt', encoding='utf-8') as file:
        data = json.load(file)
    if not json_files:
        data['lang_file'] = 'default_language'
        lang = default_language
    elif data['lang_file'] == 'default_language':
        lang = default_language
    else:
        try:
            with open(f"{lang_dir_path}{data['lang_file']}", 'rt', encoding='utf-8') as file:
                lang = json.load(file)
        except FileNotFoundError:
            data['lang_file'] = 'default_language'
            lang = default_language
    available_lang = []
    for lang_file in json_files:
        with open(f"{lang_dir_path}{lang_file}", 'rt', encoding='utf-8') as file:
            lang_file = json.load(file)
            available_lang.append(lang_file['lang_name'])
    data['available_lang'] = available_lang
    if data['timezone'] not in pytz.all_timezones:
        data['timezone'] = 'UTC'
    with open(config_file, 'wt', encoding='utf-8') as file:
        json.dump(data, file, indent=2)
    LIST_OF_ADMINS = data['admins']
    GROUP_ID = data['group_id']


def remind_time_checker():
    while True:
        variables_updater()
        with open(config_file, 'rt', encoding='utf-8') as file:
            data = json.load(file)
        now = datetime.now(pytz.timezone('Europe/Kiev'))
        current_day = datetime.now().isoweekday()
        if data['day_status'][f'day_{current_day}'] == 'ON' and data['day_time'][f'day_{current_day}'] \
                == now.strftime("%H:%M:%S"):
            message_to_remind()
        time.sleep(1)


telegram_bot_polling = Thread(target=telegram_bot_polling)
remind_time_checker = Thread(target=remind_time_checker)

telegram_bot_polling.start()
remind_time_checker.start()

telegram_bot_polling.join()
remind_time_checker.join()
