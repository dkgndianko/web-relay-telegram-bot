from telegram import Update
from com.dkgndianko.core.logging import get_logger
from com.dkgndianko.telegram.bot.web_relay.app import app

log = get_logger(__name__)
log.debug("start polling ...")
app.run_polling(allowed_updates=Update.ALL_TYPES)