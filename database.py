import sqlite3

DB_FILE = 'service_requests.db'

def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    # Create tickets table if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tickets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email_from TEXT,
            subject TEXT,
            body TEXT,
            department TEXT
        )
    ''')

    conn.commit()
    conn.close()

def insert_ticket(email_from, subject, body, department):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    # Insert a new ticket into the database with department info
    cursor.execute('''
        INSERT INTO tickets (email_from, subject, body, department)
        VALUES (?, ?, ?, ?)
    ''', (email_from, subject, body, department))

    conn.commit()
    conn.close()

def fetch_all_tickets():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    # Fetch all tickets
    cursor.execute('SELECT * FROM tickets')
    tickets = cursor.fetchall()

    conn.close()
    return tickets

def delete_all_tickets():
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()

        # Delete all records from the tickets table
        cursor.execute("DELETE FROM tickets")

        # Commit changes and close the connection
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

        # Drop the tickets table completely
        cursor.execute("DROP TABLE IF EXISTS tickets")

        # Commit changes and close the connection
        conn.commit()
        print("The tickets table has been dropped successfully.")
    except Exception as e:
        print(f"Error occurred while dropping the table: {e}")
    finally:
        conn.close()