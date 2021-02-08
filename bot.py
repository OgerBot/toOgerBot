# coding=utf-8
from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters
from telegram import InlineQueryResultArticle, InlineQueryResultAudio, InputTextMessageContent
from telegram.ext import InlineQueryHandler
from translate import OgerTranslator
import logging
import random

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

token = open("token.SECRET").read().replace("\n", "")
updater = Updater(token=token, use_context=True)
dispatcher = updater.dispatcher

audios = open("audios.txt", "r", encoding="utf-8").read().split("\n")[0:-1]

def start(update, context):
    startnachricht = "Hallo. Ich übersetze deinen Scheiß in Meddlfrängisch! Schreib:"
    command = "@toOgerBot <deine Nachricht>"

    startnachricht = OgerTranslator.translate(startnachricht) + " " + command
    context.bot.send_message(chat_id=update.effective_chat.id, text=startnachricht)
                             
def echo(update, context):
    """
        translates messages and sends them back
    """
    message = update.message.text
    response = "Meintest du vielleicht: \n" + message
    context.bot.send_message(chat_id=update.effective_chat.id, text=OgerTranslator.translate(response))


def inline_translate(update, context):
    query = update.inline_query.query
    results = []

    if len(query.split(' ')) == 1 or not query:
        audio_id = 0
        if query:
            for i in range(len(audios)):
                if query.lower() in audios[i].split(";")[1].lower():
                    audio_id = i
                    break
        else:
            audio_id = random.randint(0, len(audios))
        audiofile, title = audios[audio_id].split(";")
        #title = OgerTranslator.translate(title)
        results.append(InlineQueryResultAudio(
            id = "audio"+str(audio_id),
            audio_url = audiofile,
            title = title,
            caption = title
            )
        )

    if query:
        translation = OgerTranslator.translate(query)
        results.append(
            InlineQueryResultArticle(
                id = hash(query),
                title = 'Meddlfrängische Übersetzung.',
                input_message_content = InputTextMessageContent(translation),
                thumb_url = 'https://ogertranslate.ml/assets/img/dzo-logo.png',
                description = translation
            )
        )
    context.bot.answer_inline_query(update.inline_query.id, results)

start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

"""
    do echo handling for text messages in private chats only, but not for messages that come via the bot itself or replies
"""
echo_handler = MessageHandler(Filters.text & Filters.chat_type.private & (~Filters.via_bot(username="@toOgerBot")) & (~Filters.reply)  & (~Filters.command), echo)
dispatcher.add_handler(echo_handler)

inline_translator = InlineQueryHandler(inline_translate)
dispatcher.add_handler(inline_translator)

updater.start_polling()
