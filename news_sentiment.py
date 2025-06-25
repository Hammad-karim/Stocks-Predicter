import requests
import pandas as pd
from textblob import TextBlob
import matplotlib.pyplot as plt

# --- Step 1: API Setup ---
API_KEY = '568c69b7ed0b482ba9174d935531f9aa'
NEWS_URL = f'https://newsapi.org/v2/top-headlines?category=business&language=en&pageSize=100&apiKey={API_KEY}'

# --- Step 2: Fetch News Headlines ---
response = requests.get(NEWS_URL)
data = response.json()

headlines = []
if data.get("status") == "ok":
    articles = data.get("articles", [])
    for article in articles:
        title = article.get("title")
        if title:
            headlines.append(title)
else:
    print("Error fetching news:", data.get("message"))

# --- Step 3: Analyze Sentiment ---
def get_sentiment(text):
    analysis = TextBlob(text)
    polarity = analysis.sentiment.polarity
    if polarity > 0:
        return 'Positive'
    elif polarity < 0:
        return 'Negative'
    else:
        return 'Neutral'

df = pd.DataFrame(headlines, columns=["Headline"])
df["Sentiment"] = df["Headline"].apply(get_sentiment)

# --- Step 4: Display Summary ---
print("\nSentiment Breakdown:")
print(df["Sentiment"].value_counts())
print("\nSample Headlines with Sentiment:")
print(df.head(10))

# --- Step 5: Plot Sentiment Pie Chart ---
plt.figure(figsize=(6, 6))
df["Sentiment"].value_counts().plot.pie(autopct='%1.1f%%', colors=['lightgreen', 'lightcoral', 'lightblue'])
plt.title("Sentiment Distribution of Business News")
plt.ylabel("")
plt.show()

# --- Step 6: Save to CSV ---
df.to_csv("news_sentiment_results.csv", index=False)
print("\n✅ Results saved to 'news_sentiment_results.csv'")
