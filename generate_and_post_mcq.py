import random
import json
import requests
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

BOT_TOKEN = "<YOUR BOT TOKEN HERE>"
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

# Split by lines and strip
lines = [line.strip() for line in text.split("\n") if line.strip()]

# Initialize variables
question = ""
options = {}
answer = ""
explanation = ""

# Parse dynamically
for line in lines:
    if line.startswith("Question"):
        question = line.split(":",1)[1].strip() if ":" in line else line
    elif line.startswith(("A)","B)","C)","D)")):
        options[line[0]] = line[2:].strip()
    elif line.lower().startswith("answer"):
        answer = line.split(":",1)[1].strip() if ":" in line else line
    elif line.lower().startswith("explanation"):
        explanation = line.split(":",1)[1].strip() if ":" in line else line

# Fallback if model missed parts
if not question: question = "Question not generated properly."
for o in ["A","B","C","D"]:
    if o not in options: options[o] = "Option missing"
if not answer: answer = "Answer not generated"
if not explanation: explanation = "Explanation not generated"

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
