# signal_engine.py

import random

def generate_trade_signals(price_data, flow_data, sentiment_data, mode="day"):
    """
    Combines price, flow, and sentiment data to produce AI-based options trade signals.
    Returns a list of signal dictionaries.
    """
    # Simulate mock confidence scores (real version would use ML models)
    confidence = round(random.uniform(78, 95), 2)
    
    sentiment_score = sentiment_data.get("score", 0)
    flow_bias = flow_data.get("bias", "neutral")
    
    direction = "bullish" if sentiment_score > 0.2 and flow_bias == "call" else "bearish"

    if direction == "bullish":
        contract = "QQQ 06/07 $440C"
        entry = 2.15
        tp = 3.50
        sl = 1.35
    else:
        contract = "QQQ 06/07 $435P"
        entry = 2.05
        tp = 3.25
        sl = 1.30

    signal = {
        "symbol": "QQQ",
        "contract": contract,
        "entry": entry,
        "tp": tp,
        "sl": sl,
        "confidence": confidence,
        "strategy": f"{direction.title()} Momentum",
        "reason": f"Strong {direction} setup from sentiment ({sentiment_score}) and order flow ({flow_bias})."
    }

    return [signal]
