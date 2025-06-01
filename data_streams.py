import random

def get_fake_price_data(ticker):
    price = round(random.uniform(430, 450), 2)
    return f"{ticker} price: ${price}"

def get_fake_order_flow(ticker):
    descriptions = [
        f"{ticker} 0DTE $445C — 1,200 contracts @ $2.35 (sweep)",
        f"{ticker} 1W $430P — 900 contracts @ $1.10 (block trade)",
        f"{ticker} $440C — rising open interest"
    ]
    return {
        "bias": random.choice(["call", "put", "neutral"]),
        "unusual_activity": random.choice([True, False]),
        "note": random.choice(descriptions)
    }

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
