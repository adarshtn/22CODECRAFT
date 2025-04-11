import sqlite3

def init_db():
    conn = sqlite3.connect('service_requests.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS tickets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT,
            subject TEXT,
            body TEXT,
            group_name TEXT
        )
    ''')
    conn.commit()
    conn.close()

def insert_ticket(email, subject, body, group_name):
    conn = sqlite3.connect('service_requests.db')
    c = conn.cursor()
    c.execute('''
        INSERT INTO tickets (email, subject, body, group_name)
        VALUES (?, ?, ?, ?)
    ''', (email, subject, body, group_name))
    conn.commit()
    conn.close()

def fetch_all_tickets():
    conn = sqlite3.connect('service_requests.db')
    c = conn.cursor()
    c.execute('SELECT * FROM tickets')
    tickets = c.fetchall()
    conn.close()
    return tickets
