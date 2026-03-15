import sqlite3

DB_NAME = "chat_history.db"


def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            text TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()


def save_message(username, text):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO messages (username, text) VALUES (?, ?)",
        (username, text)
    )

    conn.commit()

    cursor.execute("SELECT COUNT(*) FROM messages")
    count = cursor.fetchone()[0]

    conn.close()

    return count


def get_users():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT DISTINCT username FROM messages")

    users = [row[0] for row in cursor.fetchall()]

    conn.close()

    return users


def get_messages_by_user(username):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT text FROM messages WHERE username=?",
        (username,)
    )

    messages = [row[0] for row in cursor.fetchall()]

    conn.close()

    return messages


def get_last_messages(limit=20):
    """
    Returns the latest N messages from the database
    Used for batch analysis
    """
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT username, text FROM messages ORDER BY id DESC LIMIT ?",
        (limit,)
    )

    rows = cursor.fetchall()

    conn.close()

    # reverse so conversation order is correct
    rows.reverse()

    return rows