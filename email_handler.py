import smtplib
import os
from dotenv import load_dotenv
from main import generate
from news_handler import get_news_summary
from calendar_handler import get_calendar_summary
from health_tracker import analyze_health
from finance_tracker import analyze_finance

load_dotenv()

EMAIL = os.getenv("EMAIL")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

def send_email(subject, body):
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart

    msg = MIMEMultipart()
    msg["From"] = EMAIL
    msg["To"] = EMAIL
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain", "utf-8"))

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(EMAIL, EMAIL_PASSWORD)
        server.sendmail(EMAIL, EMAIL, msg.as_string())

def send_daily_digest():
    news_summary = get_news_summary()
    health_summary = analyze_health()
    finance_summary = analyze_finance()

    prompt = f"""Create a beautiful morning digest email with clear sections and headings for:

NEWS:
{news_summary}

HEALTH:
{health_summary}

FINANCE:
{finance_summary}

Make it friendly, concise and motivating."""

    body = generate(prompt)
    send_email("Daily Digest", body)

send_daily_digest()