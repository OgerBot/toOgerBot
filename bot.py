# coding=utf-8
from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters
from telegram import InlineQueryResultArticle, InputTextMessageContent, InlineQueryResultVoice
from telegram.ext import InlineQueryHandler
from translate import OgerTranslator
import logging
import random

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

token = open("token.SECRET").read().replace("\n", "")
updater = Updater(token=token, use_context=True)
dispatcher = updater.dispatcher

audios = open("audios.csv", "r", encoding="utf-8").read().split("\n")[0:-1]
random.shuffle(audios)
audio_files = []
audio_titles = []
audio_titles_lowered = []
for audio in audios:
    audio = audio.split(";")
    audio_files.append(audio[0])
    audio_titles.append(audio[1])
    audio_titles_lowered.append(audio[1].lower())
audios = None


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

    audio_id = []
    if 2 < len(query) < 16:
        for i in range(len(audio_titles)):
            if query.lower() in audio_titles_lowered[i]:
                audio_id.append(i)
                if len(audio_id) == 3:
                    break

    if audio_id == [] and (not query or len(query) < 16):
        audio_id = [random.randint(0, len(audio_titles))]

    for aud_id in audio_id:
        audiofile, title = audio_files[aud_id], audio_titles[aud_id]
        #title = OgerTranslator.translate(title)
        results.append(InlineQueryResultVoice(
            id = "voice"+str(aud_id),
            voice_url  = audiofile,
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
                thumb_url = 'https://www.oger.ml/oger.png',
                description = translation
            )
        )
    results.reverse()
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
