import telebot
import re

bot = telebot.TeleBot("1244865090:AAEwHmvbWQ_Fu2UsSEvIXj3UY2-YIoQjtIk")


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	bot.reply_to(message, "Howdy, how are you doing?")


def url_extractor(text):
	return re.search("(?P<url>https?://[^\s]+)", text.lower()).group("url")


@bot.message_handler(func=lambda message: True)
def echo_all(message):
	bot.reply_to(message, message.text)


def echo_all(message):
	text = message.text
	urls = url_extractor(text)
	if len(urls) == 0:
		bot.reply_to(message, "FUCK OFF, I WANT URLS!")
	else:
		for url in urls:
			answer = get_video_summary(urls)
	bot.reply_to(message, answer)


bot.polling()
