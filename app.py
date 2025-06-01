# app.py

import os
import time
import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
from datetime import datetime, timedelta
from data_streams import (
    get_fake_price_data,
    get_fake_order_blocks,
    get_fake_news_sentiment
)
from eodhd_options import get_live_order_flow_eodhd
from export_tools import export_signals_to_pdf, send_signals_to_notion
from signal_engine import generate_trade_signals
from contract_selector import get_top_contracts
from options_monitor import display_options_monitor

st.set_page_config(page_title="AetherQuant v2 – Real-Time AI Trade Command Console", layout="wide")

st.title("📡 AetherQuant v2 – Real-Time AI Trade Command Console")

ticker = st.text_input("Enter Ticker Symbol (e.g., QQQ, AAPL)", value="QQQ").upper()
trade_mode = st.radio("Trade Mode", ["Day Trade (0DTE)", "Swing Trade"], horizontal=True)
refresh_toggle = st.checkbox("Auto-refresh data every 60 seconds")

if refresh_toggle:
    time.sleep(60)
    st.experimental_rerun()

if ticker:
    st.markdown("### 📈 Price Data")
    st.markdown("### 📈 Live Price Chart")

try:
    # Fetch past 2 days of 5-minute interval data
    stock_data = yf.download(ticker, period="2d", interval="5m", progress=False)

    if not stock_data.empty:
        fig = go.Figure(data=[
            go.Candlestick(
                x=stock_data.index,
                open=stock_data["Open"],
                high=stock_data["High"],
                low=stock_data["Low"],
                close=stock_data["Close"],
                name="Price"
            )
        ])
        fig.update_layout(title=f"{ticker} – 5min Candlestick Chart", xaxis_rangeslider_visible=False)
        st.plotly_chart(fig, use_container_width=True)

        latest_price = stock_data["Close"].iloc[-1]
        st.success(f"{ticker} price: ${round(latest_price, 2)}")
    else:
        st.warning("No price data available.")
except Exception as e:
    st.error(f"Error fetching chart: {e}")


    st.markdown("### 📦 Order Blocks")
    blocks = get_fake_order_blocks(ticker)
    if blocks:
        for block in blocks:
            st.info(f"{block.get('type', 'Unknown')} Block @ ${block.get('price', '?')} | Volume: {block.get('volume', '?')}")
    else:
        st.warning("No order blocks detected.")

    st.markdown("### 🧠 Option Order Flow")
    try:
        api_key = st.secrets.get("EODHD_API_KEY", os.getenv("EODHD_API_KEY", "demo"))
        flow = get_live_order_flow_eodhd(ticker, api_key)
        if flow:
            st.write(f"Bias: **{flow['bias']}**")
            if flow["unusual_activity"]:
                st.warning("⚠️ Unusual options activity detected!")
            else:
                st.success("No unusual activity detected.")
            st.markdown("#### 🔍 Recent Flow Highlights")
            for item in flow.get("details", []):
                st.markdown(f"- {item}")
        else:
            st.warning("No option flow data available.")
    except Exception as e:
        st.error(f"Error fetching option flow: {e}")
        flow = None

    st.markdown("### 📰 Sentiment & News")
    sentiment = get_fake_news_sentiment(ticker, trade_mode)
    score = sentiment["score"]
    headlines = sentiment["headlines"]
    st.write(f"Sentiment Score: **{score}**")
    for h in headlines:
        st.markdown(f"- {h}")

    st.markdown("### 📌 AI Strategy Trade Signals")
    flow_data = {
        "bias": flow["bias"] if flow else "neutral",
        "unusual_activity": flow["unusual_activity"] if flow else False
    }
    sentiment_data = {
        "score": score,
        "headlines": headlines
    }
    price_data = {
        "price": float(price_output.split("$")[-1])
    }
    mode = "day" if "Day" in trade_mode else "swing"
    signals = generate_trade_signals(price_data, flow_data, sentiment_data, mode)

    st.write("Generated Signals:", signals)

    for sig in signals:
        st.markdown(
    f"**{sig.get('type', 'Unknown')} {sig.get('contract', '')}** → Entry: ${sig.get('entry', '?')} | TP: ${sig.get('target', '?')} | SL: ${sig.get('stop', '?')}"
    )

    pdf_data = export_signals_to_pdf(signals)
    st.download_button("⬇️ Download Signals as PDF", data=pdf_data, file_name="signals.pdf")
    if st.button("📤 Send to Notion"):
        try:
            send_signals_to_notion(signals)
            st.success("Signals sent to Notion!")
        except Exception as e:
            st.error(f"Failed to send to Notion: {e}")

    st.markdown("---")
    st.markdown("### 🧠 Smart Contract Selector")
    contracts = get_top_contracts(ticker)
    for contract in contracts:
        st.markdown(f"- {contract}")

    st.markdown("### 🔍 Options Monitor Tool")
    if st.button("🧪 Run Monitor"):
        display_options_monitor(ticker)
