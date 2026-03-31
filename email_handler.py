import smtplib
import imaplib
import email
import json
import os
import time
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
from main import generate
from news_handler import get_news_summary
from calendar_handler import get_calendar_summary
from health_tracker import analyze_health
from finance_tracker import analyze_finance

BASE_DIR = "/Users/architjagadeb/Desktop/Projects/daily-assistant"

load_dotenv()

EMAIL = os.getenv("EMAIL")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
EVENING_SUBJECT = "Log Your Day "


# ── Shared helper ────────────────────────────────────────────────────────────

def send_email(subject, body):
    msg = MIMEMultipart()
    msg["From"] = EMAIL
    msg["To"] = EMAIL
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain", "utf-8"))

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(EMAIL, EMAIL_PASSWORD)
        server.sendmail(EMAIL, EMAIL, msg.as_string())


# ── 7am Morning Digest ───────────────────────────────────────────────────────

def send_daily_digest():
    news    = get_news_summary()
    health  = analyze_health()
    finance = analyze_finance()

    prompt = f"""Create a friendly morning digest email with clear sections for:

NEWS: {news}
HEALTH: {health}
FINANCE (yesterday): {finance}

Keep it under 200 words. Be motivating."""

    send_email("☀️ Your Morning Digest", generate(prompt))
    print("Morning digest sent.")


# ── 9pm Evening Check-in ─────────────────────────────────────────────────────

def send_evening_prompt():
    body = """Hey! How was your day? 🙂

Reply to this email with your expenses like:
  Coffee 120, Lunch 350, Uber 80

Optionally add health info on a new line:
  slept 7hrs, walked 5000 steps
"""
    send_email(EVENING_SUBJECT, body)
    print("Evening prompt sent.")


def poll_for_reply():
    """Check inbox every 15 mins for up to 3 hours for a reply."""
    for _ in range(12):  # 12 x 15min = 3 hours
        try:
            mail = imaplib.IMAP4_SSL("imap.gmail.com")
            mail.login(EMAIL, EMAIL_PASSWORD)
            mail.select("inbox")

            _, ids = mail.search(None, f'SUBJECT "Re: {EVENING_SUBJECT}"')
            if ids[0]:
                _, msg_data = mail.fetch(ids[0].split()[-1], "(RFC822)")
                msg = email.message_from_bytes(msg_data[0][1])

                for part in msg.walk():
                    if part.get_content_type() == "text/plain":
                        return part.get_payload(decode=True).decode("utf-8", errors="ignore").strip()

            mail.logout()
        except Exception as e:
            print(f"Inbox check failed: {e}")

        print("No reply yet, checking again in 15 mins...")
        time.sleep(900)  # 15 minutes

    return None


def parse_and_save(reply_text):
    """One Gemini call to parse reply → saves to finance_log.json + health_log.json."""
    prompt = f"""Extract data from this message. Return ONLY valid JSON, no markdown.

{{
  "expenses": [{{"expense": 120, "category": "Food"}}],
  "health": {{"sleep": "7", "water": "8", "steps": "5000"}}
}}

Use empty list/empty object if nothing found. Guess category if not mentioned.

Message: {reply_text}"""

    raw = generate(prompt).strip().removeprefix("```json").removeprefix("```").removesuffix("```").strip()

    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        print("Could not parse Gemini response. Skipping save.")
        return

    timestamp = datetime.now().isoformat()

    with open(f"{BASE_DIR}/data/finance_log.json", "a") as f:
        for item in data.get("expenses", []):
            json.dump({"expense": item["expense"], "category": item["category"], "timestamp": timestamp}, f)
            f.write("\n")

    health = data.get("health", {})
    if health:
        with open(f"{BASE_DIR}/data/health_log.json", "a") as f:
            json.dump({**health, "timestamp": timestamp}, f)
            f.write("\n")

    print("Expenses and health data saved.")


def run_evening_flow():
    send_evening_prompt()
    reply = poll_for_reply()
    if reply:
        parse_and_save(reply)
    else:
        print("No reply received tonight.")


if __name__ == "__main__":
    send_daily_digest()