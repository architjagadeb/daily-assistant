import json
from main import generate
from datetime import datetime
import os

if not os.path.exists("data/finance_log.json"):
    income = input("Enter your monthly income: ")
    budget = input("Enter your monthly budget: ")
    config_data = {
        "MONTHLY_INCOME": income,
        "MONTHLY_BUDGET": budget
    }
    with open("data/finance_config.json", "w") as f:
        json.dump(config_data, f)
    print("Setup saved!")
else:
    with open("data/finance_config.json", "r") as f:
        config_data = json.load(f)
    MONTHLY_INCOME = config_data.get("MONTHLY_INCOME", 0)
    MONTHLY_BUDGET = config_data.get("MONTHLY_BUDGET", 0)

def log_finance_data():
    while True:
        expense = input("Enter today's expenses: ")

        if expense == "done":
            break
        
        category = input("Enter expense category (e.g., Food, Transport, Entertainment): ")

        print(f"Finance data logged: expense: {expense}, category: {category}")

        data = {
            "expense": expense,
            "category": category,
            "timestamp": datetime.now().isoformat()
        }

        with open("data/finance_log.json", "a") as f:
            json.dump(data, f)
            f.write("\n")

        print("Finance data saved!")
        

def analyze_finance():

    with open("data/finance_log.json", "r") as f:
        data = f.read()

    prompt = f""" Analyze the following finance data logs, provide insights on spending habits and suggest improvements if needed. Here are the logs:
    {data}
     """

    return generate(prompt)

log_finance_data()
print(analyze_finance())