"""Module 1 Project: AI Prompt Kit.

Asks for business details, prints three ready-made prompts, and (Task 2.1
stretch) sends Prompt 1 to a real AI and prints its answer, so there is
no copy-pasting.
"""

from langchain.chat_models import init_chat_model

business_name = input("Business name: ")
business_type = input("Business type: ")
city = input("City: ")
customers = input("Main customers: ")
# Why: input() always gives text, so budget is converted with int()
budget = int(input("Monthly budget (PKR): "))

# Why: each prompt has a role, a task, an audience and a tone, so the
# AI answer is specific. Prompt 1 is stored in a variable so we can
# both print it and send the same text to the AI.
prompt_1 = (
    "You are a social media manager. "
    f"Write a short Instagram post for {business_name}, a {business_type} "
    f"in {city}. The audience is {customers}. Tone: warm and stylish. "
    "Write 3 short sentences plus 5 hashtags. Reply with the post only."
)

prompt_2 = (
    f"You are the manager of {business_name}, a {business_type} in {city}. "
    f"A customer ({customers}) is unhappy because her order arrived late. "
    "Write a polite reply in 3 short sentences. Say sorry, offer a "
    "solution, and keep a friendly tone."
)

prompt_3 = (
    f"You are a business advisor for a {business_type} in {city}. "
    f"Suggest 3 low-cost AI tools that {business_name} can use to reach "
    f"{customers}. The budget is {budget:,} PKR per month. "
    "For each tool give the name, one use and the approximate cost."
)

# Why: the header shows the business name so the output feels personal
print("\n=========================================")
print(f"   AI Prompt Kit for {business_name}")
print("=========================================")

print("\n[1] Marketing")
print(prompt_1)

print("\n[2] Customer Service")
print(prompt_2)

print("\n[3] Growth")
print(prompt_3)

# Stretch: send Prompt 1 to the AI
# Why: temperature 0.7 gives a creative, varied post, which is good
# for marketing text.
llm = init_chat_model("gemma4:31b-cloud", model_provider="ollama", temperature=0.7)
response = llm.invoke(prompt_1)

print("\n--- AI answer to Prompt 1 ---")
print(response.text)