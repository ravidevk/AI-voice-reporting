import smtplib
from email.mime.text import MIMEText

def send_email(recipient, subject, body, sender_email, sender_pass):
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = recipient

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender_email, sender_pass)
        server.send_message(msg)

