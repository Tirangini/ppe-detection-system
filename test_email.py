import smtplib
from email.mime.text import MIMEText
from dotenv import load_dotenv
import os

load_dotenv()

EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

print("Email:", EMAIL_ADDRESS)
print("Password length:", len(EMAIL_PASSWORD) if EMAIL_PASSWORD else "NOT FOUND")

msg = MIMEText("Test email from PPE project")
msg['Subject'] = 'Test'
msg['From'] = EMAIL_ADDRESS
msg['To'] = EMAIL_ADDRESS

with smtplib.SMTP('smtp.gmail.com', 587) as server:
    server.starttls()
    server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
    server.send_message(msg)

print("Sent successfully!")