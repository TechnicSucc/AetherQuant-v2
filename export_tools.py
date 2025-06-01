from fpdf import FPDF
from notion_client import Client
from io import BytesIO

def export_signals_to_pdf(signals):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    pdf.set_font("Arial", "B", 16)
    pdf.cell(200, 10, "AetherQuant AI Trade Signals", ln=True, align="C")
    pdf.ln(10)

    pdf.set_font("Arial", "", 12)
    for i, signal in enumerate(signals):
        contract = str(signal.get("contract", "N/A"))
        entry = str(signal.get("entry", "N/A"))
        tp = str(signal.get("tp", "N/A"))
        sl = str(signal.get("sl", "N/A"))
        confidence = str(signal.get("confidence", "N/A"))
        reason = str(signal.get("reason", "No reason provided")).replace("™", "")

        text = (
            f"Trade #{i+1}\n"
            f"Contract: {contract}\n"
            f"Entry: ${entry} | TP: ${tp} | SL: ${sl}\n"
            f"Confidence: {confidence}%\n"
            f"Reason: {reason}\n"
            f"{'-'*40}"
        )
        pdf.multi_cell(0, 10, text)
        pdf.ln(2)

    # Return binary content as BytesIO object
    pdf_binary = pdf.output(dest='S').encode('latin1')
    return BytesIO(pdf_binary)

def send_signals_to_notion(signals, notion_token, database_id):
    notion = Client(auth=notion_token)
    for signal in signals:
        notion.pages.create(
            parent={"database_id": database_id},
            properties={
                "Name": {"title": [{"text": {"content": str(signal.get("contract", "Unnamed"))}}]},
                "Confidence": {"number": float(signal.get("confidence", 0))},
                "Entry": {"rich_text": [{"text": {"content": f"${signal.get('entry', 'N/A')}"}}]},
                "TP": {"rich_text": [{"text": {"content": f"${signal.get('tp', 'N/A')}"}}]},
                "SL": {"rich_text": [{"text": {"content": f"${signal.get('sl', 'N/A')}"}}]},
                "Reason": {"rich_text": [{"text": {"content": signal.get('reason', 'No reason provided')}}]}
            }
        )
