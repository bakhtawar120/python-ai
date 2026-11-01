"""Task 2.7: Order Extractor for Sweet Crumbs Bakery.

Turns messy WhatsApp orders (English and Roman Urdu) into clean,
checked data. The AI fills a JSON schema, Python checks every reply
and calculates the totals, and the orders are saved to orders.json
(and orders.csv).
"""

import json

from langchain.chat_models import init_chat_model

PRICES = {
    "chocolate cake": 1500,
    "cupcake": 250,
    "brownie": 300,
    "donut": 200,
}

# Why: a mix of cases so we can test every check: normal, many items,
# off-menu item, not an order, and Roman Urdu.
messages = [
    "Hi, I want 1 brownie. Sara, DHA Phase 5",
    "Salam! 2 cupcakes aur 1 chocolate cake chahiye. Ali, house 12 Gulberg",
    "1 pizza and 2 brownies, Bilal, Model Town",
    "hi do you deliver to Johar Town?",
    "Assalam o alaikum, mujhe 3 donuts chahiye. Ayesha, Bahria Town",
]

# Why: the schema is the "form" the AI must fill. With format= the
# reply is always valid JSON with these keys.
schema = {
    "type": "object",
    "properties": {
        "is_order": {"type": "boolean"},
        "customer": {"type": "string"},
        "address": {"type": "string"},
        "items": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "quantity": {"type": "integer"},
                },
                "required": ["name", "quantity"],
            },
        },
    },
    "required": ["is_order", "customer", "address", "items"],
}

# Why: temperature 0 means the same message gives the same data every
# time, which is what we want for extraction (no creativity needed).
extractor = init_chat_model(
    "gemma4:31b-cloud",
    model_provider="ollama",
    temperature=0,
    format=schema,
)

system_text = (
    "Extract the order from the customer message. "
    "Set is_order to false if the message is not an order. "
    "Use singular lowercase item names like 'cupcake'. "
    "Use an empty string if the customer name or address is missing. "
    "Never invent a name."
)

saved_orders = []
orders_found = 0
total_value = 0
checks = 0

for text in messages:
    print(f"Message: {text}")
    response = extractor.invoke([
        {"role": "system", "content": system_text},
        {"role": "user", "content": text},
    ])

    # Why: even with a schema, we never trust the reply blindly. If
    # the JSON is broken we report it and move on, not crash.
    try:
        data = json.loads(response.text)
    except json.JSONDecodeError:
        print("  CHECK: the AI reply was not valid JSON")
        checks += 1
        print()
        continue

    if not data.get("is_order", False):
        print("  Not an order: needs a human reply.")
        print()
        continue

    customer = data.get("customer", "")
    address = data.get("address", "")

    # Why: the AI can invent a name. A real name must appear in the
    # message text, so we check that.
    if customer == "" or customer.lower() not in text.lower():
        print(f"  CHECK: customer name '{customer}' is not in the message")
        checks += 1
        customer = ""

    order_total = 0
    order_items = []
    for item in data.get("items", []):
        name = str(item.get("name", "")).lower().strip()
        quantity = item.get("quantity", 1)
        if not isinstance(quantity, int) or quantity < 1:
            quantity = 1

        # Why: an item that is not on our menu must never get a price.
        if name not in PRICES:
            print(f"  CHECK: '{name}' is not on the menu")
            checks += 1
            continue

        # Why: Python does the maths. The AI can make arithmetic mistakes.
        line_total = PRICES[name] * quantity
        order_total += line_total
        order_items.append(
            {"item": name, "quantity": quantity, "line_total": line_total}
        )
        print(f"  {quantity} x {name} = {line_total:,} PKR")

    if order_items:
        print(f"  Customer: {customer}, Address: {address}")
        print(f"  Total: {order_total:,} PKR")
        saved_orders.append({
            "customer": customer,
            "address": address,
            "items": order_items,
            "total": order_total,
        })
        orders_found += 1
        total_value += order_total
    print()

with open("orders.json", "w", encoding="utf-8") as file:
    json.dump(saved_orders, file, indent=2, ensure_ascii=False)

# Stretch: one line per item, opened in Excel or Google Sheets
with open("orders.csv", "w", encoding="utf-8") as file:
    file.write("customer,item,quantity,line_total\n")
    for order in saved_orders:
        for line in order["items"]:
            file.write(
                f"{order['customer']},{line['item']},"
                f"{line['quantity']},{line['line_total']}\n"
            )

print("=" * 50)
print(f"Orders found: {orders_found} | Total value: {total_value:,} PKR | Checks: {checks}")
print(f"Saved {orders_found} orders to orders.json")

