import json
import os

SUBSCRIBERS_FILE = "subscribers.json"

def load_subscribers():
    if not os.path.exists(SUBSCRIBERS_FILE):
        return []
    with open(SUBSCRIBERS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_subscribers(subscribers):
    with open(SUBSCRIBERS_FILE, "w", encoding="utf-8") as f:
        json.dump(subscribers, f, ensure_ascii=False, indent=2)

def add_subscriber(chat_id):
    subscribers = load_subscribers()
    if chat_id not in subscribers:
        subscribers.append(chat_id)
        save_subscribers(subscribers)

def remove_subscriber(chat_id):
    subscribers = load_subscribers()
    if chat_id in subscribers:
        subscribers.remove(chat_id)
        save_subscribers(subscribers)
