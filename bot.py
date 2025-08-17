import os
import logging
import threading
from flask import Flask
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# --- Flask Web Server အပိုင်း ---
# Render.com က port binding error မတက်အောင် web server အတုတစ်ခု run ထားပေးမယ်။
app = Flask(__name__)

@app.route('/')
def index():
    # Render က ဒီ URL ကိုလာစစ်တဲ့အခါ "I am alive" လို့ပြရင် service က run နေတယ်လို့မှတ်ယူသွားမယ်။
    return "Bot is alive and running!"

def run_flask():
    # Render က PORT ဆိုတဲ့ Environment Variable ကိုအလိုအလျောက်ထည့်ပေးတယ်။
    # အဲ့ဒီ port ကိုသုံးပြီး server ကို run မယ်။
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)

# --- Telegram Bot အပိုင်း ---
# Logging ကို အသင့်ပြင်ထားခြင်း (Error တွေစစ်ဖို့)
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# /start command အတွက် function
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user

    # Bot ကနေ ပြန်ပို့ချင်တဲ့ စာသားကို ဒီမှာစုရေးထားပါတယ်
    welcome_message = f"""မင်္ဂလာပါ {user.mention_html()}!

VIPဝင်ရန် ​အောက်ပါအ​ကောင့်များသို့ ဝင်ကြေး တစ်​သောင်းကျပ်လွှဲပြီး ​ပြေစာကို ယခုBotသို့ ပို့​ပေးပါ။
​ပြေစာပို့ပြီး မိနစ်ပိုင်း (သို့မဟုတ်) နာရီပိုင်းအတွင်း VIP channel invite linkများ ပို့​ပေးပါမယ်။

​ငွေလွှဲ​ပြေစာကို AIနဲ့စစ်ပြီးမှ adminစီကို ​ရောက်တာမလို့
- ​​ကြည်လင်ပျက်သားတဲ့ ​​ငွေလွှဲပြေစာကို ပို့​ပေးပါ။
- ​ငွေလွှဲသည့်အခါ တစ်​သောင်းကျပ်ကို အတိအကျ လွှဲ​ပေးပါ။

<b>Kpay</b>
Kaung Khant Wai
09123456789

<b>Wave</b>
Kaung Khant Wai
09123456789
"""

    # စာသားကို user ဆီ ပို့လွှတ်ပါမယ်
    await update.message.reply_html(
        text=welcome_message,
    )

# File တွေပို့လာရင် ထိန်းချုပ်မယ့် function
async def handle_file(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("အမှားအယွင်း ဖြစ်ပွားသွားပါတယ်။ ​ခဏ​နေမှ ပြန်လည်ကြိုးစားကြည့်ပါ (သို့မဟုတ်) ​ပြေစာကို ပြန်လည်စစ်​ဆေးကြည့်ပါ။")

def main() -> None:
    # --- အရေးကြီးတဲ့ အပြောင်းအလဲ ---
    # Flask server ကို thread သီးသန့်တစ်ခုနဲ့ background မှာ run မယ်။
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.daemon = True
    flask_thread.start()
    
    # Telegram Bot Token ကို Environment Variable ကနေယူသုံးမယ်။
    TOKEN = os.getenv("TELEGRAM_TOKEN")
    if not TOKEN:
        raise ValueError("TELEGRAM_TOKEN ဆိုတဲ့ environment variable ကိုရှာမတွေ့ပါ!")

    # Application ကိုတည်ဆောက်မယ်။
    application = Application.builder().token(TOKEN).build()

    # Handlers တွေကို မှတ်ပုံတင်မယ်။
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(
        filters.Document.ALL | filters.PHOTO | filters.VIDEO | filters.AUDIO | filters.VOICE, 
        handle_file
    ))

    # Bot ကို စတင်လည်ပတ်စေမယ်။
    print("Starting Telegram Bot Polling...")
    application.run_polling()

if __name__ == "__main__":
    main()
