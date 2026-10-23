"""Task 2.4: Batch Product Writer.

Writes a one-sentence menu description for every product of a small
business in a single run. Items with price 0 are skipped. At the end it
prints a numbered menu and a summary with the total tokens and seconds.
"""

from langchain.chat_models import init_chat_model

# Why: "Old stock" is first so the "Skipping" line prints before the menu,
# like the expected output. It has price 0, so it will be skipped.
products = {
    "Old stock": 0,
    "Chocolate Cake": 1500,
    "Cupcake": 250,
    "Brownie": 300,
    "Donut": 200,
}

# Why: the model is created once, before the loop. Creating it for
# every item would be slow and wasteful.
llm = init_chat_model(
    "gemma4:31b-cloud",
    model_provider="ollama",
    temperature=0.2,
)

# Why: accumulators must start at 0 BEFORE the loop. If we put them
# inside the loop they would reset to 0 on every item and we would
# lose the running total.
total_tokens = 0
total_seconds = 0

# Why: a list of dictionaries keeps item, price and text together, so
# we can print the numbered menu after the loop.
results = []

for name, price in products.items():
    # Why: a price of 0 means the item is not for sale. continue skips
    # the AI call, so no tokens or time are spent on it.
    if price == 0:
        print(f"Skipping {name.lower()} (no price)")
        continue

    messages = [
        {
            "role": "system",
            "content": (
                "You write menu descriptions for a bakery. "
                "Reply with exactly one sentence and nothing else."
            ),
        },
        {"role": "user", "content": f"Describe this item: {name}"},
    ]

    response = llm.invoke(messages)

    # Why: Ollama gives the duration in nanoseconds, so we divide by
    # 1 billion to get seconds.
    total_tokens += response.usage_metadata["total_tokens"]
    total_seconds += response.response_metadata["total_duration"] / 1_000_000_000

    results.append({"item": name, "price": price, "text": response.text})

print("=" * 50)
for number, entry in enumerate(results, start=1):
    print(f"{number}. {entry['item']} ({entry['price']} PKR)")
    print(f"   {entry['text']}")
print("=" * 50)
print(f"{len(results)} descriptions, {total_tokens} tokens, {total_seconds:.1f} seconds")

