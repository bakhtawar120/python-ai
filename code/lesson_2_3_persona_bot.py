"""Task 2.3: Persona Bot with Real Facts.

A chat bot for a small business with memory. The system message is built
from a facts dictionary so the AI only uses real information. The user
can change the bot's personality with /persona and get exact prices with
/price (answered from the dictionary, without calling the AI).
Stretch: /add adds a new item and rebuilds the system message.
"""

from langchain.chat_models import init_chat_model

# Why: one config dictionary keeps all settings in one place, so we
# can change the model, temperature or memory size without hunting
# through the code.
config = {
    "model": "gemma4:31b-cloud",
    "temperature": 0.2,
    "memory_size": 8,
}

# Why: the facts are real data. The AI must use only these, so it
# cannot invent prices. CHANGE THESE to your own business.
facts = {
    "name": "Sweet Crumbs Bakery",
    "city": "Lahore",
    "opening_hours": "9 AM to 9 PM, every day",
    "phone": "0300-1234567",
    "delivery": "Free delivery above 2000 PKR",
    "prices": {
        "cupcake": 250,
        "brownie": 300,
        "chocolate cake": 1500,
    },
}

personas = {
    "friendly": "warm and cheerful, uses simple words",
    "formal": "polite and professional, no slang",
    "sales": "excited, always suggests one extra item to buy",
}


def build_system_message(style):
    """Build the system message text from the facts and a style."""
    price_lines = ""
    for item, price in facts["prices"].items():
        price_lines += f"- {item}: {price} PKR\n"

    return (
        f"You are the assistant of {facts['name']} in {facts['city']}. "
        f"Opening hours: {facts['opening_hours']}. "
        f"Phone: {facts['phone']}. "
        f"Delivery: {facts['delivery']}.\n"
        f"Prices:\n{price_lines}"
        "Only use these facts. If the answer is not in the facts, "
        "say you do not know and ask the customer to call us. "
        f"Your style: {style}. Answer in at most 3 short sentences."
    )


# Why: the model is created once, outside the loop, because creating
# it for every message would be slow.
llm = init_chat_model(
    config["model"],
    model_provider="ollama",
    temperature=config["temperature"],
)

# NEW: remembers the current style so /add can rebuild the system
# message without changing the persona.
current_style = personas["friendly"]

# Why: messages[0] is the system message. Changing its content later
# is how /persona changes the bot's personality.
messages = [
    {"role": "system", "content": build_system_message(current_style)}
]

print("Bot ready. Commands: /persona friendly|formal|sales, /price <item>, /add <item> <price>, bye")

while True:
    user_text = input("You: ").strip()

    if user_text == "":
        continue

    if user_text.lower() == "bye":
        print("Bot: Goodbye!")
        break

    if user_text.lower().startswith("/persona"):
        name = user_text[8:].strip().lower()
        # Why: .get() with a default means a wrong name like "pirate"
        # gives the friendly style instead of crashing with KeyError.
        style = personas.get(name, personas["friendly"])
        current_style = style  # NEW
        messages[0]["content"] = build_system_message(style)
        print(f"Bot: Style changed to: {style}")
        continue

    if user_text.lower().startswith("/price"):
        item = user_text[6:].strip().lower()
        price = facts["prices"].get(item)
        # Why: prices come from the dictionary, not the AI, so they are
        # always correct and cost no tokens.
        if price is None:
            print(f"Bot: Sorry, {item} is not on our menu.")
        else:
            print(f"Bot: {item.capitalize()} costs {price} PKR.")
        continue

    # NEW: stretch command /add <item> <price>
    if user_text.lower().startswith("/add"):
        # Why: rsplit splits from the right, so item names with spaces
        # like "chocolate cake" still work: the last word is the price.
        parts = user_text[4:].strip().rsplit(" ", 1)
        if len(parts) != 2 or not parts[1].isdigit():
            print("Bot: Use it like this: /add pastry 180")
        else:
            item = parts[0].strip().lower()
            facts["prices"][item] = int(parts[1])
            # Why: we rebuild the system message so the AI knows about
            # the new item immediately.
            messages[0]["content"] = build_system_message(current_style)
            print(f"Bot: Added {item} at {parts[1]} PKR.")
        continue

    messages.append({"role": "user", "content": user_text})
    response = llm.invoke(messages)
    messages.append({"role": "assistant", "content": response.text})

    # Why: keep the system message plus only the last N messages, so
    # the cost does not grow forever.
    messages = [messages[0]] + messages[1:][-config["memory_size"]:]

    print(f"Bot: {response.text}")

    