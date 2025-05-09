import requests
import openai

# Telegram
TOKEN = "7270680340:AAENSNCCoXsL40voZF2tS_-gP6EtKO_KJn0"
CHAT_ID = "8058541002"

# OpenAI
import os
openai.api_key = os.getenv("OPENAI_API_KEY")
# NewsAPI
NEWS_API_KEY = "824a8c4a436447d8a46378005c7744ec"

def get_news_headlines():
    url = f"https://newsapi.org/v2/top-headlines?language=en&category=technology&pageSize=5&apiKey={NEWS_API_KEY}"
    response = requests.get(url)
    articles = response.json().get("articles", [])
    headlines = [a["title"] for a in articles if a.get("title")]
    return headlines

def summarize_with_openai(headlines):
    prompt = (
        "Aşağıda İngilizce haber başlıkları verilmiştir. "
        "Her başlığı Türkçe olarak özetle ve anlamlı bir şekilde sırala:\n\n"
    )
    for i, h in enumerate(headlines, 1):
        prompt += f"{i}. {h}\n"

    prompt += "\nTürkçe özetlenmiş hali:\n"

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
    )

    return response["choices"][0]["message"]["content"]

def send_telegram_message(text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": text,
        "parse_mode": "Markdown"
    }
    requests.post(url, data=payload)

def main():
    headlines = get_news_headlines()
    summary = summarize_with_openai(headlines)
    send_telegram_message("🧠 *OpenAI Destekli Haber Özeti:*\n\n" + summary)

if __name__ == "__main__":
    main()
