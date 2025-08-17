import os
import logging
from telegram import Update, ForceReply
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Logging ကို အသင့်ပြင်ထားခြင်း (Error တွေစစ်ဖို့)
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# /start command အတွက် function
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """User က /start command ကိုနှိပ်ရင် 'မင်္ဂလာပါ' လို့ စာပြန်မယ်။"""
    user = update.effective_user
    # User ကို HTML format နဲ့ reply ပြန်ပြီး မင်္ဂလာပါလို့ နှုတ်ဆက်မယ်။
    await update.message.reply_html(
        f"မင်္ဂလာပါ {user.mention_html()}!",
    )

# File တွေပို့လာရင် ထိန်းချုပ်မယ့် function
async def handle_file(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """User က file (document, photo, video, audio, etc.) ပို့လာရင် လက်မခံကြောင်း စာပြန်မယ်။"""
    # ဘာ file မှ download မလုပ်ဘဲ စာပဲပြန်မယ်။
    await update.message.reply_text("File များလက်မခံပါ။")

def main() -> None:
    """Bot ကို စတင်လည်ပတ်စေမယ်။"""
    # Telegram Bot Token ကို Environment Variable ကနေယူသုံးမယ်။
    # Render.com မှာ deploy လုပ်တဲ့အခါ ဒီနည်းက လုံခြုံပါတယ်။
    TOKEN = os.getenv("TELEGRAM_TOKEN")
    if not TOKEN:
        raise ValueError("TELEGRAM_TOKEN ဆိုတဲ့ environment variable ကိုရှာမတွေ့ပါ!")

    # Application ကိုတည်ဆောက်မယ်။
    application = Application.builder().token(TOKEN).build()

    # Command တွေကို မှတ်ပုံတင်မယ်။
    # /start command အတွက် start function ကိုချိတ်ဆက်ပေးလိုက်တယ်။
    application.add_handler(CommandHandler("start", start))

    # Message Handler တွေကို မှတ်ပုံတင်မယ်။
    # filters.ALL ထဲက text, command မဟုတ်တဲ့ file အမျိုးအစားအားလုံးကို handle_file function နဲ့ ချိတ်ပေးလိုက်တယ်။
    # DOCUMENT, PHOTO, VIDEO, AUDIO, VOICE စတဲ့ file မှန်သမျှကို ဒီ handler က ဖမ်းပေးပါလိမ့်မယ်။
    application.add_handler(MessageHandler(
        filters.Document.ALL | filters.PHOTO | filters.VIDEO | filters.AUDIO | filters.VOICE, 
        handle_file
    ))

    # Bot ကို စတင်လည်ပတ်စေမယ်။
    print("Bot is running...")
    application.run_polling()

if __name__ == "__main__":
    main()