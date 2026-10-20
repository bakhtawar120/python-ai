
"""
This program creates an AI model profile
and calculates the cost of one chat.
"""

# Store the AI model information
model_name = "llama3.2"
context_window = 128000
price = 0.5
runs_locally = True

# Why: Different data types store different kinds of information.
print("--- AI Model Profile Card ---")
print(f"Model: {model_name} {type(model_name)}")
print(f"Context window: {context_window} tokens {type(context_window)}")
print(f"Price per 1K tokens: {price} PKR {type(price)}")
print(f"Runs locally: {runs_locally} {type(runs_locally)}")

# Why: int() converts the user's input into a whole number.
tokens = int(input("Tokens per chat: "))

cost = tokens * price / 1000

print(f"Estimated cost: {round(cost, 2)} PKR")