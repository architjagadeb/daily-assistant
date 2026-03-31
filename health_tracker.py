import json
from main import generate
from datetime import datetime

BASE_DIR = "/Users/architjagadeb/Desktop/Projects/daily-assistant"

def log_health_data():

    sleep = input("Enter hours of sleep: ")
    water = input("Enter glasses of water consumed: ")
    steps = input("Enter number of steps taken: ")

    print(f"Health Data Logged: Sleep: {sleep} hours, Water: {water} glasses, Steps: {steps}")

    data = {
        "sleep": sleep,
        "water": water,
        "steps": steps,
        "timestamp": datetime.now().isoformat()
    }

    with open(f"{BASE_DIR}/data/health_log.json", "a") as f:
        json.dump(data, f)
        f.write("\n")

    print("Health data saved!")

def analyze_health():

    with open(f"{BASE_DIR}/data/health_log.json", "r") as f:
        data = f.read()

    prompt = f""" Analyze the following heath data logs, tell whether i am getting adequate sleep, water and exercise. Also suggest improvements if needed. Here are the logs:
    {data}
     """

    return generate(prompt)

if __name__ == "__main__":
    log_health_data()
    print(analyze_health())