"""Task 2.4 Stretch: Bot Battle.

Runs the same test questions through the Lesson 1.8 if/elif rules and
through a real AI, prints both answers, and counts how many questions
the rules could not answer.
"""

from langchain.chat_models import init_chat_model

# Why: at least 6 questions. Some match the old rules, some do not,
# so we can see where the rules fail.
questions = [
    "What are your timings?",
    "How much is the consultation fee?",
    "Where is the clinic?",
    "I want to book an appointment",
    "Do you have a dentist?",
    "Is the doctor available on Sunday?",
    "Do you accept insurance?",
    "My doctor was late",
]


def rules_answer(message):
    """Lesson 1.8 rules. Returns the answer, or None if no rule matches."""
    # Why: strip().lower() so capitals and spaces never break matching
    message = message.strip().lower()

    if "late" in message or "complaint" in message or "problem" in message:
        return "Sorry about that. The clinic manager will call you today."
    elif message == "hi" or message.startswith("hello"):
        return "Hello! How can I help?"
    elif "timing" in message or "open" in message:
        return "We are open 10 am to 8 pm, Monday to Saturday."
    elif "fee" in message or "price" in message or "cost" in message:
        return "Consultation fee is 2,000 PKR."
    elif "where" in message or "location" in message or "address" in message:
        return "We are on Main Boulevard, Lahore."
    elif "appointment" in message or "book" in message:
        return "Please call 0300-0000000 to book."
    # Why: returning None (not text) lets us count the failures later
    return None


# Why: the model is created once, before the loop, to save time.
llm = init_chat_model(
    "gemma4:31b-cloud",
    model_provider="ollama",
    temperature=0.2,
)

# Why: the AI gets the same real facts as the rules and must only use
# them, so it cannot invent timings or fees.
system_message = (
    "You are the friendly assistant of City Care Clinic. "
    "Facts: open 10 am to 8 pm, Monday to Saturday. "
    "Consultation fee is 2,000 PKR. Address: Main Boulevard, Lahore. "
    "Phone: 0300-0000000. Only use these facts. If the answer is not "
    "in the facts, say you do not know and ask the patient to call us. "
    "Answer in 2 short lines."
)

# Why: the counter starts at 0 BEFORE the loop so it keeps its total.
rules_failed = 0

for number, question in enumerate(questions, start=1):
    rule_reply = rules_answer(question)

    if rule_reply is None:
        rules_failed += 1
        rule_reply = "(no rule matched)"

    response = llm.invoke(
        [
            {"role": "system", "content": system_message},
            {"role": "user", "content": question},
        ]
    )

    print(f"{number}. Question: {question}")
    print(f"   Rules: {rule_reply}")
    print(f"   AI:    {response.text}")
    print("-" * 50)

print(f"Rules could not answer {rules_failed} of {len(questions)} questions.")