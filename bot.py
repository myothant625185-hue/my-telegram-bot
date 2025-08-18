import os
import logging
import threading
from flask import Flask
from waitress import serve  # <--- ဒီတစ်ကြောင်း အသစ်ထည့်ပါ
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# ======== 1. Render အတွက် Web Server အပိုင်း ========
app = Flask(__name__)
@app.route('/')
def index():
    return "Bot is alive!"

def run_flask():
    port = int(os.environ.get('PORT', 10000))
    # app.run(...) အစား waitress server ကိုသုံးမယ်
    serve(app, host='0.0.0.0', port=port)  # <--- ဒီတစ်ကြောင်းကို ပြောင်းပါ

# ======== 2. Telegram Bot Logic အပိုင်း ========
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

# /start command handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("မင်္ဂလာပါ။")

# File handler
async def handle_file(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # ... (ဒီအပိုင်းကတော့ သင်ရေးထားတဲ့အတိုင်းပါပဲ) ...
    await update.message.reply_text("File များလက်မခံပါ။")

# ======== 3. Bot ကို Run မယ့် အဓိက အပိုင်း ========
def main() -> None:
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.daemon = True
    flask_thread.start()

    TOKEN = os.getenv("TELEGRAM_TOKEN")
    
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.Document.ALL | filters.PHOTO, handle_file))

    print("Telegram Bot is running...")
    application.run_polling()

if __name__ == "__main__":
    main()
