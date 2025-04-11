import imaplib
import email

def fetch_unread_emails(username, password):
    # Connect to Gmail IMAP server
    mail = imaplib.IMAP4_SSL('imap.gmail.com')

    mail.login(username, password)
    mail.select('inbox')

    # Search for all unread messages
    status, messages = mail.search(None, '(UNSEEN)')
    email_list = []

    for num in messages[0].split():
        status, data = mail.fetch(num, '(RFC822)')
        msg = email.message_from_bytes(data[0][1])

        subject = msg['subject']
        from_email = msg['from']

        # Get email body
        if msg.is_multipart():
            body = ""
            for part in msg.walk():
                if part.get_content_type() == "text/plain":
                    body += part.get_payload(decode=True).decode()
        else:
            body = msg.get_payload(decode=True).decode()

        email_list.append({
            'subject': subject,
            'from': from_email,
            'body': body
        })

    mail.logout()
    return email_list