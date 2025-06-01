# price_stream.py

import websocket
import json
import os

ALPACA_WS = "wss://stream.data.alpaca.markets/v2/iex"
ALPACA_API_KEY = os.getenv("ALPACA_API_KEY")
ALPACA_SECRET = os.getenv("ALPACA_SECRET")

def on_message(ws, message):
    data = json.loads(message)
    print("📡", data)

def on_error(ws, error):
    print("❌ WebSocket error:", error)

def on_close(ws, close_status_code, close_msg):
    print("🔒 WebSocket closed")

def on_open(ws):
    print("🔑 WebSocket opened")
    auth_msg = {
        "action": "auth",
        "key": ALPACA_API_KEY,
        "secret": ALPACA_SECRET
    }
    ws.send(json.dumps(auth_msg))
    listen_msg = {
        "action": "subscribe",
        "trades": ["QQQ"]
    }
    ws.send(json.dumps(listen_msg))

if __name__ == "__main__":
    websocket.enableTrace(True)
    ws_app = websocket.WebSocketApp(ALPACA_WS,
                                    on_open=on_open,
                                    on_message=on_message,
                                    on_error=on_error,
                                    on_close=on_close)
    ws_app.run_forever()
