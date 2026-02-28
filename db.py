import sqlite3


def create_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY,
        username TEXT,
        first_name TEXT
    )
    """)
    conn.commit()
    conn.close()

def add_user(user_id, username, first_name):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("""
    INSERT OR IGNORE INTO users (user_id, username, first_name)
    VALUES (?, ?, ?)
    """, (user_id, username, first_name))
    conn.commit()
    conn.close()

def get_all_users():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("""
    SELECT user_id FROM users
    """)
    result = cursor.fetchall()
    conn.close()
    return [row[0] for row in result]