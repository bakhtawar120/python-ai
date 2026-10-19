"""Task 1.5: AI Model Profile Card with a token cost estimate."""

model_name = "llama3.2"          # str
context_window = 128000          # int
price_per_1k_tokens = 0.5        # float (example price in PKR, not a real price)
runs_locally = True              # bool


print("--- AI Model Profile Card ---")
print(f"Model: {model_name} {type(model_name)}")
print(f"Context window: {context_window} tokens {type(context_window)}")
print(f"Price per 1K tokens: {price_per_1k_tokens} PKR {type(price_per_1k_tokens)}")
print(f"Runs locally: {runs_locally} {type(runs_locally)}")

# Why: input() always returns text, so int() is needed before doing maths
tokens_per_chat = int(input("Tokens per chat: "))

# Why: price is per 1000 tokens, so divide tokens by 1000 first
cost = tokens_per_chat / 1000 * price_per_1k_tokens

print(f"Estimated cost: {round(cost, 2)} PKR")