import telebot
import time
import feedparser
from six.moves import urllib
import datetime

bot_token =  '740233654:AAFTi6vHYvMu2KGwHzLaFazMXuptVYXOZfg'

bot = telebot.TeleBot(token = bot_token)
 
def find_audio():
    start = '<img src="'
    end = '\" height'
    NewsFeed = feedparser.parse("http://feed.desiringgod.org/solid-joys-audio.rss")
    entry = NewsFeed.entries[1]
    summary_detail = entry.summary_detail.value
    image_link = ((summary_detail.split(start))[1].split(end)[0])
    return image_link,entry.subtitle,entry.links[1].href

def find_at(msg):
    for text in msg:
        if '@' in text:
            return text

@bot.message_handler(commands=['start'])
def send_wellcome(message):
    bot.reply_to(message,"Welcome! ")
    bot.send_message(chat_id =message.chat.id,text ="Solid Joys is a daily devotional written and read by John Piper. These short and substantive readings will feed your joy in Jesus every day of the year. Discover more from Piper at desiringGod.org.")

@bot.message_handler(commands=['help'])
def send_help(message):
    bot.reply_to(message,"Use /audio to get Sermon of the day ")

@bot.message_handler(commands=['audio'])
def send_audio(message):
    now = datetime.datetime.now()
    date = str(now.day)+str(now.month)+str(now.year)
    chat_id = message.chat.id
    image_link,subtitle,audio_url = find_audio()
    output_file = "daily_dev.mp3"
    urllib.request.urlretrieve(audio_url, output_file)
    bot.send_message(chat_id=chat_id,text = subtitle)
    bot.send_audio(chat_id=chat_id, audio=open(output_file, 'rb'))



while True:
    try:
        bot.polling()
    except Exception:
        time.sleep(15)