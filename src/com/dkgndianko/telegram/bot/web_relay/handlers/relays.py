from operator import itemgetter
from typing import List
from uuid import uuid4

# from telegram import Update, InlineQueryResultArticle, InputTextMessageContent
# from telegram.ext import ContextTypes


# async def list_relays(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     # return map(itemgetter("name"), context.chat_data.get("relays", []))
#     query = update.inline_query.query
#     if not query:
#         return
#     results = []
#     for it in range(5):
#         results.append(
#             InlineQueryResultArticle(
#                 id=query,
#                 title=f"Item {it}",
#                 input_message_content=InputTextMessageContent(f"This is item {it}")
#             )
#         )
#     await context.bot.answer_inline_query(update.inline_query.id, results)


from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import ContextTypes, filters, ConversationHandler, CommandHandler, MessageHandler

from com.dkgndianko.core.logging import get_logger
from com.dkgndianko.telegram.bot.web_relay.states import SELECT_RELAY, RELAY_SELECTED, CREATE_RELAY



get_name = itemgetter("name")
get_id = itemgetter("id")

log = get_logger(__name__)

async def list_relays(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    log.debug(context.chat_data)
    try:
        relays = context.chat_data["RELAYS"]
    except KeyError:
        log.error("No relays found. Creating new ones")
        relays = [{"id": str(uuid4()), "name": f"Item {i}", "url": "", "switches": []} for i in range(5)]
        context.chat_data["RELAYS"] = relays
    if len(relays) == 0:
        log.info("No relay is there.")
        await update.message.reply_text("No relay found. Please create new ones.")
        return CREATE_RELAY
    reply_keyboard = [list(map(get_name,relays))]
    presentation = "Please choose one of these items"
    await update.message.reply_text(
        presentation,
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=False, input_field_placeholder="Which item to choose"
        )
    )
    return SELECT_RELAY


async def select_relay(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    selected_relay_name = update.message.text
    relays: List = context.chat_data["RELAYS"]
    selected_relay = next(filter(lambda r: get_name(r) == selected_relay_name, relays), None)

    if selected_relay:
        context.chat_data["CURRENT_RELAY_ID"] = selected_relay.get("id")
        reply_keyboard = [["cancel", "edit", "remove"], ["Get states", "Set state"]]
        presentation = f"Please select the action you wish with the relay ({selected_relay_name})"
        await update.message.reply_text(
            presentation,
            reply_markup=ReplyKeyboardMarkup(
                reply_keyboard, one_time_keyboard=False, input_field_placeholder="Action"
            )
        )

        return RELAY_SELECTED
    else:
        await update.message.reply_text("please select one of these relays.")
        return SELECT_RELAY


async def add_new_relay(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    pass

async def remove_relay(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    try:
        relay_id = context.chat_data["CURRENT_RELAY_ID"]
        relays: List = context.chat_data["RELAYS"]
        new_relays = filter(lambda r: get_id(r) != relay_id, relays)
        context.chat_data["RELAYS"] = list(new_relays)
        del context.chat_data["CURRENT_RELAY_ID"]
        await update.message.reply_text("Relay is deleted successfully!", reply_markup=ReplyKeyboardRemove())
    except KeyError:
        await update.message.reply_text("No relay selected.")
    return ConversationHandler.END


async def cancel_relay(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user =  update.message.from_user
    message = f"{user.first_name} you are cancelling the relay"
    del context.chat_data["CURRENT_RELAY_ID"]
    await update.message.reply_text(message, reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END


async def edit_relay(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text(f"You are editing the relay. You can set the name or the url.", reply_markup=ReplyKeyboardRemove())
    # return RELAY_SELECTED
    return ConversationHandler.END




relays_conversation_handler = ConversationHandler(
    entry_points=[CommandHandler("list", list_relays)],
    states={
        SELECT_RELAY: [MessageHandler(filters.ALL, select_relay)],
        RELAY_SELECTED: [
            MessageHandler(filters.Regex("^cancel$"), cancel_relay),
            MessageHandler(filters.Regex("^remove$"), remove_relay),
            MessageHandler(filters.Regex("^edit$"), edit_relay)
            ]
    },
    fallbacks=[CommandHandler("cancel", cancel_relay)]
)

