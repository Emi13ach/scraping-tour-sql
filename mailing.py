import os
import ssl
import smtplib
from email.message import EmailMessage


def send_email(content):
    HOST = "smtp.gmail.com"
    PORT = 465
    USERNAME = "eb.pythoncode@gmail.com"
    PASSWORD = os.getenv("GMAIL_PASSWORD")
    RECEIVER = 'eb.pythoncode@gmail.com'

    email_message = EmailMessage()
    email_message["Subject"] = "Next tour"
    email_message.set_content(content)

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL(host=HOST, port=PORT, context=context) as server:
        server.login(USERNAME, PASSWORD)
        server.sendmail(USERNAME, RECEIVER, email_message.as_string())
