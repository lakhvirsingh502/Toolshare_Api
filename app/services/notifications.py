from fastapi import BackgroundTasks
import os
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv
load_dotenv()

SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
SMTP_PORT = int(os.getenv("SMTP_PORT"))
SMTP_USERNAME = os.getenv("SMTP_USERNAME")
SMTP_HOST = os.getenv("SMTP_HOST")

def send_notification(recipient:str,subject:str,message:str,):
    email = EmailMessage()
    email["From"] = SMTP_USERNAME
    email["To"] = recipient
    email["Subject"] = subject
    email.set_content(message)

    with smtplib.SMTP(SMTP_HOST,SMTP_PORT) as server:
        server.starttls()
        server.login(SMTP_USERNAME,SMTP_PASSWORD)
        server.send_message(email)