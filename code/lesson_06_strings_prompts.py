"""
This program cleans the user's name and question,
counts characters, estimates tokens, and builds a prompt.
"""

name = input("Your name: ")
question = input("Your question: ")


name = name.strip().title()
question = question.strip().capitalize()


characters = len(question)
tokens = round(characters / 4)


mentions_python = "python" in question.lower()


question = question.replace("stupid", "***")


prompt = f"""You are a friendly Python tutor.
Greet {name} by name and answer in 3 short lines.
Question: {question[:150]}"""

print("=" * 40)
print(f"Cleaned question: {question}")
print(f"Characters: {characters}, about {tokens} tokens")
print(f"Mentions Python: {mentions_python}")
print("=" * 40)
print(prompt)


price = 0.50
cost = tokens / 1000 * price
print(f"Estimated cost: {cost:.2f} PKR")