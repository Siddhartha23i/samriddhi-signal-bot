# messenger.py
# Responsible for ONE thing only: sending a message to a Signal user.
# It calls the signal-cli REST API which forwards the message to Signal's servers.

import httpx
import os
from dotenv import load_dotenv

load_dotenv()

SIGNAL_API_URL = os.getenv("SIGNAL_API_URL")  # e.g. http://localhost:8080
BOT_PHONE = os.getenv("BOT_PHONE")            # Your registered Signal number


async def send_message(recipient: str, text: str):
    """
    Sends a text message to a Signal user.

    Args:
        recipient: The user's phone number in international format, e.g. "+91XXXXXXXXXX"
        text:      The message string to send
    """
    url = f"{SIGNAL_API_URL}/v2/send"
    payload = {
        "message": text,
        "number": BOT_PHONE,
        "recipients": [recipient]
    }
    async with httpx.AsyncClient(timeout=30) as client:
        try:
            response = await client.post(url, json=payload)
            print(f"[SEND] Status: {response.status_code} Body: {response.text}")
            response.raise_for_status()
        except Exception as e:
            print(f"[SEND ERROR] {type(e).__name__}: {e}")
