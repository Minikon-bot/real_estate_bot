import json
import os

FILE = "subscribers.json"

def load_subscribers():
    if not os.path.exists(FILE):
        return []
    with open(FILE, "r") as f:
        return json.load(f)

def save_subscriber(chat_id):
    subs = load_subscribers()
    if chat_id not in subs:
        subs.append(chat_id)
        with open(FILE, "w") as f:
            json.dump(subs, f)
