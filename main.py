# main.py
# FastAPI webhook server for Samriddhi Anveshana Signal Bot.
# signal-cli (json-rpc mode) pushes incoming messages here via POST /webhook.

from fastapi import FastAPI, Request
from bot_logic import handle_message
import asyncio
import httpx
import os
from dotenv import load_dotenv

load_dotenv()

SIGNAL_API_URL = os.getenv("SIGNAL_API_URL")
BOT_PHONE = os.getenv("BOT_PHONE")
BOT_URL = os.getenv("BOT_URL", "")  # e.g. https://samriddhi-signal-bot.onrender.com

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


async def keep_alive():
    """
    Pings both Render services every 5 minutes so neither spins down.
    Also re-registers the webhook every 10 minutes in case signal-cli restarted.
    """
    print("[KEEP-ALIVE] Started keep-alive loop")
    cycle = 0
    async with httpx.AsyncClient(timeout=30) as client:
        while True:
            await asyncio.sleep(300)  # every 5 minutes
            cycle += 1
            try:
                # Ping signal-cli to keep it awake
                await client.get(f"{SIGNAL_API_URL}/v1/about")
                print("[KEEP-ALIVE] Pinged signal-cli ✅")
            except Exception as e:
                print(f"[KEEP-ALIVE] signal-cli ping failed: {e}")

            try:
                # Ping this bot to keep it awake
                if BOT_URL:
                    await client.get(f"{BOT_URL}/")
                    print("[KEEP-ALIVE] Pinged bot ✅")
            except Exception as e:
                print(f"[KEEP-ALIVE] Bot ping failed: {e}")

            # Re-register webhook every 10 minutes (2 cycles) in case signal-cli restarted
            if cycle % 2 == 0:
                try:
                    await client.post(
                        f"{SIGNAL_API_URL}/v1/configuration",
                        json={"webhookURL": f"{BOT_URL}/webhook"}
                    )
                    print("[KEEP-ALIVE] Webhook re-registered ✅")
                except Exception as e:
                    print(f"[KEEP-ALIVE] Webhook re-register failed: {e}")


@app.on_event("startup")
async def startup():
    asyncio.create_task(keep_alive())