"""Business Prompt Builder: asks for business details and prints a ready-to-use AI prompt."""

# input() always returns text, so we store each answer as a string variable
name = input("BAKHTAWAR KHAN ")
business = input("marketing agency ")
problem = input("reaching the right audience on social media ")

# int() converts the typed text into a number, because input() never gives numbers directly
budget = int(input("Monthly budget in PKR:: 20000  "))

print(f"\nWelcome, {name}!")

# An f-string keeps the prompt readable and avoids messy string joining
prompt = (
    f"Suggest 3 AI solutions for a {business} that struggles with {problem}. "
    f"Budget: {budget} PKR per month."
)

print("--- Your AI Prompt ---")
print(prompt)


