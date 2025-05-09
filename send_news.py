import requests
from googletrans import Translator

# Telegram bot token ve chat ID
TOKEN = "7270680340:AAENSNCCoXsL40voZF2tS_-gP6EtKO_KJn0"
CHAT_ID = "8058541002"

# News API anahtarı
NEWS_API_KEY = "824a8c4a436447d8a46378005c7744ec"

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

def send_message(text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": text,
        "parse_mode": "Markdown"
    }
    requests.post(url, data=payload)

def main():
    general_news = get_translated_news("general")
    tech_news = get_translated_news("technology")

    message = "🗞️ *GÜNLÜK HABER ÖZETİ*\n\n"
    message += "*Genel Dünya Gündemi:*\n" + "\n".join(general_news) + "\n\n"
    message += "*Teknoloji Gündemi:*\n" + "\n".join(tech_news)

    send_message(message)

if __name__ == "__main__":
    main()
