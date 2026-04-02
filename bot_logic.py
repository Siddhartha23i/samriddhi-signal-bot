# bot_logic.py
# The brain of the bot.
# Receives every incoming message, checks the user's state,
# decides what to reply, and sends it.

from services import SERVICES, build_main_menu, build_service_menu
from state_store import get_state, set_state, reset_state
from messenger import send_message

# Any of these words restart the conversation and show the main menu
TRIGGER_WORDS = {"hi", "hello", "start", "menu", "hey", "namaste"}


async def handle_message(sender: str, text: str):
    """
    Main entry point for every incoming message.

    Args:
        sender: The user's phone number, e.g. "+91XXXXXXXXXX"
        text:   The raw message text they sent
    """
    text = text.strip()
    state = get_state(sender)

    # ── Always restart on trigger words or first contact ──────────────────────
    if text.lower() in TRIGGER_WORDS or state["stage"] == "new":
        set_state(sender, {"stage": "main"})
        await send_message(sender, build_main_menu())
        return

    # ── User is at the main menu ───────────────────────────────────────────────
    if state["stage"] == "main":

        if text in SERVICES:
            # Valid service number picked → show that service's submenu
            set_state(sender, {"stage": "service", "service_id": text})
            await send_message(sender, build_service_menu(text))

        elif text == "6":
            # Human handoff
            await send_message(
                sender,
                "🧑 You'll be connected to our team shortly.\n\n"
                "📍 *Samriddhi Anveshana*, Hyderabad\n"
                "We typically respond within 30 minutes during business hours.\n\n"
                "Type *menu* anytime to explore our services."
            )
            reset_state(sender)

        else:
            # Invalid input
            await send_message(
                sender,
                "❓ Please reply with a number between *1–6*.\n"
                "Type *menu* anytime to see the options again."
            )

    # ── User is inside a service submenu ──────────────────────────────────────
    elif state["stage"] == "service":
        service_id = state["service_id"]
        subservices = SERVICES[service_id]["subservices"]
        service_name = SERVICES[service_id]["name"]
        total_options = len(subservices)

        if text == "0":
            # Go back to main menu
            set_state(sender, {"stage": "main"})
            await send_message(sender, build_main_menu())

        elif text in subservices:
            # Valid subservice picked → send confirmation and end conversation
            chosen = subservices[text]
            await send_message(
                sender,
                f"✅ *{chosen}*\n\n"
                f"Thank you for your interest in our {service_name} services.\n"
                f"Our team at *Samriddhi Anveshana* will reach out to you shortly! 🙏\n\n"
                f"Type *menu* to explore other services."
            )
            reset_state(sender)

        else:
            # Invalid input inside submenu
            await send_message(
                sender,
                f"❓ Please reply with a number between *1–{total_options}*.\n"
                f"Reply *0* to go back to the main menu."
            )
