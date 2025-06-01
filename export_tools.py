from fpdf import FPDF
from notion_client import Client
import datetime

def export_signals_to_pdf(signals, filename="AetherQuant_Signals.pdf"):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(200, 10, "AetherQuant™ AI Trade Signals", ln=True, align="C")
    pdf.ln(10)

    pdf.set_font("Arial", "", 12)
    for i, signal in enumerate(signals):
        pdf.multi_cell(0, 10,
            f"Trade #{i+1}\n"
            f"Contract: {signal['contract']}\n"
            f"Entry: ${signal['entry']} | TP: ${signal['tp']} | SL: ${signal['sl']}\n"
            f"Confidence: {signal['confidence']}%\n"
            f"Reason: {signal['reason']}\n"
            f"{'-'*40}"
        )
        pdf.ln(2)

    pdf.output(filename)

def send_signals_to_notion(signals, notion_token, database_id):
    notion = Client(auth=notion_token)
    for signal in signals:
        notion.pages.create(
            parent={"database_id": database_id},
            properties={
                "Name": {"title": [{"text": {"content": signal["contract"]}}]},
                "Confidence": {"number": float(signal["confidence"])},
                "Entry": {"rich_text": [{"text": {"content": f"${signal['entry']}"}}]},
                "TP": {"rich_text": [{"text": {"content": f"${signal['tp']}"}}]},
                "SL": {"rich_text": [{"text": {"content": f"${signal['sl']}"}}]},
                "Reason": {"rich_text": [{"text": {"content": signal['reason']}}]}
            }
        )
