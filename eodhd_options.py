# eodhd_options.py
import requests
import os

# Set your EODHD API key (can be overridden via environment variable)
EODHD_API_KEY = os.getenv("EODHD_API_KEY", "683bb05655eb24.11196226")

BASE_URL = "https://eodhistoricaldata.com/api"

def get_live_order_flow_eodhd(ticker, api_key=EODHD_API_KEY):
    """
    Simulates live order flow pulled using an API key. Replace with real logic later.
    Returns dict with bias, unusual_activity, and mock detail list.
    """
    return {
        "bias": "neutral",
        "unusual_activity": False,
        "details": [f"No live flow available for {ticker} (API placeholder)."]
    }

def get_qqq_options_chain():
    endpoint = f"{BASE_URL}/options/QQQ.US"
    params = {
        "api_token": EODHD_API_KEY,
        "fmt": "json"
    }

    try:
        response = requests.get(endpoint, params=params)
        response.raise_for_status()
        data = response.json()

        calls = []
        puts = []

        for option in data.get("data", []):
            opt_type = option.get("type")
            opt_data = {
                "symbol": option.get("code"),
                "strike": option.get("strike"),
                "expiration": option.get("expirationDate"),
                "lastPrice": option.get("lastTradePrice"),
                "iv": option.get("impliedVolatility"),
                "delta": option.get("delta"),
                "volume": option.get("volume"),
                "openInterest": option.get("openInterest")
            }
            if opt_type == "call":
                calls.append(opt_data)
            elif opt_type == "put":
                puts.append(opt_data)

        return calls, puts

    except Exception as e:
        print(f"Error fetching QQQ options: {e}")
        return [], []

# Test when run directly
if __name__ == "__main__":
    calls, puts = get_qqq_options_chain()
    print("Top 5 Call Options:")
    for c in calls[:5]:
        print(c)

    print("\nTop 5 Put Options:")
    for p in puts[:5]:
        print(p)
