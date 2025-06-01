# contract_selector.py

def get_top_contracts(ticker: str):
    """
    Simulate retrieving the top call/put options for the given ticker.
    Replace this with your live Polygon or Tradier logic.
    """
    contracts = [
        {"symbol": f"O:{ticker}250602C00400000", "type": "call", "expiration": "2025-06-02", "strike": 400},
        {"symbol": f"O:{ticker}250602C00405000", "type": "call", "expiration": "2025-06-02", "strike": 405},
        {"symbol": f"O:{ticker}250602P00400000", "type": "put",  "expiration": "2025-06-02", "strike": 400},
        {"symbol": f"O:{ticker}250602P00395000", "type": "put",  "expiration": "2025-06-02", "strike": 395},
    ]

    return contracts
