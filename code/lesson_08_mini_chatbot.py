"""Glow Beauty Salon Bot: answers common questions and counts the ones it cannot answer."""

print("Glow Bot: Hi! Ask about timings, prices, location or appointments. Type 'bye' to exit.")

# ask the name once, before the loop, so we do not ask it again in every message
user_name = input("Glow Bot: What is your name? ").strip().title()

message_count = 0
unanswered_count = 0

# while True keeps the chat going until we use break
while True:
    # strip() and lower() so " BYE " and "bye" are treated the same
    message = input(f"{user_name}: ").strip().lower()
    message_count += 1

    # complaint rule is first so an angry customer is never given a normal answer
    if "late" in message or "bad" in message or "problem" in message or "angry" in message:
        print("Glow Bot: Sorry about that. The manager will call you today.")
    elif message == "bye":
        print(f"Glow Bot: Take care, {user_name}!")
        break
    elif "timing" in message or "open" in message or "close" in message:
        print("Glow Bot: We are open 11 am to 8 pm, every day.")
    elif "price" in message or "fee" in message or "cost" in message or "how much" in message:
        print("Glow Bot: Haircut is 800 PKR and facial is 2,000 PKR.")
    elif "where" in message or "location" in message or "address" in message:
        print("Glow Bot: We are in Gulberg, Lahore.")
    elif "appointment" in message or "book" in message:
        print("Glow Bot: Call 0300-1234567 to book your appointment.")
    elif message == "hi" or message.startswith("hello"):
        # == and startswith() for short words, because "hi" in "this" would wrongly match
        print(f"Glow Bot: Hello {user_name}! How can I help?")
    else:
        unanswered_count += 1
        print(f"Glow Bot: I am not sure yet. In Module 2, an AI will answer: You are the friendly assistant of Glow Beauty Salon. Answer in 2 lines: {message}")

print("=" * 40)
print(f"Chat summary: {message_count} messages, {unanswered_count} unanswered.")