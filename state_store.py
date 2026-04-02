# state_store.py
# Tracks each user's position in the conversation flow.
#
# State structure per user (keyed by phone number):
#   {"stage": "new"}                              → Never talked to bot before
#   {"stage": "main"}                             → At the main services menu
#   {"stage": "service", "service_id": "1"}       → Inside a specific service's submenu
#
# NOTE: This is in-memory storage.
# If the server restarts, all user states reset and users start fresh.
# For production: replace this with Redis.

_store: dict = {}


def get_state(phone: str) -> dict:
    """Returns the current state for a user. Defaults to 'new' if not seen before."""
    return _store.get(phone, {"stage": "new"})


def set_state(phone: str, state: dict):
    """Updates the state for a user."""
    _store[phone] = state


def reset_state(phone: str):
    """Removes the user's state entirely (used after a conversation ends)."""
    _store.pop(phone, None)
