import os
import openai
import requests

# Telegram bilgileri
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("8058541002")

# OpenAI API
openai.api_key = os.getenv(
")

# NewsAPI
NEWS_API_KEY = os.getenv("824a8c4a436447d8a46378005c7744ec")

def get_headlines():
    url = f"https://newsapi.org/v2/top-headlines?language=en&category=technology&pageSize=5&apiKey={NEWS_API_KEY}"
    response = requests.get(url)
    data = response.json()
    return [a["title"] for a in data.get("articles", []) if a.get("title")]

def summarize(headlines):
    joined = "\n".join(f"{i+1}. {h}" for i, h in enumerate(headlines))
    prompt = f"Aşağıdaki İngilizce haber başlıklarını Türkçeye çevirerek kısa, sade özetler üret:\n\n{joined}\n\nÖzet:"
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{ "role": "user", "content": prompt }],
        temperature=0.7
    )
    return response["choices"][0]["message"]["content"]

def send_telegram_message(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = { "chat_id": CHAT_ID, "text": text, "parse_mode": "Markdown" }
    requests.post(url, data=payload)

def main():
    headlines = get_headlines()
    summary = summarize(headlines)
    send_telegram_message(f"🧠 *Günlük Haber Özeti:*\n\n{summary}")

if __name__ == "__main__":
    main()
