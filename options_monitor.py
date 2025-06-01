# options_monitor.py

import streamlit as st
from contract_selector import get_top_contracts

def display_options_monitor(ticker: str, contract_type: str):
    st.subheader("📈 Options Monitor")
    st.write(f"Monitoring contracts for **{ticker}**")

    contracts = get_top_contracts(ticker)

    if contract_type != "both":
        contracts = [c for c in contracts if c["type"] == contract_type]

    call_contracts = [c for c in contracts if c["type"] == "call"]
    put_contracts = [c for c in contracts if c["type"] == "put"]

    st.markdown("**Top 5 Call Contracts:**")
    for c in call_contracts[:5]:
        st.code(f'{c["symbol"]} | Strike: {c["strike"]} | Exp: {c["expiration"]}')

    st.markdown("**Top 5 Put Contracts:**")
    for p in put_contracts[:5]:
        st.code(f'{p["symbol"]} | Strike: {p["strike"]} | Exp: {p["expiration"]}')
