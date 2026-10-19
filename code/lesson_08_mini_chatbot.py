"""Task 1.8: City Care Clinic helper bot."""

bot = "City Care Bot"
message_count = 0
unanswered = 0

print(f"{bot}: Hi! Ask about timings, fees, location or appointments. Type 'bye' to exit.")
# Why: ask the name once before the loop, so we do not ask on every message
name = input(f"{bot}: What is your name? ").strip().title()

while True:
    # Why: strip().lower() so capitals and extra spaces never break matching
    message = input(f"{name}: ").strip().lower()
    message_count += 1

    if message == "bye":
        print(f"{bot}: Take care, {name}!")
        break
    # Why: complaint rule comes first so an upset customer is never ignored
    elif "late" in message or "complaint" in message or "problem" in message:
        print(f"{bot}: Sorry about that. The clinic manager will call you today.")
    # Why: short words like "hi" use == / startswith, because "in" would match inside "this"
    elif message == "hi" or message.startswith("hello"):
        print(f"{bot}: Hello {name}! How can I help?")
    elif "timing" in message or "open" in message:
        print(f"{bot}: We are open 10 am to 8 pm, Monday to Saturday.")
    elif "fee" in message or "price" in message or "cost" in message:
        print(f"{bot}: Consultation fee is 2,000 PKR.")
    elif "where" in message or "location" in message or "address" in message:
        print(f"{bot}: We are on Main Boulevard, Lahore.")
    elif "appointment" in message or "book" in message:
        print(f"{bot}: Please call 0300-0000000 to book.")
    else:
        unanswered += 1
        print(f"{bot}: I am not sure yet. In Module 2, an AI will answer: "
              f"You are the friendly assistant of City Care Clinic. "
              f"Answer in 2 lines: {message}")

print("=" * 40)
print(f"Chat summary: {message_count} messages, {unanswered} unanswered.")

