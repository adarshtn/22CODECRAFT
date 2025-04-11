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
USERNAME = 'adarshthulasidas04@gmail.com'  # <--- Replace this
PASSWORD = 'zifwgbjvgdgpyarb'              # <--- Replace this (use App Password)

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

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/fetch-emails')
def fetch_emails():
    # Fetch new emails
    emails = fetch_unread_emails(USERNAME, PASSWORD)
    for email_data in emails:
        group = classify_issue(email_data['body'])
        insert_ticket(email_data['from'], email_data['subject'], email_data['body'], group)
    return "Emails fetched and stored successfully."

@app.route('/department/<dept_name>')
def show_department_tickets(dept_name):
    tickets = fetch_all_tickets()
    filtered_tickets = [t for t in tickets if t[4].lower() == dept_name.lower()]
    return render_template('department.html', tickets=filtered_tickets, department=dept_name.capitalize())

if __name__ == '__main__':
    app.run(debug=True)
