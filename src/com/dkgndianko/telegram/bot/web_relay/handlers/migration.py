from telegram import Update
from telegram.ext import ContextTypes


def migration_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    messsage = update.message
    application = context.application
    application.migrate_chat_data(message=messsage)