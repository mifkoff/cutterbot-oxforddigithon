import traceback

from functions import *
import telebot
import re
import config
import database

bot = telebot.TeleBot(config.telegram_access_token)


def url_extractor(text):
    return re.findall("(?P<url>https?://[^\s]+)", text)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    if database.is_user_new(user_id=message.chat.id):
        bot.send_message(chat_id=message.chat.id, text=content.welcome_message)  # welcome message
        database.set_state(user_id=message.chat.id, state='waiting')
    else:
        bot.send_message(chat_id=message.chat.id, text=content.already_in_bot)


@bot.message_handler(commands=['help'])
def send_welcome(message):
    if database.is_user_new(user_id=message.chat.id):
        bot.send_message(chat_id=message.chat.id, text=content.welcome_message)  # welcome message
        database.set_state(user_id=message.chat.id, state='waiting')
    else:
        bot.send_message(chat_id=message.chat.id, text=content.welcome_message)


@bot.message_handler(func=lambda message: True)
def echo_all(message):
    if not database.is_user_new(user_id=message.chat.id) and database.get_state(user_id=message.chat.id) != 'in_progress':
        text = message.text
        urls = url_extractor(text)
        if len(urls) == 0:
            bot.reply_to(message, content.answer_for_message_no_links)
        else:
            database.set_state(user_id=message.chat.id, state='in_progress')
            bot.reply_to(message, content.answer_for_message_with_links)  # answer for links it gets
            for url in urls:
                if video_id_extractor(url):
                    summary_text = get_video_summary(url)
                    if summary_text is not False:
                        bot.send_message(chat_id=message.chat.id, text=content.uploading_in_progress)
                        video = open('final_video.mp4', 'rb')
                        sended_message = bot.send_video(message.chat.id, video)
                        database.new_summary(
                            user_id=message.chat.id,
                            message_id=sended_message.message_id,
                            summary_text=summary_text,
                            url=url,
                            summary_type='video'
                        )
                        database.set_state(user_id=message.chat.id, state='waiting')
                    else:
                        bot.send_message(chat_id=message.chat.id, text=content.cannot_process)
                        database.set_state(user_id=message.chat.id, state='waiting')
                else:
                    page_text = get_page_text(url)
                    if len(page_text) != 0:
                        summary_text = get_summary(page_text)
                        text_to_speech(summary_text)
                        sended_message = bot.reply_to(message, prettify_output(summary_text))
                        # Audio
                        audio = open(content.audio_file_name, 'rb')
                        bot.send_audio(message.chat.id, audio)
                        database.new_summary(
                            user_id=message.chat.id,
                            message_id=sended_message.message_id,
                            summary_text=summary_text,
                            url=url,
                            summary_type='article'
                        )
                        database.set_state(user_id=message.chat.id, state='waiting')
                    else:
                        bot.send_message(chat_id=message.chat.id, text=content.cannot_process)
                        database.set_state(user_id=message.chat.id, state='waiting')
    else:
        bot.send_message(chat_id=message.chat.id, text=content.already_in_progress)


if __name__ == '__main__':
    while True:
        try:
            prettify_output('Started')
            bot.polling()
        except ConnectionError:
            print('ConnectionError', time.time())
            print(traceback.format_exc())
            time.sleep(2)
