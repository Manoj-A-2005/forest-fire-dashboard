import sqlite3

def get_db():
    conn = sqlite3.connect("database.db", check_same_thread=False)
    conn.execute("""
    CREATE TABLE IF NOT EXISTS fire_events (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        latitude REAL,
        longitude REAL,
        probability REAL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    return conn