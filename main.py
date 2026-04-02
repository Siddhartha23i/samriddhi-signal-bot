# main.py
# FastAPI webhook server for Samriddhi Anveshana Signal Bot.
# signal-cli (json-rpc mode) pushes incoming messages here via POST /webhook.

from fastapi import FastAPI, Request
from bot_logic import handle_message
import os
from dotenv import load_dotenv

load_dotenv()

SIGNAL_API_URL = os.getenv("SIGNAL_API_URL")
BOT_PHONE = os.getenv("BOT_PHONE")

app = FastAPI(
    title="Samriddhi Anveshana Signal Bot",
    description="Signal chatbot for Samriddhi Anveshana healthcare services",
    version="1.0.0"
)


@app.get("/")
def health():
    """Health check — visit this URL to confirm the bot is running."""
    return {"status": "🟢 Samriddhi Anveshana Signal Bot is running"}


@app.post("/webhook")
async def webhook(request: Request):
    """
    Receives incoming Signal messages from signal-cli (json-rpc mode).
    signal-cli POSTs here every time a user messages the bot's number.
    """
    body = await request.json()
    try:
        envelope = body.get("envelope", {})
        sender = envelope.get("source")
        data_message = envelope.get("dataMessage", {})
        text = data_message.get("message", "")
        if sender and text and sender != BOT_PHONE:
            print(f"[MSG] From {sender}: {text}")
            await handle_message(sender, text)
    except Exception as e:
        print(f"[ERROR] {e}")
    # Always return 200 — if we return non-200, signal-cli retries and spams the user
    return {"status": "ok"}