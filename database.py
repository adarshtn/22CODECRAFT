# database.py
import sqlite3

DB_FILE = 'service_requests.db'

def init_db():
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tickets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email_from TEXT NOT NULL,
                subject TEXT NOT NULL,
                body TEXT NOT NULL,
                department TEXT NOT NULL,
                status TEXT DEFAULT 'open'
            )
        ''')
        cursor.execute("PRAGMA table_info(tickets)")
        columns = [col[1] for col in cursor.fetchall()]
        if 'status' not in columns:
            cursor.execute("ALTER TABLE tickets ADD COLUMN status TEXT DEFAULT 'open'")
            print("Added 'status' column to existing 'tickets' table.")
        conn.commit()
        print("Database initialized successfully with 'tickets' table.")
    except Exception as e:
        print(f"Error initializing database: {e}")
    finally:
        conn.close()

def insert_ticket(email_from, subject, body, department):
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO tickets (email_from, subject, body, department)
            VALUES (?, ?, ?, ?)
        ''', (email_from, subject, body, department))
        conn.commit()
    except Exception as e:
        print(f"Error inserting ticket: {e}")
    finally:
        conn.close()

def fetch_all_tickets():
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        # Include status in the query
        cursor.execute('SELECT id, email_from, subject, body, department, status FROM tickets')
        tickets = cursor.fetchall()
        return tickets
    except Exception as e:
        print(f"Error fetching tickets: {e}")
        return []
    finally:
        conn.close()

def delete_all_tickets():
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM tickets")
        conn.commit()
        print("All tickets have been deleted successfully.")
    except Exception as e:
        print(f"Error occurred while deleting tickets: {e}")
    finally:
        conn.close()

def drop_all():
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute("DROP TABLE IF EXISTS tickets")
        conn.commit()
        print("The tickets table has been dropped successfully.")
    except Exception as e:
        print(f"Error occurred while dropping the table: {e}")
    finally:
        conn.close()