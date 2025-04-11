from flask import Flask, render_template, request
from email_reader import fetch_unread_emails
from database import init_db, insert_ticket, fetch_all_tickets
from email_sender import send_reply_email
import json
import sqlite3
import re

app = Flask(__name__)

# Initialize DB
init_db()

# Load keywords from JSON file
with open('keywords.json', 'r') as file:
    keywords_data = json.load(file)
    departments = keywords_data['departments']

# Gmail credentials (move to environment variables in production)
USERNAME = 'adarshthulasidas04@gmail.com'    # <--- Replace this
PASSWORD = 'ujurhywrokvlpbak'       # <--- Replace this (use App Password)

def classify_issue(email_body):
    email_body = email_body.lower()
    for dept, keywords in departments.items():
        if any(keyword in email_body for keyword in keywords):
            return dept
    return 'General'  # Default if no keywords match

def extract_email(raw_email):
    # Extract the email address from a string like 'Name <email@example.com>'
    match = re.search(r'<(.+?)>', raw_email)
    return match.group(1) if match else raw_email.strip()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        ticket_id = request.form.get('ticket_id')
        reply_body = request.form.get('reply_body')
        print(f"Received POST with ticket_id: {ticket_id}, reply_body: {reply_body}")  # Debug
        if ticket_id and reply_body:
            conn = sqlite3.connect('service_requests.db')
            cursor = conn.cursor()
            cursor.execute('SELECT email, subject FROM tickets WHERE id = ?', (ticket_id,))
            ticket = cursor.fetchone()
            conn.close()
            if ticket:
                raw_to_email, subject = ticket
                to_email = extract_email(raw_to_email)  # Extract clean email address
                print(f"Raw to_email: {raw_to_email}, Extracted to_email: {to_email}, Subject: {subject}")  # Debug
                # Default reply template
                default_reply = f"Thank you for your email. We have received your concern regarding '{subject}'. Our team is currently reviewing it and will get back to you soon. If you have additional details, please let us know.\n\nBest regards,\nYour Support Team"
                # Combine default reply with user input (if provided)
                final_reply = default_reply if not reply_body.strip() else f"{default_reply}\n\nAdditional Notes: {reply_body}"
                send_reply_email(to_email, subject, final_reply, USERNAME, PASSWORD)

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