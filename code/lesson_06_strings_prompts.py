"""Prompt Cleaner: cleans a messy name and question before sending them to an AI."""

name = input("Your name: ")
question = input("Your question: ")

# strip() removes extra spaces, title() makes each word start with a capital
clean_name = name.strip().title()
# capitalize() makes only the first letter big, like a normal sentence
clean_question = question.strip().capitalize()

print("=" * 40)
print(f"Cleaned question: {clean_question}")

# len() counts characters, and 1 token is roughly 4 characters
characters = len(clean_question)
estimated_tokens = round(characters / 4)
print(f"Characters: {characters}, about {estimated_tokens} tokens")

# lower() so "Python", "PYTHON" and "python" all match
mentions_python = "python" in clean_question.lower()
print(f"Mentions Python: {mentions_python}")
print("=" * 40)

# [:150] limits the question to 150 characters so the prompt stays short and cheap
prompt = f"""You are a friendly Python tutor.
Greet {clean_name} by name and answer in 3 short lines.
Question: {clean_question[:150]}"""
print(prompt)
