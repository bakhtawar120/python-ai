"""Task 1.7: Route a request to the right AI model and estimate cost."""

# Why: strip().lower() so " Code " still matches "code"
task = input("Task (code / private / chat): ").strip().lower()
tokens = int(input("Estimated tokens: "))
if task == "code":
    model = "claude (cloud, strong at code)"
    price = 0.8
elif task == "private":
    model = "llama3.2 (local, Ollama)"
    price = 0      # Why: a local model runs on your machine, so no API cost
else:
    model = "a cheap cloud model"
    price = 0.2
    cost = tokens / 1000 * price

if tokens > 4000:
    print("Warning: long request, consider shortening it.")
else:
    print("Length is fine.")
    print(f"Chosen model: {model}")
print(f"Estimated cost: {cost:.2f} PKR")

paid = input("Is this a paid user? (yes/no) ").strip().lower()
if paid == "no" and tokens > 2000:
    print("Upgrade to send long requests.")
    
