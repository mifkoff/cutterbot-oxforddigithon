from functions import *
import telebot
import re

bot = telebot.TeleBot("1244865090:AAEwHmvbWQ_Fu2UsSEvIXj3UY2-YIoQjtIk")


def url_extractor(text):
    return re.findall("(?P<url>https?://[^\s]+)", text)


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Welcome message")  # welcome message


@bot.message_handler(func=lambda message: True)
def echo_all(message):
    text = message.text
    urls = url_extractor(text)
    if len(urls) == 0:
        bot.reply_to(message, "FUCK OFF, I WANT URLS!")  # answer for messages w/o links
    else:
        bot.reply_to(message, "Got it. Will write back when finished!")  # answer for links it gets
        for url in urls:
            if video_id_extractor(url):
                answer = get_video_summary(url)
                bot.send_message(chat_id=message.chat.id, text='Uploading your video 🤪')
                video = open('final_video.mp4', 'rb')
                bot.send_video(message.chat.id, video)

            else:
                page_text = get_page_text(url)
                text_to_speech(page_text),
                answer = get_summary(page_text)
                bot.reply_to(message, answer)
                # Audio
                audio = open(content.audio_file_name, 'rb')
                bot.send_audio(message.chat.id, audio)


bot.polling()
