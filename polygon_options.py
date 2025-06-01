# polygon_options.py
import requests
import os

POLYGON_API_KEY = "7iUiUpNffoYBcmX2x99mUfoW5MuZKPS3"

BASE_URL = "https://api.polygon.io/v3/reference/options/contracts"


def get_qqq_options():
    url = f"{BASE_URL}"
    params = {
        "underlying_ticker": "QQQ",
        "limit": 20,
        "apiKey": POLYGON_API_KEY
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        contracts = response.json().get("results", [])

        calls = []
        puts = []

        for option in contracts:
            opt_data = {
                "symbol": option.get("ticker"),
                "type": option.get("contract_type"),
                "expiration": option.get("expiration_date"),
                "strike": option.get("strike_price")
            }
            if option["contract_type"] == "call":
                calls.append(opt_data)
            elif option["contract_type"] == "put":
                puts.append(opt_data)

        return calls, puts

    except Exception as e:
        print(f"Error fetching Polygon QQQ options: {e}")
        return [], []


if __name__ == "__main__":
    calls, puts = get_qqq_options()
    print("Top 5 Call Contracts:")
    for c in calls[:5]:
        print(c)

    print("\nTop 5 Put Contracts:")
    for p in puts[:5]:
        print(p)
