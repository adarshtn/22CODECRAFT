from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from email_reader import fetch_unread_emails
from database import init_db, insert_ticket, fetch_all_tickets
from email_sender import send_reply_email
import json
import sqlite3
import re

app = Flask(__name__)
app.secret_key = 'supersecretkey'

init_db()

with open('keywords.json', 'r') as file:
    keywords_data = json.load(file)
    departments = keywords_data['departments']

USERNAME = 'adarshthulasidas04@gmail.com'
PASSWORD = 'zifwgbjvgdgpyarb'

DEPT_PASSWORDS = {
    'technical': 'tech123',
    'sales': 'sales123',
    'accounts': 'acc123',
    'general': 'gen123'
}

def classify_issue(email_body):
    email_body = email_body.lower()
    for dept, keywords in departments.items():
        if any(keyword in email_body for keyword in keywords):
            return dept
    return 'General'

def extract_email(raw_email):
    match = re.search(r'<(.+?)>', raw_email)
    return match.group(1) if match else raw_email.strip()

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/department/<dept_name>/auth', methods=['GET', 'POST'])
def department_auth(dept_name):
    if request.method == 'POST':
        password = request.form.get('password')
        correct_password = DEPT_PASSWORDS.get(dept_name.lower())
        if password == correct_password:
            session[f'{dept_name}_access'] = True
            return redirect(url_for('show_department_tickets', dept_name=dept_name))
        else:
            return render_template('password.html', dept_name=dept_name, error="Incorrect password")
    return render_template('password.html', dept_name=dept_name)

@app.route('/department/<dept_name>')
def show_department_tickets(dept_name):
    if not session.get(f'{dept_name}_access'):
        return redirect(url_for('department_auth', dept_name=dept_name))

    tickets = fetch_all_tickets()
    filtered_tickets = [t for t in tickets if t[4].lower() == dept_name.lower()]
    return render_template('department.html', tickets=filtered_tickets, department=dept_name.capitalize())

@app.route('/fetch-emails')
def fetch_emails():
    emails = fetch_unread_emails(USERNAME, PASSWORD)
    for email_data in emails:
        group = classify_issue(email_data['body'])
        insert_ticket(email_data['from'], email_data['subject'], email_data['body'], group)
    return "Emails fetched and stored."

@app.route('/mark-solved', methods=['POST'])
def mark_solved():
    ticket_id = request.form.get('ticket_id')
    if not ticket_id:
        return jsonify({'error': 'Missing ticket_id'}), 400

    try:
        conn = sqlite3.connect('service_requests.db')
        cursor = conn.cursor()
        cursor.execute("UPDATE tickets SET status = 'solved' WHERE id = ?", (ticket_id,))
        if cursor.rowcount == 0:
            return jsonify({'error': 'Ticket not found'}), 404
        conn.commit()
        conn.close()
        return '', 200
    except Exception as e:
        print(f"Error marking ticket as solved: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    conn = sqlite3.connect('service_requests.db')
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='tickets'")
    if cursor.fetchone():
        print("Table 'tickets' exists.")
        cursor.execute("PRAGMA table_info(tickets)")
        print("Table schema:", cursor.fetchall())
    else:
        print("Table 'tickets' does NOT exist. Initializing now...")
        init_db()
    conn.close()
    app.run(debug=True)