"""AI Front Desk for Sweet Crumbs bakery: answers FAQs with rules,
gives exact price quotes, and turns other questions into AI prompts."""

BOT_NAME = "Sweet Crumbs Desk"
DELIVERY_FEE = 200
FREE_DELIVERY_LIMIT = 3000
CLOUD_PRICE_PER_1K = 0.1   # example price in PKR, not a real price

message_count = 0
rule_answers = 0
unanswered = 0
quote_count = 0
quoted_value = 0
total_ai_cost = 0
complaints = 0

print("=" * 50)
print(f"   {BOT_NAME}: rules, quotes and AI-ready prompts")
print("=" * 50)
print("Ask anything, type /quote for a price, or bye to exit.")
# Why: ask the name once before the loop, so we never repeat the question
name = input(f"{BOT_NAME}: What is your name? ").strip().title()

while True:
    # Why: strip().lower() so capitals and extra spaces never break matching
    message = input(f"{name}: ").strip().lower()

    # Why: an empty message is not a real question, so do not count it
    if message != "":
        message_count += 1

    if message == "":
        print(f"{BOT_NAME}: Please type a question, or bye to exit.")
    # Why: complaint rule is first so an unhappy customer always reaches a human
    elif "refund" in message or "complaint" in message or " late" in message:
        rule_answers += 1
        complaints += 1
        print(f"{BOT_NAME}: Sorry about that. A manager will call you within 1 hour.")
    elif message == "agent" or message == "human":
        print(f"{BOT_NAME}: Connecting you to a human...")
        break
    elif message == "bye":
        rule_answers += 1
        print(f"{BOT_NAME}: Goodbye, {name}!")
        break
    # Why: short words like "hi" use == / startswith, because "in" matches "which"
    elif message == "hi" or message.startswith("hello"):
        rule_answers += 1
        print(f"{BOT_NAME}: Hello {name}! How can I help?")
    elif "hour" in message or "open" in message or "timing" in message:
        rule_answers += 1
        print(f"{BOT_NAME}: We are open 9 am to 10 pm, every day.")
    elif "where" in message or "location" in message:
        rule_answers += 1
        print(f"{BOT_NAME}: We are on Main Boulevard, Lahore.")
    elif "deliver" in message:
        rule_answers += 1
        print(f"{BOT_NAME}: We deliver across the city. Fee {DELIVERY_FEE:,} PKR, free from {FREE_DELIVERY_LIMIT:,} PKR.")
    elif "price" in message or "cost" in message or "how much" in message:
        rule_answers += 1
        print(f"{BOT_NAME}: Type /quote to get an exact price.")
    elif message == "/quote":
        item = input(f"{BOT_NAME}: Which item? ").strip().lower()
        quantity_text = input(f"{BOT_NAME}: How many? ").strip()
        # Why: isdigit() stops a crash when the customer types letters
        if not quantity_text.isdigit():
            print(f"{BOT_NAME}: Please type the quantity as a whole number, like 12.")
        else:
            quantity = int(quantity_text)
            if item == "cupcake":
                unit_price = 250
            elif item == "brownie":
                unit_price = 300
            elif item == "chocolate cake":
                unit_price = 1500
            else:
                unit_price = 0

            if unit_price == 0:
                print(f"{BOT_NAME}: Sorry, {item} is not on our menu.")
            else:
                subtotal = unit_price * quantity
                if quantity >= 10:
                    discount = round(subtotal * 0.10)
                else:
                    discount = 0
                # Why: delivery is checked AFTER the discount, because the customer pays the lower amount
                after_discount = subtotal - discount
                if after_discount >= FREE_DELIVERY_LIMIT:
                    delivery = 0
                else:
                    delivery = DELIVERY_FEE
                total = after_discount + delivery

                quote_count += 1
                quoted_value += total
                print(f"{BOT_NAME}: {quantity} x {item} = {subtotal:,} PKR")
                print(f"     Discount: -{discount:,} PKR | Delivery: {delivery:,} PKR")
                print(f"     Total: {total:,} PKR")
    else:
        unanswered += 1
        question = message.capitalize()[:150]
        tokens = round(len(question) / 4)

        # Why: private details must never go to a cloud model, so route them locally
        if "phone" in message or "cnic" in message or "my address" in message:
            model = "llama3.2 (local, private)"
            price = 0
        else:
            model = "small cloud model (cheap)"
            price = CLOUD_PRICE_PER_1K

        total_ai_cost += tokens / 1000 * price

        prompt = f"""You are the assistant of Sweet Crumbs bakery.
Answer {name} in 2 short lines. Question: {question}"""
        print(f"{BOT_NAME}: Good question! Routed to: {model} (~{tokens} tokens)")
        print(f"     Prompt: {prompt}")

print("=" * 50)
print("Session report")
print(f"Messages: {message_count} | Answered by rules: {rule_answers} | Unanswered: {unanswered}")
print(f"Quotes: {quote_count} | Quoted value: {quoted_value:,} PKR")
print(f"Complaints: {complaints}")
print(f"Estimated AI cost for unanswered questions: {total_ai_cost:.4f} PKR")
print("=" * 50)
