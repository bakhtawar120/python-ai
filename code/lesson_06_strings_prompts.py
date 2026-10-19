"""Task 1.6: Clean a messy question and build a safe AI prompt."""

# Why: strip() removes extra spaces, title()/capitalize() fix the capitals
name = input("Your name: ").strip().title()
question = input("Your question: ").strip().capitalize()
characters = len(question)
tokens = round(characters / 4)   # rough rule: 1 token is about 4 characters
# Why: lower() makes "PYTHON" and "Python" match "python"
mentions_python = "python" in question.lower()
print("=" * 40)
print(f"Cleaned question: {question}")
print(f"Characters: {characters}, about {tokens} tokens")
print(f"Mentions Python: {mentions_python}")
print("=" * 40)
prompt = f"""You are a friendly Python tutor.
Greet {name} by name and answer in 3 short lines.
Question: {question[:150]}"""
print(prompt)
