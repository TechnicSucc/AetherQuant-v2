# app.py

import streamlit as st
import pandas as pd
import os
import time
from contract_selector import get_top_contracts
from signal_engine import generate_trade_signals
from options_monitor import display_options_monitor
from data_streams import (
    get_fake_price_data,
    get_fake_order_flow,
    get_fake_order_blocks,
    get_fake_news_sentiment,
)
from export_tools import export_signals_to_pdf, send_signals_to_notion

st.set_page_config(page_title="AetherQuant v2 – Real-Time AI Trade Command Console", layout="wide")

st.title("📡 AetherQuant v2 – Real-Time AI Trade Command Console")


# --- Sidebar ---
with st.sidebar:
    st.subheader("⚙️ Trading Setup")
    ticker = st.text_input("Enter Ticker Symbol", value="QQQ")
    timeframe = st.selectbox("Select Timeframe", options=["1m", "2m", "5m"])
    trade_mode = st.radio("Trade Mode", ["Day Trade (0DTE)", "Swing Trade"])
    refresh_toggle = st.checkbox("🔄 Auto-Refresh Every 60s")

if refresh_toggle:
    time.sleep(60)
    st.experimental_rerun()


# --- Dashboard Sections ---
from data_streams import get_fake_price_data

st.markdown("### 📈 Price Stream")
price_output = get_fake_price_data(ticker)
st.success(price_output)

st.markdown("### 📦 Order Blocks")
blocks = get_fake_order_blocks(ticker)
for block in blocks:
    st.info(f"{block['type']} Block @ ${block['price']} | Volume: {block['volume']}")

st.markdown("### 🧠 Option Order Flow")
flow = get_fake_order_flow(ticker)
st.write(f"Bias: **{flow['bias']}**")
if flow["unusual_activity"]:
    st.warning("⚠️ Unusual options activity detected!")
else:
    st.success("✅ No unusual activity detected.")

st.markdown("### 📰 Sentiment & News")
sentiment = get_fake_news_sentiment(ticker)

score = sentiment["score"]
headlines = sentiment["headlines"]

if score > 0.2:
    st.success(f"🟢 Bullish Sentiment | Score: {score}")
elif score < -0.2:
    st.error(f"🔴 Bearish Sentiment | Score: {score}")
else:
    st.info(f"⚪ Neutral Sentiment | Score: {score}")

st.markdown("**Latest Headlines:**")
for h in headlines:
    st.markdown(f"- {h}")

# --- Options Monitor ---
st.markdown("### 📊 Options Monitor")

with st.expander("📍 Scan Available Option Contracts"):
    ticker_input = st.text_input("🔎 Ticker", value="QQQ", key="opt_ticker")
    contract_type = st.selectbox("Contract Type", ["both", "call", "put"], key="opt_type")

    if st.button("🧪 Run Monitor"):
        st.info(f"Fetching live options for {ticker_input.upper()}...")
        display_options_monitor(ticker_input, contract_type)


# --- Strategy Signals ---
st.markdown("### 📌 AI Strategy Trade Signals")
contracts = get_top_contracts(ticker_input)
# Mock inputs (replace with real streaming data in production)
price_data = {
    "latest": 441.23,
    "open": 440.5,
    "high": 442.1,
    "low": 439.8,
    "volume": 12039823
}

flow_data = {
    "bias": "call",  # or "put", or "neutral"
    "unusual_activity": True
}

sentiment_data = {
    "score": 0.3,  # Range: -1 (bearish) to 1 (bullish)
    "headlines": [
        "Tech stocks rally as traders bet on rate cuts",
        "Positive sentiment builds around NASDAQ gains"
    ]
}

st.markdown("### 📤 Export Trade Signals")

col1, col2 = st.columns(2)

with col1:
    if st.button("📄 Download PDF"):
        export_signals_to_pdf(signals)
        st.success("PDF saved as AetherQuant_Signals.pdf")

with col2:
    notion_token = st.text_input("🔐 Notion API Token", type="password")
    db_id = st.text_input("🧱 Notion Database ID")

    if st.button("🚀 Send to Notion"):
        if notion_token and db_id:
            send_signals_to_notion(signals, notion_token, db_id)
            st.success("Signals pushed to Notion!")
        else:
            st.warning("Enter both Notion token and database ID.")


# Determine mode based on sidebar selection
mode = "day" if trade_mode == "Day Trade (0DTE)" else "swing"

st.markdown("### 📌 AI Strategy Trade Signals")

signals = generate_trade_signals(price_data, flow_data, sentiment_data, mode)

for sig in signals:
    st.markdown(f"#### 💡 Strategy: {sig['strategy']}")
    st.code(
        f"{sig['contract']} | Entry: ${sig['entry']} | TP: ${sig['tp']} | SL: ${sig['sl']}"
    )
    st.write(f"🧠 Confidence: **{sig['confidence']}%**")
    st.write(f"📌 Reason: {sig['reason']}")
    st.markdown("---")

st.markdown("### 🧾 Strategy Recap")

st.write(f"🧠 Mode: **{'Day Trade' if mode == 'day' else 'Swing Trade'}**")
st.write(f"📉 Flow Bias: **{flow_data['bias']}**")
st.write(f"📰 Sentiment Score: **{sentiment_data['score']}**")
st.write(f"🎯 Contracts Evaluated: **{len(contracts)}**")
st.write(f"✅ Signals Generated: **{len(signals)}**")

# Dummy comment


