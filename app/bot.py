# -*- coding: utf-8 -*-

import logging
import time
import json
import os
from dotenv import load_dotenv

from telebot import TeleBot, types, logger

load_dotenv()

API_TOKEN = os.getenv('BOT_API_TOKEN')
WEBHOOK_HOST = os.getenv('WEBHOOK_HOST')
WEBHOOK_URL = WEBHOOK_HOST + '/api/bot'

logger.setLevel(logging.INFO)

bot = TeleBot(API_TOKEN, threaded=False)

# Handle '/start'
@bot.message_handler(commands=['start'])
def start_command_handler(message: types.Message):
	mention = f'<a href="tg://user?id={message.from_user.id}">{message.from_user.first_name}</a>'
	bot.send_message(
		chat_id = message.chat.id, # chat id where the message will be sent
		text = f'Hello, dear {mention}! \nCopy and paste or directly type in the editor below your messy JSON code and let me tidy and validate it.', # message text
		parse_mode = "HTML"
	)

# Handle all other messages
@bot.message_handler()
def message_handler(message: types.Message):
	try:
		payload = json.loads(message.text)
	except json.JSONDecodeError as ex:
		bot.send_message(
			chat_id=message.chat.id,
			text=f'Error:\n<code>{str(ex)}</code>\nPlease specify valid JSON.',
			parse_mode = "HTML"
		)
		return
	text = json.dumps(payload, indent=2, sort_keys=False, ensure_ascii=False)
	bot.send_message(
		chat_id=message.chat.id,
		text=f'JSON:\n<code>{text}</code>',
		parse_mode = "HTML"
	)

def bot_register(json_string):
	update = types.Update.de_json(json_string)
	bot.process_new_updates([update])
	return ''

def update_webhook():
	bot.remove_webhook()
	time.sleep(1)
	bot.set_webhook(url=WEBHOOK_URL)
	return "Webhook was updated to: %s" % (WEBHOOK_URL)
