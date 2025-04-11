import sqlite3

# Connect to the database
conn = sqlite3.connect('service_requests.db')
cursor = conn.cursor()

# Get table info
cursor.execute("PRAGMA table_info(tickets)")
columns = cursor.fetchall()
print("Table columns:")
for col in columns:
    print(f"Column: {col[1]} (Type: {col[2]})")

# Query all data from tickets table
cursor.execute('SELECT * FROM tickets')
tickets = cursor.fetchall()

# Print the results
print("\nTickets in database:")
if tickets:
    for ticket in tickets:
        print(f"Row: {ticket}")
else:
    print("No tickets found.")

# Close the connection
conn.close()