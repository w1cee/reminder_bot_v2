# -*- coding: utf-8 -*-
# bot by w1cee

import json
import time
import telebot
import pytz
from datetime import datetime

json_file = 'config.json'

TOKEN = 'TOKEN'
bot = telebot.TeleBot(TOKEN)
group_id = 'id'


def message_to_remind():
    data = json.load(open(json_file, 'r'))
    updated_list = data['name']
    updated_list = ' '.join(updated_list)
    text_message = data['text']
    text_message = ''.join(text_message)
    bot.send_message(group_id,
                     f'{text_message}\n{updated_list}')


while True:
    file_check = json.load(open(json_file, 'r'))
    now = datetime.now(pytz.timezone('Europe/Kiev'))
    current_day = datetime.today().isoweekday()
    if file_check['day_status'][f'day_{current_day}'] == 'ON':
        if file_check['day_time'][f'day_{current_day}'] == now.strftime("%H:%M:%S"):
            message_to_remind()
    time.sleep(1)
