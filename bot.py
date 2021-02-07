# coding=utf-8
from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters
from telegram import InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import InlineQueryHandler
from translate import OgerTranslator
import logging

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

token = open("token.SECRET").read().replace("\n", "")
updater = Updater(token=token, use_context=True)
dispatcher = updater.dispatcher

def start(update, context):
    startnachricht = "Hallo. Ich übersetze deinen Scheiß in Meddlfrängisch! Schreib:"
    command = "@toOgerBot <deine Nachricht>"

    startnachricht = OgerTranslator.translate(startnachricht) + " " + command
    context.bot.send_message(chat_id=update.effective_chat.id, text=startnachricht)
                             
def echo(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)


def inline_translate(update, context):
    query = update.inline_query.query
    if not query:
        return
    results = list()
    results.append(
        InlineQueryResultArticle(
            id=hash(query),
            title='Meddlfrängische Übersetzung',
            input_message_content=InputTextMessageContent(OgerTranslator.translate(query)),
            thumb_url = 'https://ogertranslate.ml/assets/img/dzo-logo.png'
        )
    )
    context.bot.answer_inline_query(update.inline_query.id, results)

start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

#echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)
#dispatcher.add_handler(echo_handler)

inline_translator = InlineQueryHandler(inline_translate)
dispatcher.add_handler(inline_translator)

updater.start_polling()
