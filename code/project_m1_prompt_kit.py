"""AI Prompt Kit for a Local Business

This tool asks a small business owner 5 simple questions and then prints
3 ready-to-use AI prompts (marketing, customer service, growth).

Who it is for: shop owners (bakery, clinic, salon, tuition centre...) who
want help from AI but do not know what to type.
"""

# Ask the questions first, because every prompt below depends on these answers.
business_name = input("Business name: ")
business_type = input("Business type: ")
city = input("City: ")
customers = input("Main customers: ")

# input() always returns text, so we convert the budget to a number with int().
# This lets us use it as a real number later (for example, for calculations).
budget = int(input("Monthly budget (PKR): "))

# A reusable separator line keeps the output clean and easy to read.
line = "=" * 41

# Header
print()
print(line)
print(f"   AI Prompt Kit for {business_name}")
print(line)

# Prompt 1: a good prompt names a task, audience, tone and a number.
# That is why we ask for ONE call to action and a friendly tone.
prompt_marketing = (
    f"Write a short Instagram post for {business_name}, a {business_type} in {city}.\n"
    f"Target {customers}. Friendly tone, 1 call to action."
)

# Prompt 2: giving the AI a role ("manager") makes the reply sound
# professional instead of generic.
prompt_service = (
    f"You are the manager of {business_name}. Write a polite reply to a customer\n"
    f"whose order arrived late. Apologise and offer a small discount."
)

# Prompt 3: putting the budget inside the prompt stops the AI from suggesting
# expensive tools the owner cannot afford.
prompt_growth = (
    f"Suggest 3 low-cost AI tools a {business_type} in {city} can use\n"
    f"to attract {customers} with a budget of {budget} PKR per month."
)

# Print each prompt with a label
print()
print("[1] Marketing")
print(prompt_marketing)

print()
print("[2] Customer Service")
print(prompt_service)

print()
print("[3] Growth")
print(prompt_growth)

print()
print(line)
print("Copy each prompt into Ollama, Claude or ChatGPT.")
print(line)
