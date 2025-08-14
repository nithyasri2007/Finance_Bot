import sqlite3

def init_db():
    conn = sqlite3.connect('financebot.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS sessions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_type TEXT,
        chat_history TEXT,
        income REAL,
        expenses REAL,
        goal TEXT,
        goal_amount REAL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
