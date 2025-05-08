from telegram.ext import Updater, CommandHandler
import logging
import datetime
import time
import threading

TOKEN = "7270680340:AAENSNCCoXsL40voZF2tS_-gP6EtKO_KJn0"

def start(update, context):
    update.message.reply_text("Merhaba! Asistan botun göreve hazır.")

def send_daily_message(context):
    chat_id = context.job.context
    context.bot.send_message(chat_id=chat_id, text="Günaydın! Hazırsan sana özel gündem geliyor.")

def daily_scheduler(updater, chat_id):
    job_queue = updater.job_queue
    job_queue.run_daily(send_daily_message, time=datetime.time(hour=8, minute=0), context=chat_id)

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
