import smtplib
import re
from email.mime.text import MIMEText

def send_reply_email(to_email, subject, body, username, password):
    # Gmail SMTP server settings
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    
    # Clean up the recipient email if needed
    to_email = to_email.strip()
    
    # Create the email message
    msg = MIMEText(body)
    msg['Subject'] = f"Re: {subject}"
    msg['From'] = username
    msg['To'] = to_email
    print(f"Preparing to send reply to: {to_email}")
    
    try:
        # Connect to SMTP server
        print(f"Connecting to {smtp_server}:{smtp_port}")
        server = smtplib.SMTP(smtp_server, smtp_port)
        
        # Debug mode for detailed connection information
        server.set_debuglevel(1)
        
        # Start TLS encryption
        server.ehlo()
        server.starttls()
        server.ehlo()
        
        print(f"Logging in with: {username}")
        server.login(username, password)
        
        print(f"Sending email to: {to_email}")
        # Send the email
        result = server.sendmail(username, to_email, msg.as_string())
        if not result:
            print(f"Reply email sent successfully to {to_email}")
        else:
            print(f"Partial send success. Failed recipients: {result}")
            
    except smtplib.SMTPAuthenticationError as e:
        print(f"SMTP Authentication Error: {e}")
        print("Please verify your username and app password are correct")
    except smtplib.SMTPRecipientsRefused as e:
        print(f"SMTP Recipients Refused: {e}")
        print(f"Invalid recipient: {to_email}")
    except smtplib.SMTPSenderRefused as e:
        print(f"SMTP Sender Refused: {e}")
        print("Your email provider may be blocking the send attempt")
    except smtplib.SMTPException as e:
        print(f"SMTP Error: {e}")
    except ConnectionRefusedError as e:
        print(f"Connection Refused: {e}")
        print("Check if your firewall is blocking outgoing connections")
    except Exception as e:
        print(f"Unexpected error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        try:
            server.quit()
        except:
            pass
        print("SMTP connection closed")

def extract_email(raw_email):
    if not raw_email:
        return ""
    
    # Try to extract email from format like "Name <email@example.com>"
    match = re.search(r'<([^<>]+)>', raw_email)
    if match:
        return match.group(1).strip()
    
    # Try to find any email pattern in the string
    match = re.search(r'([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)', raw_email)
    if match:
        return match.group(1).strip()
    
    # If no patterns match, just return the cleaned string
    return raw_email.strip()

# Test function to verify email sending functionality
def test_email_send(username, password, test_recipient=None):
    if not test_recipient:
        test_recipient = username  # Send to self if no recipient specified
    
    test_subject = "Test Email"
    test_body = "This is a test email to verify SMTP functionality."
    
    print("Running direct email send test...")
    send_reply_email(test_recipient, test_subject, test_body, username, password)
    print("Email test complete")

# Uncomment the below line to test when this file is run directly
# if __name__ == "__main__":
#     from app import USERNAME, PASSWORD
#     test_email_send(USERNAME, PASSWORD)