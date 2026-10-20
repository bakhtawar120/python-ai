"""
This program selects an AI model based on the task
and calculates the estimated cost.
"""

task = input("Task (code / private / chat): ")
task = task.strip().lower()

tokens = int(input("Estimated tokens: "))
paid_user = input("Is this a paid user? (yes/no): ")
paid_user = paid_user.strip().lower()

# Why: Different tasks need different AI models.
if task == "private":
    model = "llama3.2 (local, Ollama)"
    price = 0

elif task == "code":
    model = "claude (cloud, strong at code)"
    price = 0.80

else:
    model = "cheap chat model (cloud)"
    price = 0.20

# Why: Long requests may need to be shortened.
if tokens > 4000:
    print("Warning: long request, consider shortening it.")
else:
    print("Length is fine.")

# Stretch: Free users have a limit for long requests.
if paid_user == "no" and tokens > 2000:
    print("Upgrade to send long requests.")

cost = tokens / 1000 * price

print(f"Chosen model: {model}")
print(f"Estimated cost: {cost:.2f} PKR")
