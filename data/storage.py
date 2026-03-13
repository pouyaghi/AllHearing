import json
import os

DATA_FILE = "messages.json"


def load_data():
    if not os.path.exists(DATA_FILE):
        return {}

    with open(DATA_FILE, "r") as f:
        return json.load(f)


def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)


def save_message(username, message):
    data = load_data()

    if username not in data:
        data[username] = []

    data[username].append(message)

    save_data(data)


def get_users():
    data = load_data()
    return list(data.keys())


def get_messages_by_user(username):
    data = load_data()
    return data.get(username, [])