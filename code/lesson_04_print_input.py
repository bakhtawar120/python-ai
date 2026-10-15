

# Asking for inputs directly makes the tool interactive for clients
name = input("Your name: ")
business = input("Business type: ")
problem = input("Biggest problem: ")
budget = int(input("Monthly budget in PKR: "))  # Why: converting ensures numeric use

# Why comment: welcoming the user makes the tool feel personal
print(f"\nWelcome, {name}!")

print("--- Your AI Prompt ---")

# Why comment: using f-strings ensures the prompt is dynamic and reusable
print(f"Suggest 3 AI solutions for a {business} that struggles with {problem}.")
print(f"Budget: {budget} PKR per month.")
