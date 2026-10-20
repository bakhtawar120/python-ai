
"""
City Care Clinic Business Helper Bot.
Answers common questions and counts unanswered messages.
"""

print("City Care Bot: Hi! Ask about timings, fees, location or appointments. Type 'bye' to exit.")

name = input("City Care Bot: What is your name? ").strip().title()

messages = 0
unanswered = 0
complaints = 0

while True:
    message = input(f"{name}: ").strip().lower()
    messages += 1

    
    if any(word in message for word in ["complaint", "late", "problem"]):
        complaints += 1
        print("City Care Bot: Sorry about that. The clinic manager will call you today.")

    elif "agent" in message or "human" in message:
        print("City Care Bot: Connecting you to a human...")
        break

    elif message == "bye":
        print(f"City Care Bot: Take care, {name}!")
        break

    
    elif message == "hi" or message.startswith("hi ") or message == "hello" or message.startswith("hello "):
        print("City Care Bot: Hello! How can I help you?")

    elif "timing" in message or "hours" in message or "open" in message:
        print("City Care Bot: We are open 10 am to 8 pm, Monday to Saturday.")

    elif "fee" in message or "price" in message or "cost" in message:
        print("City Care Bot: Consultation fee is 2,000 PKR.")

    elif "location" in message or "address" in message or "where" in message:
        print("City Care Bot: We are located in Lahore.")

    elif "appointment" in message or "book" in message or "booking" in message:
        print("City Care Bot: Please call the clinic to book an appointment.")

    else:
        unanswered += 1
        prompt = (
            "You are the friendly assistant of City Care Clinic. "
            "Answer in 2 lines: " + message
        )
        print("City Care Bot: I am not sure yet. In Module 2, an AI will answer: " + prompt)

    

print("=" * 40)
print(f"Chat summary: {messages} messages, {unanswered} unanswered.")
print(f"Complaints received: {complaints}")