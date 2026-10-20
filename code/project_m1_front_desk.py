"""
Sweet Crumbs Front Desk Assistant
Answers common bakery questions, calculates quotes, and prepares AI prompts
for questions that the rules cannot answer.
"""

BOT_NAME = "Sweet Crumbs Desk"
BUSINESS_NAME = "Sweet Crumbs bakery"
DELIVERY_FEE = 200
FREE_DELIVERY_LIMIT = 3000
CLOUD_PRICE_PER_1K_TOKENS = 0.10  # Example estimate only; not a verified provider price.
LOCAL_MODEL = "llama3.2 (local, private)"
CLOUD_MODEL = "small cloud model (cheap)"

print("=" * 50)
print(f"   {BOT_NAME}: rules, quotes and AI-ready prompts")
print("=" * 50)
print("Ask anything, type /quote for a price, or bye to exit.")

customer_name = input(f"{BOT_NAME}: What is your name? ").strip().title()
if customer_name == "":
    customer_name = "Customer"

# Counters start before the loop so their values are kept for the whole session.
messages = 0
answered_by_rules = 0
unanswered = 0
number_of_quotes = 0
total_quoted_value = 0
total_ai_cost = 0.0
complaints = 0

while True:
    message = input(f"{customer_name}: ").strip().lower()
    messages += 1

    if message == "":
        print(f"{BOT_NAME}: Please type a question, /quote, or bye.")
        continue

    # Complaints are checked first so unhappy customers get priority.
    if "refund" in message or "complaint" in message or "late" in message:
        complaints += 1
        answered_by_rules += 1
        print(f"{BOT_NAME}: Sorry about that. A manager will call you within 1 hour.")

    elif "agent" in message or "human" in message:
        print(f"{BOT_NAME}: Connecting you to a human...")
        break

    elif message == "bye":
        print(f"{BOT_NAME}: Goodbye, {customer_name}!")
        break

    elif message == "/quote":
        item = input(f"{BOT_NAME}: Which item? ").strip().lower()
        quantity_text = input(f"{BOT_NAME}: How many? ").strip()

        # isdigit() avoids a ValueError when a beginner enters letters for quantity.
        if not quantity_text.isdigit():
            print(f"{BOT_NAME}: Please enter the quantity as a whole number, such as 2.")
            answered_by_rules += 1
        else:
            quantity = int(quantity_text)

            if quantity <= 0:
                print(f"{BOT_NAME}: Quantity must be at least 1.")
                answered_by_rules += 1
            else:
                if item == "cupcake" or item == "cupcakes":
                    item_price = 250
                    item_name = "cupcake"
                elif item == "brownie" or item == "brownies":
                    item_price = 300
                    item_name = "brownie"
                elif item == "chocolate cake" or item == "chocolate cakes":
                    item_price = 1500
                    item_name = "chocolate cake"
                else:
                    item_price = 0
                    item_name = item

                if item_price == 0:
                    print(f"{BOT_NAME}: Sorry, {item} is not on our menu.")
                    answered_by_rules += 1
                else:
                    subtotal = item_price * quantity
                    discount = 0

                    # The discount is calculated before delivery is checked.
                    if quantity >= 10:
                        discount = subtotal * 0.10

                    discounted_subtotal = subtotal - discount

                    # Free delivery is based on the discounted subtotal.
                    if discounted_subtotal >= FREE_DELIVERY_LIMIT:
                        delivery = 0
                    else:
                        delivery = DELIVERY_FEE

                    total = discounted_subtotal + delivery
                    print(f"{BOT_NAME}: {quantity:,} x {item_name} = {subtotal:,.0f} PKR")
                    print(f"     Discount: -{discount:,.0f} PKR | Delivery: {delivery:,.0f} PKR")
                    print(f"     Total: {total:,.0f} PKR")

                    number_of_quotes += 1
                    total_quoted_value += total
                    answered_by_rules += 1

    elif message == "hi" or message.startswith("hi ") or message == "hello" or message.startswith("hello ") or message == "salam" or message.startswith("salam "):
        answered_by_rules += 1
        print(f"{BOT_NAME}: Welcome to Sweet Crumbs! How can I help you?")

    elif "hour" in message or "timing" in message or "open" in message:
        answered_by_rules += 1
        print(f"{BOT_NAME}: We are open 9 AM to 10 PM every day.")

    elif "location" in message or "where are you" in message:
        answered_by_rules += 1
        print(f"{BOT_NAME}: Please contact our staff for the bakery location.")

    elif "delivery" in message or "deliver" in message or "shipping" in message:
        answered_by_rules += 1
        print(f"{BOT_NAME}: Delivery costs {DELIVERY_FEE} PKR. It is free for orders of {FREE_DELIVERY_LIMIT:,} PKR or more after discount.")

    elif "contact" in message:
        answered_by_rules += 1
        print(f"{BOT_NAME}: Please contact our staff for assistance.")

    else:
        unanswered += 1
        clean_question = message.capitalize()[:150]
        estimated_tokens = round(len(clean_question) / 4)

        # Private details stay with a local model; only other questions get a cloud estimate.
        if "phone" in message or "cnic" in message or "address" in message:
            chosen_model = LOCAL_MODEL
            estimated_cost = 0.0
        else:
            chosen_model = CLOUD_MODEL
            estimated_cost = estimated_tokens / 1000 * CLOUD_PRICE_PER_1K_TOKENS

        total_ai_cost += estimated_cost
        print(f"{BOT_NAME}: Good question! Routed to: {chosen_model} (~{estimated_tokens} tokens)")
        print(f"""     Prompt: You are the assistant of {BUSINESS_NAME}.
     Answer {customer_name} in 2 short lines. Question: {clean_question}""")

print("=" * 50)
print("Session report")
print(f"Messages: {messages} | Answered by rules: {answered_by_rules} | Unanswered: {unanswered}")
print(f"Quotes: {number_of_quotes} | Quoted value: {total_quoted_value:,.0f} PKR")
print(f"Estimated AI cost for unanswered questions: {total_ai_cost:.4f} PKR")
print(f"Complaints received: {complaints}")
print("=" * 50)