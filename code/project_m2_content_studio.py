"""AI Content Studio for Sweet Crumbs Bakery (Lahore).

The studio writes menu descriptions in one batch, streams social media
posts in different tones, answers prices from a dictionary without the
AI, and chats with customers using memory and real facts only. At the
end it prints a session report with the AI usage.
"""

from langchain.chat_models import init_chat_model

# Why: one config dictionary keeps all settings in one place.
config = {
    "model": "gemma4:31b-cloud",
    "max_messages": 8,
    "precise_temp": 0.2,
    "creative_temp": 0.8,
}

# Why: these are the real facts. The AI must use only these, so it
# cannot invent prices. CHANGE THEM to your own business.
facts = {
    "name": "Sweet Crumbs",
    "city": "Lahore",
    "hours": "9 am to 10 pm, every day",
    "phone": "0300-1234567",
    "delivery": "200 PKR, free for orders from 3,000 PKR",
    "prices": {
        "chocolate cake": 1500,
        "cupcake": 250,
        "brownie": 300,
        "donut": 200,
        "mango tart": 0,
    },
}

tones = {
    "fun": "playful and full of energy, short sentences",
    "premium": "elegant and calm, focused on quality",
    "urgent": "exciting, tells customers to order today",
}

# Why: two models for two jobs. Precise (low temperature) is for
# facts and chat, creative (high temperature) is for marketing text.
# Both are created once, here, because creating them in a loop is slow.
precise = init_chat_model(
    config["model"], model_provider="ollama",
    temperature=config["precise_temp"],
)
creative = init_chat_model(
    config["model"], model_provider="ollama",
    temperature=config["creative_temp"],
)

# Build the price lines for the system message
price_lines = ""
for item, price in facts["prices"].items():
    if price == 0:
        price_lines += f"- {item}: coming soon\n"
    else:
        price_lines += f"- {item}: {price:,} PKR\n"

system_message = {
    "role": "system",
    "content": (
        f"You are the assistant of {facts['name']} in {facts['city']}. "
        f"Opening hours: {facts['hours']}. "
        f"Phone: {facts['phone']}. "
        f"Delivery: {facts['delivery']}.\n"
        f"Prices:\n{price_lines}"
        "Only use these facts. If the answer is not in the facts, "
        "say you do not know and ask the customer to call us. "
        "Answer in at most 3 short sentences."
    ),
}

# Why: messages[0] is always the system message, so /reset and
# trimming never remove the AI's rules.
messages = [system_message]

# Why: counters and accumulators start at 0 BEFORE the loop, so they
# keep the running totals for the session report.
chat_count = 0
menu_count = 0
post_count = 0
price_count = 0
total_tokens = 0
total_seconds = 0

print("=" * 50)
print(f"   {facts['name']} AI Content Studio")
print("=" * 50)
print("Commands: /menu, /post fun|premium|urgent, /price <item>, /reset, bye")

while True:
    user_text = input("You: ").strip()
    # Why: lower() once, so commands work with any capitals
    command = user_text.lower()

    if command == "":
        continue

    if command == "bye":
        print("Studio: Goodbye!")
        break

    if command == "/reset":
        messages = [system_message]
        print("Studio: Chat memory cleared.")
        continue

    if command == "/menu":
        results = []
        for item, price in facts["prices"].items():
            if price == 0:
                print(f"Studio: Skipping {item} (coming soon)")
                continue
            response = creative.invoke([
                {"role": "system", "content": (
                    f"You write menu descriptions for {facts['name']}, "
                    f"a bakery in {facts['city']}. "
                    "Reply with exactly one sentence and nothing else.")},
                {"role": "user", "content": f"Describe this item: {item}"},
            ])
            total_tokens += response.usage_metadata["total_tokens"]
            total_seconds += response.response_metadata["total_duration"] / 1_000_000_000
            results.append({"item": item, "price": price, "text": response.text})
            menu_count += 1

        print("-" * 50)
        for number, entry in enumerate(results, start=1):
            print(f"{number}. {entry['item'].title()} ({entry['price']:,} PKR)")
            print(f"   {entry['text']}")
        print("-" * 50)
        continue

    if command.startswith("/post"):
        tone_name = command[5:].strip()
        # Why: .get() with a default means a wrong tone like "pirate"
        # uses the fun tone instead of crashing with KeyError.
        tone = tones.get(tone_name, tones["fun"])
        print(f"Studio ({tone}):")

        full = None
        # Why: stream() gives the post piece by piece, so the owner
        # sees it appear word by word instead of waiting.
        for chunk in creative.stream([
            {"role": "system", "content": system_message["content"]},
            {"role": "user", "content": (
                f"Write a short Instagram post for {facts['name']}. "
                f"Style: {tone}. Mention one product with its price, "
                "and the opening hours.")},
        ]):
            print(chunk.text, end="", flush=True)
            # Why: adding chunks together gives the final tokens and time
            full = chunk if full is None else full + chunk
        print()

        if full is not None:
            total_tokens += (full.usage_metadata or {}).get("total_tokens", 0)
            total_seconds += full.response_metadata.get("total_duration", 0) / 1_000_000_000
        post_count += 1
        continue

    if command.startswith("/price"):
        item = command[6:].strip()
        # Why: prices come from the dictionary, not the AI, so they are
        # always correct and cost no tokens.
        if item not in facts["prices"]:
            print("Studio: Sorry, that is not on our menu.")
        elif facts["prices"][item] == 0:
            print(f"Studio: {item.title()} is coming soon.")
        else:
            print(f"Studio: {item.title()} costs {facts['prices'][item]:,} PKR.")
        price_count += 1
        continue

    # Anything else is a chat question for the precise model
    messages.append({"role": "user", "content": user_text})
    messages = [messages[0]] + messages[1:][-config["max_messages"]:]
    response = precise.invoke(messages)
    messages.append({"role": "assistant", "content": response.text})

    total_tokens += response.usage_metadata["total_tokens"]
    total_seconds += response.response_metadata["total_duration"] / 1_000_000_000
    chat_count += 1

    print(f"Studio: {response.text}")
    print(f"        (memory: {len(messages)} messages, "
          f"{response.usage_metadata['input_tokens']} tokens sent)")

print("=" * 50)
print("Session report")
print(f"Chat answers: {chat_count} | Menu descriptions: {menu_count} | "
      f"Posts: {post_count} | Price answers: {price_count}")
print(f"AI usage: {total_tokens:,} tokens in {total_seconds:.1f} seconds")
print("=" * 50) 

