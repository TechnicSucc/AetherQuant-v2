import random

def get_fake_price_data(ticker):
    price = round(random.uniform(430, 450), 2)
    return f"{ticker} price: ${price}"

def get_fake_order_flow(ticker):
    flows = [
        {"bias": "call", "unusual_activity": True},
        {"bias": "put", "unusual_activity": False},
        {"bias": "neutral", "unusual_activity": False}
    ]
    return random.choice(flows)

def get_fake_order_blocks(ticker):
    return [
        {"type": "Buy", "price": round(random.uniform(435, 440), 2), "volume": random.randint(500, 1000)},
        {"type": "Sell", "price": round(random.uniform(442, 447), 2), "volume": random.randint(600, 1200)},
        {"type": "Cluster", "price": round(random.uniform(438, 445), 2), "volume": random.randint(300, 600)}
    ]

def get_fake_news_sentiment(ticker, mode):
    if "Day" in mode:
        headlines = [
            f"{ticker} surging pre-market after Fed comments",
            f"Volatility high due to CPI data today",
            f"TSLA sympathy move pushing {ticker} higher"
        ]
    else:
        headlines = [
            f"Strong macro outlook for tech — {ticker} bullish swing setup",
            f"Earnings season improving sentiment on {ticker}",
            f"Analysts raise PT for {ticker}"
        ]
    score = round(random.uniform(-1.0, 1.0), 2)
    return {
        "score": score,
        "headlines": random.sample(headlines, 2)
    }
