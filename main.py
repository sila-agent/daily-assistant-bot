from telegram.ext import Updater, CommandHandler
import logging
import datetime
import time
import threading
import json
import requests
from googletrans import Translator
from datetime import datetime

# Telegram Bot Token
TOKEN = "7270680340:AAENSNCCoXsL40voZF2tS_-gP6EtKO_KJn0"

# NewsAPI Key
NEWS_API_KEY = "824a8c4a436447d8a46378005c7744ec"

# /start komutu
def start(update, context):
    update.message.reply_text("Merhaba! Asistan botun göreve hazır.")

# Günaydın mesajı
def send_daily_message(context):
    chat_id = context.job.context
    context.bot.send_message(chat_id=chat_id, text="Günaydın! Hazırsan sana özel gündem geliyor.")

# Sertifika bildirimleri
def send_certificate_updates(context):
    chat_id = context.job.context
    try:
        with open("certificate_list.json", "r", encoding="utf-8") as f:
            data = json.load(f)

        today = datetime.today().strftime("%d %B %Y")
        message = f"[GÜNCEL SERTİFİKA FIRSATLARI – {today}]\n\n"

        for cert in data:
            title = cert.get("title", "Bilinmeyen")
            deadline = cert.get("deadline", "Yok")
            link = cert.get("link", "#")
            message += f"**{title}**\n→ Başvuru Son Tarihi: {deadline}\n→ [Detaylı Bilgi]({link})\n\n"

        context.bot.send_message(chat_id=chat_id, text=message, parse_mode="Markdown")
    except Exception as e:
        context.bot.send_message(chat_id=chat_id, text=f"Sertifika verisi okunamadı: {str(e)}")

# Haber çekme ve çeviri
def get_translated_news(category):
    url = f"https://newsapi.org/v2/top-headlines?language=en&category={category}&pageSize=3&apiKey={NEWS_API_KEY}"
    response = requests.get(url)
    data = response.json()

    translator = Translator()
    news_items = []

    if data.get("articles"):
        for article in data["articles"]:
            title_en = article.get("title", "")
            if title_en:
                translated = translator.translate(title_en, src="en", dest="tr")
                news_items.append(f"- {translated.text}")
    return news_items

# Haber mesajı gönder
def send_daily_news(context):
    chat_id = context.job.context
    try:
        general_news = get_translated_news("general")
        tech_news = get_translated_news("technology")

        message = "🗞️ *GÜNLÜK HABER ÖZETİ*\n\n"
        message += "*Genel Dünya Gündemi:*\n" + "\n".join(general_news) + "\n\n"
        message += "*Teknoloji Gündemi:*\n" + "\n".join(tech_news)

        context.bot.send_message(chat_id=chat_id, text=message, parse_mode="Markdown")
    except Exception as e:
        context.bot.send_message(chat_id=chat_id, text=f"Haber alınamadı: {str(e)}")

# Zamanlayıcı
def daily_scheduler(updater, chat_id):
    job_queue = updater.job_queue
    job_queue.run_daily(send_daily_message, time=datetime.time(hour=8, minute=0), context=chat_id)
    job_queue.run_daily(send_daily_news, time=datetime.time(hour=9, minute=0), context=chat_id)
    job_queue.run_daily(send_certificate_updates, time=datetime.time(hour=10, minute=0), context=chat_id)

# Ana fonksiyon
def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    updater.start_polling()

    def wait_for_chat_id():
        while True:
            updates = updater.bot.get_updates()
            for update in updates:
                if update.message:
                    chat_id = update.message.chat_id
                    daily_scheduler(updater, chat_id)

                    # TEST: Haber mesajını anında gönder
                    send_daily_news(type("obj", (object,), {
                        "bot": updater.bot,
                        "job": type("j", (), {"context": chat_id})
                    })())

                    return
            time.sleep(1)

    threading.Thread(target=wait_for_chat_id).start()
    updater.idle()

if __name__ == '__main__':
    main()
