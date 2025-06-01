import random
import requests

def get_fake_price_data(ticker):
    price = round(random.uniform(430, 450), 2)
    return f"{ticker} price: ${price}"

def get_live_order_flow_eodhd(ticker, api_key):
    url = f"https://eodhd.com/api/options/{ticker}.US?api_token=683bb05655eb24.11196226"
    response = requests.get(url)
    
    if response.status_code != 200:
        return {"bias": "neutral", "unusual_activity": False, "details": ["Failed to fetch data."]}

    data = response.json()
    calls = data.get("data", {}).get("CALL", [])
    puts = data.get("data", {}).get("PUT", [])

    call_volume = sum(opt.get("volume", 0) for opt in calls)
    put_volume = sum(opt.get("volume", 0) for opt in puts)

    unusual_call = any(opt.get("volume", 0) > 2 * opt.get("open_interest", 1) for opt in calls)
    unusual_put = any(opt.get("volume", 0) > 2 * opt.get("open_interest", 1) for opt in puts)

    bias = "call" if call_volume > put_volume else "put" if put_volume > call_volume else "neutral"
    details = [
        f"Call volume: {call_volume}",
        f"Put volume: {put_volume}"
    ]

    return {
        "bias": bias,
        "unusual_activity": unusual_call or unusual_put,
        "details": details
    }


def get_fake_order_blocks(ticker):
    return [
        {"type": "Buy", "price": round(random.uniform(435, 440), 2), "volume": random.randint(500, 1000)},
        {"type": "Sell", "price": round(random.uniform(442, 447), 2), "volume": random.randint(600, 1200)},
        {"type": "Cluster", "price": round(random.uniform(438, 445), 2), "volume": random.randint(300, 600)}
    ]

def get_fake_news_sentiment(ticker, mode):
    score = round(random.uniform(-1, 1), 2)
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
    return {
        "score": score,
        "headlines": headlines
    }

