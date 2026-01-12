import os
import requests

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

message = """
📘 UPSC Daily MCQ

Which Article of the Constitution deals with the Right to Equality?

A) Article 12
B) Article 14
C) Article 19
D) Article 21

🕒 Answer will be posted in the evening.
"""

url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

payload = {
    "chat_id": CHAT_ID,
    "text": message,
    "parse_mode": "HTML"
}

response = requests.post(url, json=payload)

print(response.text)
