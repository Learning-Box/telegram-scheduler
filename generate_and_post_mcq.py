import random
import json
import requests
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

BOT_TOKEN = "<YOUR BOT TOKEN HERE>"  # Or set as GitHub secret
CHAT_ID = "<YOUR CHAT ID HERE>"

# Topics list
topics = [
    "Indian Polity – Fundamental Rights",
    "Modern History – Revolt of 1857",
    "Indian Geography – Indian Monsoon",
    "Indian Economy – Inflation",
    "Environment – Biodiversity"
]

topic = random.choice(topics)

prompt = f"""
Generate ONE UPSC Prelims MCQ on the topic: {topic}.
Format:
Question:
A)
B)
C)
D)
Answer:
Explanation:
"""

# Load model
tokenizer = AutoTokenizer.from_pretrained("google/flan-t5-small")
model = AutoModelForSeq2SeqLM.from_pretrained("google/flan-t5-small")

inputs = tokenizer(prompt, return_tensors="pt")
outputs = model.generate(**inputs, max_new_tokens=150)
text = tokenizer.decode(outputs[0], skip_special_tokens=True)

# Basic parsing
lines = text.split("\n")
question = lines[0]
options = {line[0]: line[2:].strip() for line in lines[1:5]}
answer = lines[5].split(":")[1].strip()
explanation = lines[6].split(":")[1].strip()

# Prepare Telegram message
message = f"""
📘 UPSC Daily MCQ
Topic: {topic}

{question}

A) {options['A']}
B) {options['B']}
C) {options['C']}
D) {options['D']}

🕒 Answer:
{answer}
💡 Explanation:
{explanation}
"""

# Post to Telegram
url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
requests.post(url, json={"chat_id": CHAT_ID, "text": message})

print("MCQ posted for topic:", topic)
