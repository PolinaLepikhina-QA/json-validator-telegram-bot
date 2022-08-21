# -*- coding: utf-8 -*-

import flask

from app.bot import bot_register, update_webhook

WEBHOOK_URL_PATH = "/api/bot"
UPDATE_WEBHOOK_PATH = "/api/webhook"

app = flask.Flask(__name__)

@app.route("/", methods=['GET'])
def home():
    return 'Telegram bot start page'

# Process webhook calls
@app.route(WEBHOOK_URL_PATH, methods=['POST'])
def webhook():
    if flask.request.headers.get('content-type') == 'application/json':
        return bot_register(flask.request.get_data().decode('utf-8'))
    else:
        flask.abort(403)

# Update webhook
@app.route(UPDATE_WEBHOOK_PATH, methods=['GET'])
def process_update_webhook():
    return update_webhook()
