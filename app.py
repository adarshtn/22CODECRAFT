from flask import Flask, render_template
from email_reader import fetch_unread_emails
from classifier import classify_issue
from database import init_db, insert_ticket, fetch_all_tickets

app = Flask(__name__)

# Initialize DB
init_db()

# Gmail credentials
USERNAME = 'adarshthulasidas04@gmail.com'    # <--- Replace this
PASSWORD = 'ujurhywrokvlpbak'       # <--- Replace this (use App Password)

@app.route('/')
def index():
    # Fetch emails
    emails = fetch_unread_emails(USERNAME, PASSWORD)
    for email_data in emails:
        group = classify_issue(email_data['body'])
        insert_ticket(email_data['from'], email_data['subject'], email_data['body'], group)

    # Fetch all tickets
    tickets = fetch_all_tickets()
    return render_template('index.html', tickets=tickets)

if __name__ == '__main__':
    app.run(debug=True)
