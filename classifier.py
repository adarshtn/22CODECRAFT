def classify_issue(email_body):
    # Define keywords for each department
    technical_keywords = ['technical support', 'bug', 'error']
    sales_keywords = ['sales', 'order', 'purchase', 'customer', 'quote']
    accounts_keywords = ['invoice', 'payment', 'billing', 'account', 'transaction']
    
    # Convert email body to lowercase for case-insensitive matching
    email_body = email_body.lower()

    # Check which department the email belongs to based on keywords
    if any(keyword in email_body for keyword in technical_keywords):
        return 'Technical'
    elif any(keyword in email_body for keyword in sales_keywords):
        return 'Sales'
    elif any(keyword in email_body for keyword in accounts_keywords):
        return 'Accounts'
    else:
        return 'General'
