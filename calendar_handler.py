from datetime import datetime, timezone
from main import generate

def get_calendar_summary(events):
    events_lines = []

    for event in events:
        events_lines.append(f"- {event['title']} at {event['start_time']} to {event['end_time']}")

    if not events_lines:
        return "No upcoming events."

    prompt = f"""Here are your upcoming events for today:\n{chr(10).join(events_lines)}

    Summarize these in 3-4 lines, suggest time for breakfast, lunch, dinner and gym.
    """

    return generate(prompt)

test_events = [
    {"title": "Standup", "start_time": "10:00 AM", "end_time": "10:30 AM"},
    {"title": "Client Call", "start_time": "2:00 PM", "end_time": "3:00 PM"},
]

if __name__ == "__main__":
    print(get_calendar_summary(test_events))