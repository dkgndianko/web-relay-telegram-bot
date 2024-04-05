from telegram.ext import ApplicationBuilder, CommandHandler, Application, MessageHandler, filters, InlineQueryHandler, PicklePersistence
from com.dkgndianko.core.config import settings
from com.dkgndianko.core.logging import get_logger
from com.dkgndianko.telegram.bot.persistence import get_persistence
from com.dkgndianko.telegram.bot.web_relay.handlers.relays import relays_conversation_handler
from com.dkgndianko.telegram.bot.web_relay.handlers.start import start_handler
from com.dkgndianko.telegram.bot.web_relay.handlers.migration import migration_handler

log = get_logger(__name__)

log.debug(f"Telegram token is {settings.TELEGRAM_BOT_TOKEN} and perssitence is {settings.TELEGRAM_PERSISTENCE_PATH}")
# persistence = PicklePersistence(filepath=settings.TELEGRAM_PERSISTENCE_PATH)
persistence = get_persistence()

app: Application = ApplicationBuilder().token(settings.TELEGRAM_BOT_TOKEN).persistence(persistence=persistence).build()

## add handler for chat migration
app.add_handler(MessageHandler(filters.StatusUpdate.MIGRATE, migration_handler))


# app.add_handler(CommandHandler("start", start_handler))
# app.add_handler(InlineQueryHandler(list_relays))
# list relays
app.add_handler(relays_conversation_handler)
# select relay
# list switches
# get states
# set state