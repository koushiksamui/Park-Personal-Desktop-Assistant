import smtplib
from email.mime.text import MIMEText
import imaplib
import email


def send_email(to, subject, body):
    # Set up the email server
    server = smtplib.SMTP('imap.gmail.com', 587)
    server.starttls()
    server.login('koushiksamui474@gmail.com', '')

    # Create the email message
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = 'koushiksamui474@gmail.com'
    msg['To'] = to

    # Send the email
    server.sendmail('koushiksamui474@gmail.com', to, msg.as_string())

    # Close the server connection
    server.quit()


# Example usage
send_email('koushiksamui30@gmail.com', 'Hello', 'This is a test email from Jarvis.')


def receive_emails():
    mail = imaplib.IMAP4_SSL('your_imap_server.com')
    mail.login('your_email@gmail.com', 'your_email_password')
    mail.select('inbox')

    status, messages = mail.search(None, 'ALL')
    message_ids = messages[0].split()

    for msg_id in message_ids:
        _, msg_data = mail.fetch(msg_id, '(RFC822)')
        email_message = email.message_from_bytes(msg_data[0][1])

        # Process the email_message as needed

    mail.logout()


# Example usage
# receive_emails()
