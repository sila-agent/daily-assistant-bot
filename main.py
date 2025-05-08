from telegram.ext import Updater, CommandHandler
import logging
import datetime
import time
import threading
import json
from datetime import datetime

TOKEN = "7270680340:AAENSNCCoXsL40voZF2tS_-gP6EtKO_KJn0"

def start(update, context):
    update.message.reply_text("Merhaba! Asistan botun göreve hazır.")

def send_daily_message(context):
    chat_id = context.job.context
    context.bot.send_message(chat_id=chat_id, text="Günaydın! Hazırsan sana özel gündem geliyor.")

def daily_scheduler(updater, chat_id):
    job_queue = updater.job_queue
    job_queue.run_daily(send_daily_message, time=datetime.time(hour=8, minute=0), context=chat_id)
    job_queue.run_daily(send_certificate_updates, time=datetime.time(hour=10, minute=0), context=chat_id)

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
                    return
            time.sleep(1)

    threading.Thread(target=wait_for_chat_id).start()
    updater.idle()

if __name__ == '__main__':
    main()
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
