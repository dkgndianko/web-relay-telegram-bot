from telegram import Update
from telegram.ext import ContextTypes

async def start_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update._bot.send_message(chat_id=update.effective_chat.id, text=f"Hello {update.effective_user.name}")