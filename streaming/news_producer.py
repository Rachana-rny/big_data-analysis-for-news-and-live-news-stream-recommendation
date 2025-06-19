import requests
import json
from kafka import KafkaProducer
import time
import pandas as pd
import os

print("⏳ Starting GNews News Producer...")

# Kafka producer setup
producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

print("✅ Kafka Producer connected!")

API_KEY = "e3e8a660463ceff69055358487e"
URL = f"https://gnews.io/api/v4/top-headlines?token={API_KEY}&lang=en&country=in&max=100"

CSV_PATH = "/home/rachana/rtbda news/data/recommended_news.csv"

while True:
    print("🌐 Fetching news from GNews...")
    response = requests.get(URL)
    print(f"📦 API response code: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        articles = data.get("articles", [])
        
        if not articles:
            print("⚠️ No articles found.")
        else:
            news_list = []
            for article in articles:
                print(f"📰 Sending article: {article['title']}")
                producer.send("news", article)
                news_list.append({
                    "title": article['title'],
                    "description": article.get("description", ""),
                    "url": article["url"],
                    "publishedAt": article["publishedAt"]
                })

            # ✅ Save to CSV (append mode)
            df = pd.DataFrame(news_list)

            if os.path.exists(CSV_PATH):
                df.to_csv(CSV_PATH, mode='a', header=False, index=False)
            else:
                df.to_csv(CSV_PATH, index=False)

            print(f"✅ Saved {len(news_list)} articles to {CSV_PATH}")

    else:
        print(f"❌ Error fetching news: {response.text}")

    print("✅ Finished sending articles. Sleeping for 60s...\n")
    time.sleep(10)
