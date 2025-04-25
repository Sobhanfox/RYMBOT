
import telebot
import json
from datetime import datetime, timedelta

TOKEN = "YOUR_BOT_TOKEN"
bot = telebot.TeleBot(TOKEN)

DATA_FILE = "users.json"

def load_data():
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except:
        return {}

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)

@bot.message_handler(commands=['start'])
def start_handler(message):
    user_id = str(message.from_user.id)
    data = load_data()
    if user_id not in data:
        data[user_id] = {
            "score": 0,
            "last_daily": "2000-01-01",
            "invited": []
        }
        save_data(data)
        bot.reply_to(message, "به ربات بازی خوش اومدی! با /daily جایزه روزانه بگیر!")
    else:
        bot.reply_to(message, "دوباره خوش اومدی! با /score امتیازت رو ببین.")

@bot.message_handler(commands=['score'])
def score_handler(message):
    user_id = str(message.from_user.id)
    data = load_data()
    score = data.get(user_id, {}).get("score", 0)
    bot.reply_to(message, f"امتیاز شما: {score} سکه")

@bot.message_handler(commands=['daily'])
def daily_handler(message):
    user_id = str(message.from_user.id)
    data = load_data()
    today = datetime.now().date()
    last_claim = datetime.strptime(data[user_id]["last_daily"], "%Y-%m-%d").date()
    if today > last_claim:
        data[user_id]["score"] += 100
        data[user_id]["last_daily"] = today.strftime("%Y-%m-%d")
        save_data(data)
        bot.reply_to(message, "تبریک! ۱۰۰ امتیاز گرفتی!")
    else:
        bot.reply_to(message, "تو امروز جایزه‌تو گرفتی! فردا دوباره بیا.")

@bot.message_handler(commands=['invite'])
def invite_handler(message):
    user_id = str(message.from_user.id)
    link = f"https://t.me/YOUR_BOT_USERNAME?start={user_id}"
    bot.reply_to(message, f"لینک دعوت اختصاصی تو:
{link}
هر کسی با این لینک بیاد، ۵۰ امتیاز می‌گیری!")

bot.polling()
