"""Task 2.8: Your First Agent for Sweet Crumbs Bakery.

An agent that uses tools: it reads prices, checks an order status,
answers FAQs from faq.json, and places orders only after the owner
approves. The agent loop lets the AI call tools until it has an
answer, with a MAX_STEPS safety limit.
"""

import json

from langchain.chat_models import init_chat_model
from langchain_core.messages import ToolMessage
from langchain_core.tools import tool
from pydantic import ValidationError

MODEL = "gemma4:31b-cloud"
MAX_STEPS = 5

PRICES = {
    "chocolate cake": 1500,
    "cupcake": 250,
    "brownie": 300,
    "donut": 200,
}

# Why: a simple dictionary acts as our order database for this task.
ORDERS = {
    "A101": "delivered",
    "A102": "out for delivery",
    "A103": "being baked",
}


@tool(parse_docstring=True)
def get_price(item: str) -> str:
    """Get the price of one menu item.

    Args:
        item: The menu item name, for example brownie or cupcake.
    """
    price = PRICES.get(item.lower().strip())
    if price is None:
        return f"{item} is not on our menu"
    return f"{item} costs {price} PKR"


@tool(parse_docstring=True)
def order_status(order_id: str) -> str:
    """Check the status of an existing order.

    Args:
        order_id: The order number, for example A102.
    """
    status = ORDERS.get(order_id.upper().strip())
    if status is None:
        return f"Order {order_id} was not found"
    return f"Order {order_id.upper()} is {status}"


@tool(parse_docstring=True)
def place_order(item: str, quantity: int, customer: str) -> str:
    """Place a new order for a customer after the owner approves it.

    Args:
        item: The menu item to order.
        quantity: How many pieces the customer wants.
        customer: The customer's name.
    """
    price = PRICES.get(item.lower().strip())
    if price is None:
        return f"Cannot order: {item} is not on our menu"
    total = price * quantity

    # Why: placing an order spends the owner's time and money, so the
    # human must say yes first. The AI can never skip this step.
    answer = input(
        f"  [approve] {quantity} x {item} for {customer} = {total} PKR. "
        "Place it? (yes/no) "
    ).strip().lower()
    if answer != "yes":
        return "The owner said no. The order was NOT placed."

    order_id = f"A{104 + len(ORDERS) - 3}"
    ORDERS[order_id] = "being baked"
    return f"Order {order_id} placed: {quantity} x {item}, total {total} PKR"


@tool(parse_docstring=True)
def read_faq(topic: str) -> str:
    """Read a fact from the owner's faq.json file, like hours or delivery.

    Args:
        topic: The fact to look up: name, city, hours, phone or delivery.
    """
    # Stretch: the agent answers FAQs from the owner's own file
    try:
        with open("faq.json", encoding="utf-8") as file:
            faq = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return "The FAQ file is not available"
    return str(faq.get(topic.lower().strip(), f"No FAQ entry for {topic}"))


# Why: the dictionary connects the tool name the AI says to the real
# Python function we run. An unknown name is simply not in it.
TOOLS = {
    "get_price": get_price,
    "order_status": order_status,
    "place_order": place_order,
    "read_faq": read_faq,
}

llm = init_chat_model(MODEL, model_provider="ollama", temperature=0)
# Why: bind_tools tells the AI which tools exist and what they need.
llm_with_tools = llm.bind_tools(list(TOOLS.values()))

# Why: memory is just this list. Every question, tool call and answer
# is appended, so the agent remembers earlier questions.
messages = [{
    "role": "system",
    "content": (
        "You are the assistant of Sweet Crumbs Bakery in Lahore. "
        "Use the tools for prices, order status, FAQs and orders. "
        "Never guess a price. Answer in at most 3 short sentences."
    ),
}]

print("Sweet Crumbs Agent: ask about prices, orders, or place an order. Type 'bye' to exit.")

while True:
    user_text = input("You: ").strip()
    if user_text == "":
        continue
    if user_text.lower() == "bye":
        break

    messages.append({"role": "user", "content": user_text})

    # Why: for ... else. The else part runs only if the loop used all
    # MAX_STEPS without a break, so the agent never loops forever.
    for step in range(MAX_STEPS):
        ai_message = llm_with_tools.invoke(messages)
        messages.append(ai_message)

        if not ai_message.tool_calls:
            print(f"Agent: {ai_message.text}")
            break

        for call in ai_message.tool_calls:
            name = call["name"]
            args = call["args"]

            if name not in TOOLS:
                result = f"Error: there is no tool called {name}"
            else:
                try:
                    result = TOOLS[name].invoke(args)
                except ValidationError:
                    result = f"Error: wrong arguments for {name}: {args}"

            print(f"  [tool] {name}({args}) -> {result}")
            # Why: tool_call_id links this result to the AI's request,
            # so the AI knows which call it answers.
            messages.append(
                ToolMessage(content=str(result), tool_call_id=call["id"])
            )
    else:
        print("Agent: Sorry, I could not finish that. Please ask again.")
        