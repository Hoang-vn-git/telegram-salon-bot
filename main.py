import os

from telebot import types

import telegrambot.tele
from dotenv import load_dotenv
from flask import Flask, request


app = Flask(__name__)

load_dotenv()

bot = telegrambot.tele.run_bot()

@app.route('/', methods=['POST'])
def webhook():
    json_str = request.get_data().decode("utf-8")
    update = types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return "", 200

# ---------- Main ----------

if __name__ == "__main__":
    # Run Flask on port 8000
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port)