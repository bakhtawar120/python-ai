"""Task 2.6: Saved Bot for Sweet Crumbs Bakery.

A chat bot whose facts come from faq.json and whose chat history is
saved in chat_history.json, so it remembers yesterday's chat. Errors
never show a red traceback: the customer sees a friendly message and
the error is written to errors.log.
"""

import json
import sys
from datetime import datetime

import httpx
import ollama
from langchain.chat_models import init_chat_model


def log_error(error) -> None:
    """Append one error line with the time to errors.log."""
    # Why: mode "a" (append) adds to the end, so old errors are kept
    # and the owner can read what went wrong later.
    with open("errors.log", "a", encoding="utf-8") as file:
        file.write(f"{datetime.now():%Y-%m-%d %H:%M} {type(error).__name__}: {error}\n")


def save_history(history: list) -> None:
    """Save the chat history to chat_history.json."""
    # Why: indent=2 makes the file readable, and ensure_ascii=False
    # keeps Urdu letters as they are instead of \u0627 codes.
    with open("chat_history.json", "w", encoding="utf-8") as file:
        json.dump(history, file, indent=2, ensure_ascii=False)


# Why: if faq.json is missing, the bot has no facts and would invent
# prices. So we stop with a clear message instead of a traceback.
try:
    with open("faq.json", encoding="utf-8") as file:
        facts = json.load(file)
except FileNotFoundError:
    print("faq.json was not found. Put it in the same folder and run again.")
    sys.exit()
except json.JSONDecodeError:
    print("faq.json is damaged. Please check its commas and quotes.")
    sys.exit()

price_lines = ""
for item, price in facts["prices"].items():
    price_lines += f"- {item}: {price:,} PKR\n"

system_message = {
    "role": "system",
    "content": (
        f"You are the assistant of {facts['name']} in {facts['city']}. "
        f"Opening hours: {facts['hours']}. Phone: {facts['phone']}. "
        f"Delivery: {facts['delivery']}.\nPrices:\n{price_lines}"
        "For questions about the bakery, only use these facts. "
        "If the answer is not in the facts, say you do not know and "
        "ask the customer to call us. "
        "But you may use what the customer told you earlier in this "
        "chat, like their name. "
        "Answer in at most 3 short sentences."
    ),
}

llm = init_chat_model(
    "gemma4:31b-cloud", model_provider="ollama", temperature=0.2
)

# Why: the history file can be missing (first run) or damaged (bad
# edit). Both cases start a fresh chat instead of crashing.
history = []
try:
    with open("chat_history.json", encoding="utf-8") as file:
        history = json.load(file)
    if not isinstance(history, list):
        raise ValueError("history must be a list")
    print(f"Loaded {len(history)} old messages.")
except FileNotFoundError:
    history = []
except (json.JSONDecodeError, ValueError):
    print("History file was damaged. Starting a fresh chat.")
    history = []

print(f"{facts['name']} Bot: Ask me anything. Commands: /reset, /export, bye")

while True:
    user_text = input("You: ").strip()

    if user_text == "":
        continue

    if user_text.lower() == "bye":
        save_history(history)
        print("Bot: Goodbye! Your chat is saved.")
        break

    if user_text.lower() == "/reset":
        history = []
        save_history(history)
        print("Bot: Chat cleared.")
        continue

    if user_text.lower() == "/export":
        # Stretch: write the chat as a readable transcript
        with open("transcript.txt", "w", encoding="utf-8") as file:
            for message in history:
                file.write(f"{message['role']}: {message['content']}\n")
        print("Bot: Chat exported to transcript.txt")
        continue

    history.append({"role": "user", "content": user_text})

    try:
        # Only the last 8 messages go to the AI, so the cost stays small
        response = llm.invoke([system_message] + history[-8:])
    # Why: newer ollama versions turn httpx.ConnectError into the
    # built-in ConnectionError, so we catch both to be safe.
    except (httpx.ConnectError, ConnectionError) as error:
        history.pop()  # remove the unanswered question
        log_error(error)
        print("Bot: I am offline right now. Please open the Ollama app and try again.")
        continue
    except ollama.ResponseError as error:
        history.pop()
        log_error(error)
        print("Bot: Something went wrong with the AI. Please try again in a moment.")
        continue

    history.append({"role": "assistant", "content": response.text})
    save_history(history)
    print(f"Bot: {response.text}")