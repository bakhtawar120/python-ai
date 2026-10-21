"""Smart Model Router: picks a model by task type and estimates the cost."""

# strip() and lower() so " Code " and "CODE" both work
task = input("Task (code / private / chat): ").strip().lower()
# int() because input() always returns text
tokens = int(input("Estimated tokens: "))

# each task type goes to the model that suits it best
if task == "code":
    model = "claude (cloud, strong at code)"
    price = 0.8
elif task == "private":
    model = "llama3.2 (local, Ollama)"
    price = 0  # local model is free, so price is 0
else:
    model = "gemini flash (cloud, cheap)"
    price = 0.2

cost = (tokens / 1000) * price

if tokens > 4000:
    print("Warning: long request, consider shortening it.")
else:
    print("Length is fine.")

print(f"Chosen model: {model}")
print(f"Estimated cost: {cost:.2f} PKR")
