import traceback

from functions import *
import telebot
import re
import config
import database

bot = telebot.TeleBot(config.telegram_access_token)


def url_extractor(text):
    return re.findall("(?P<url>https?://[^\s]+)", text)


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    if database.is_user_new(user_id=message.chat.id):
        database.new_user(user_id=message.chat.id)
        bot.send_message(chat_id=message.chat.id, text="Welcome message")  # welcome message
        database.set_state(user_id=message.chat.id, state='waiting')
    else:
        bot.send_message(chat_id=message.chat.id, text='Already in bot')  # TODO change


@bot.message_handler(func=lambda message: True)
def echo_all(message):
    if database.get_state(user_id=message.chat.id) != 'waiting':
        text = message.text
        urls = url_extractor(text)
        if len(urls) == 0:
            bot.reply_to(message, "FUCK OFF, I WANT URLS!")  # answer for messages w/o links
        #     TODO all texts to content file
        else:
            database.set_state(user_id=message.chat.id, state='waiting')
            bot.reply_to(message, "Got it. Will write back when finished!")  # answer for links it gets
            for url in urls:
                if video_id_extractor(url):
                    summary_text = get_video_summary(url)
                    if summary_text is not False:
                        bot.send_message(chat_id=message.chat.id, text='Uploading your video 🤪')
                        video = open('final_video.mp4', 'rb')
                        sended_message = bot.send_video(message.chat.id, video)
                        database.new_summary(
                            user_id=message.chat.id,
                            message_id=sended_message.message_id,
                            summary_text=summary_text,
                            url=url,
                            summary_type='video'
                        )
                    else:
                        bot.send_message(chat_id=message.chat.id, text='cannot do that')
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
                    else:
                        bot.send_message(chat_id=message.chat.id, text='cannot do that')
    else:
        bot.send_message(chat_id=message.chat.id, text='Your summary is in progress')


if __name__ == '__main__':
    while True:
        try:
            prettify_output('Started')
            bot.polling()
        except ConnectionError:
            print('ConnectionError', time.time())
            print(traceback.format_exc())
            time.sleep(2)
