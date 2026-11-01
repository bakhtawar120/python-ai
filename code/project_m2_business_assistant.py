"""AI Business Assistant for Sweet Crumbs Bakery (Module 2 final).

An agent that answers from business.json, uses tools to read prices,
read business info, check orders and place orders (only after the
owner approves), turns WhatsApp messages into checked orders with
/import, saves everything to JSON files, logs errors, and prints a
session report at the end. The agent loop is written by hand.
"""

import json
import sys
from datetime import datetime

import httpx
import ollama
from langchain.chat_models import init_chat_model
from langchain_core.messages import ToolMessage
from langchain_core.tools import tool
from pydantic import ValidationError

# Why: constants in UPPER_CASE at the top, so a setting (model, limit,
# file name) is changed in one place and not hunted through the code.
MODEL = "gemma4:31b-cloud"
MAX_STEPS = 5
MEMORY_SIZE = 8
BUSINESS_FILE = "business.json"
ORDERS_FILE = "orders.json"
TRANSCRIPT_FILE = "transcript.json"
ERROR_LOG = "errors.log"

SCHEMA = {
    "type": "object",
    "properties": {
        "is_order": {"type": "boolean"},
        "customer": {"type": "string"},
        "address": {"type": "string"},
        "items": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "quantity": {"type": "integer"},
                },
                "required": ["name", "quantity"],
            },
        },
    },
    "required": ["is_order", "customer", "address", "items"],
}


# ---------- helper functions ----------

def load_json(path: str, default: list) -> list:
    """Load a JSON list from a file. Missing or damaged files give the default."""
    # Why: a missing file is normal on the first run, a damaged file
    # is a warning. Both start fresh instead of crashing.
    try:
        with open(path, encoding="utf-8") as file:
            data = json.load(file)
        if not isinstance(data, list):
            raise ValueError("expected a list")
        return data
    except FileNotFoundError:
        return default
    except (json.JSONDecodeError, ValueError):
        print(f"Warning: {path} was damaged. Starting fresh.")
        return default


def save_json(path: str, data: list) -> None:
    """Save data to a JSON file, readable and with Urdu letters kept."""
    with open(path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=2, ensure_ascii=False)


def log_error(error: Exception) -> None:
    """Append one error line with the time to errors.log."""
    with open(ERROR_LOG, "a", encoding="utf-8") as file:
        file.write(f"{datetime.now():%Y-%m-%d %H:%M} {type(error).__name__}: {error}\n")


def friendly_message(error: Exception) -> str:
    """Return a message a customer can read for an AI error."""
    if isinstance(error, ollama.ResponseError):
        return "Something went wrong with the AI. Please try again in a moment."
    return "I am offline right now. Please open the Ollama app and try again."


def calculate_total(price: int, quantity: int) -> int:
    """Return price multiplied by quantity (the maths is done in Python, not by the AI)."""
    return price * quantity


def clean_json_text(text: str) -> str:
    """Return only the part of a text between the first { and the last }."""
    # Why: some models wrap JSON in ```json fences or add words around
    # it, and json.loads only accepts clean JSON.
    start = text.find("{")
    end = text.rfind("}")
    if start == -1 or end == -1:
        return text
    return text[start:end + 1]


def normalize_item(name: str, prices: dict) -> str:
    """Lowercase an item name and turn a plural like 'cupcakes' into 'cupcake'."""
    name = name.lower().strip()
    if name not in prices and name.endswith("s") and name[:-1] in prices:
        name = name[:-1]
    return name


def make_order_id(orders_list: list) -> str:
    """Return the next order id: A101, A102, ..."""
    return f"A{101 + len(orders_list)}"


# Why: assert tests check the functions that need no AI. If one fails,
# Python stops and shows which function is broken.
assert calculate_total(300, 2) == 600
assert calculate_total(250, 0) == 0
assert normalize_item("Cupcakes", {"cupcake": 250}) == "cupcake"
assert make_order_id([]) == "A101"
assert make_order_id([{}, {}]) == "A103"
assert clean_json_text('```json\n{"a": 1}\n```') == '{"a": 1}'


# ---------- load the data ----------

# Why: without business.json the assistant has no facts and would
# invent prices, so we stop with a clear message and no traceback.
try:
    with open(BUSINESS_FILE, encoding="utf-8") as file:
        business = json.load(file)
except FileNotFoundError:
    print(f"{BUSINESS_FILE} was not found. Create it in the code folder and run again.")
    sys.exit()
except json.JSONDecodeError:
    print(f"{BUSINESS_FILE} is damaged. Please check its commas and quotes.")
    sys.exit()

PRICES = business["prices"]
orders = load_json(ORDERS_FILE, [])
transcript = load_json(TRANSCRIPT_FILE, [])

stats = {
    "questions": 0, "answered": 0, "errors": 0,
    "imports": 0, "orders_placed": 0,
}


# ---------- tools ----------

@tool(parse_docstring=True)
def get_price(item: str) -> str:
    """Get the price of one menu item.

    Args:
        item: The menu item name, for example brownie.
    """
    name = normalize_item(item, PRICES)
    if name not in PRICES:
        return f"{item} is not on our menu"
    return f"{name} costs {PRICES[name]} PKR"


@tool(parse_docstring=True)
def get_info(topic: str) -> str:
    """Get business information such as hours, delivery, phone, city or name.

    Args:
        topic: The information wanted: name, type, city, hours, phone or delivery.
    """
    key = topic.lower().strip()
    if key == "prices" or key not in business:
        return f"No information about {topic}"
    return f"{key}: {business[key]}"


@tool(parse_docstring=True)
def order_status(order_id: str) -> str:
    """Check the status of an order saved in orders.json.

    Args:
        order_id: The order number, for example A101.
    """
    for order in orders:
        if order["id"] == order_id.upper().strip():
            return (f"Order {order['id']} for {order['customer']} is "
                    f"{order['status']}, total {order['total']} PKR")
    return f"Order {order_id} was not found"


@tool(parse_docstring=True)
def place_order(item: str, quantity: int, customer: str) -> str:
    """Place a new order after the owner approves it.

    Args:
        item: The menu item to order.
        quantity: How many pieces the customer wants.
        customer: The customer's name.
    """
    name = normalize_item(item, PRICES)
    if name not in PRICES:
        return f"Cannot order: {item} is not on our menu"
    if quantity < 1:
        return "Cannot order: quantity must be at least 1"

    total = calculate_total(PRICES[name], quantity)

    # Why: an order commits the owner's time and money, so a human must
    # say yes first. The AI can never skip this input().
    answer = input(
        f"  [approve] {quantity} x {name} for {customer} = {total:,} PKR. "
        "Place it? (yes/no) "
    ).strip().lower()
    if answer != "yes":
        return "The owner said no. The order was NOT placed."

    order = {
        "id": make_order_id(orders),
        "customer": customer,
        "items": [{"item": name, "quantity": quantity,
                   "line_total": total}],
        "total": total,
        "status": "received",
    }
    orders.append(order)
    save_json(ORDERS_FILE, orders)
    stats["orders_placed"] += 1
    return f"Order {order['id']} placed: {quantity} x {name}, total {total} PKR"


# Why: the dictionary links the tool name the AI says to the real
# function we run. An unknown name is simply not found in it.
TOOLS = {
    "get_price": get_price,
    "get_info": get_info,
    "order_status": order_status,
    "place_order": place_order,
}
tool_counts = {name: 0 for name in TOOLS}


# ---------- models ----------

# Why: models are created once, at the top. temperature 0 gives
# steady tool choices and the same data for the same message.
agent = init_chat_model(MODEL, model_provider="ollama", temperature=0)
agent_with_tools = agent.bind_tools(list(TOOLS.values()))
extractor = init_chat_model(
    MODEL, model_provider="ollama", temperature=0, format=SCHEMA
)

SYSTEM_MESSAGE = {
    "role": "system",
    "content": (
        f"You are the assistant of {business['name']}, a {business['type']} "
        f"in {business['city']}. Use the tools for prices, business "
        "information, order status and placing orders. Never guess a "
        "price, opening hours or an order status: if a tool says it is "
        "not found, say so. Answer in at most 3 short sentences."
    ),
}


# ---------- the agent loop ----------

def ask_agent() -> str:
    """Run the agent loop on the current transcript and return the answer."""
    # Why: only the last MEMORY_SIZE transcript messages are sent, so
    # the cost does not grow. Tool messages stay in this local list
    # and never enter the saved transcript.
    work = [SYSTEM_MESSAGE] + transcript[-MEMORY_SIZE:]

    # Why: for ... else. The else part runs only if the loop used all
    # MAX_STEPS without a break, so the agent can never loop forever.
    for step in range(MAX_STEPS):
        ai_message = agent_with_tools.invoke(work)
        work.append(ai_message)

        if not ai_message.tool_calls:
            answer = ai_message.text
            break

        for call in ai_message.tool_calls:
            name = call["name"]
            args = call["args"]

            if name not in TOOLS:
                result = f"Error: there is no tool called {name}"
            else:
                tool_counts[name] += 1
                try:
                    result = TOOLS[name].invoke(args)
                except ValidationError:
                    result = f"Error: wrong arguments for {name}: {args}"

            print(f"  [tool] {name}({args}) -> {result}")
            # Why: tool_call_id tells the AI which request this result answers.
            work.append(ToolMessage(content=str(result), tool_call_id=call["id"]))
    else:
        answer = "Sorry, I could not finish that. Please ask again."

    return answer


# ---------- /import ----------

def import_order() -> None:
    """Turn a pasted WhatsApp message into a checked order and save it if approved."""
    text = input("Paste the WhatsApp message: ").strip()
    if text == "":
        print("  Nothing pasted.")
        return
    stats["imports"] += 1

    response = extractor.invoke([
        {"role": "system", "content": (
            "Extract the order from the customer message. Set is_order to "
            "false if it is not an order. Use singular lowercase item names. "
            "Use an empty string if the name or address is missing. "
            "Never invent a name.")},
        {"role": "user", "content": text},
    ])

    # Why: never trust the reply blindly. Broken JSON is reported, not a crash.
    try:
        data = json.loads(clean_json_text(response.text))
    except json.JSONDecodeError:
        print(f"  CHECK: the AI reply was not valid JSON: {response.text[:80]!r}")
        return

    if not data.get("is_order", False):
        print("  Not an order: needs a human reply.")
        return

    customer = str(data.get("customer", "")).strip()
    address = str(data.get("address", "")).strip()
    checks = []
    name_ok = True

    # Why: the AI can invent a name. A real name must appear in the message.
    if customer == "":
        checks.append("customer name is missing")
        name_ok = False
    elif customer.lower() not in text.lower():
        checks.append(f"customer '{customer}' is not in the message (invented?)")
        name_ok = False

    lines = []
    total = 0
    for entry in data.get("items", []):
        name = normalize_item(str(entry.get("name", "")), PRICES)
        quantity = entry.get("quantity", 1)
        if not isinstance(quantity, int) or quantity < 1:
            quantity = 1
        # Why: an item that is not on the menu is never priced.
        if name not in PRICES:
            checks.append(f"'{name}' is not on the menu")
            continue
        line_total = calculate_total(PRICES[name], quantity)
        total += line_total
        lines.append({"item": name, "quantity": quantity, "line_total": line_total})
        print(f"  {quantity} x {name} = {line_total:,} PKR")

    print(f"  Customer: {customer}, Address: {address}")
    print(f"  Total: {total:,} PKR")
    for check in checks:
        print(f"  CHECK: {check}")

    if not lines:
        print("  No menu items found, nothing to save.")
        return

    answer = input("  [approve] Save this order? (yes/no) ").strip().lower()
    if answer != "yes":
        print("  Not saved.")
        return

    orders.append({
        "id": make_order_id(orders),
        # Why: an invented or missing name is saved as "unknown", never as a fake name.
        "customer": customer if name_ok else "unknown",
        "address": address,
        "items": lines,
        "total": total,
        "status": "received",
    })
    save_json(ORDERS_FILE, orders)
    stats["orders_placed"] += 1
    print(f"  Saved as {orders[-1]['id']}.")


# ---------- main loop ----------

print("=" * 60)
print(f"   {business['name']} AI Business Assistant")
print("=" * 60)
print("Ask anything, or use: /import, /orders, /reset, bye")

while True:
    user_text = input("You: ").strip()
    command = user_text.lower()

    if command == "":
        continue

    if command == "bye":
        save_json(TRANSCRIPT_FILE, transcript)
        save_json(ORDERS_FILE, orders)
        print("Assistant: Goodbye! Everything is saved.")
        break

    if command == "/reset":
        # Only the chat is cleared. The orders stay.
        transcript.clear()
        save_json(TRANSCRIPT_FILE, transcript)
        print("Assistant: Chat cleared. Your orders are still saved.")
        continue

    if command == "/orders":
        if not orders:
            print("  No orders yet.")
        for number, order in enumerate(orders, start=1):
            print(f"  {number}. {order['id']} | {order['customer']} | "
                  f"{order['total']:,} PKR | {order['status']}")
        continue

    if command == "/import":
        try:
            import_order()
        except (httpx.ConnectError, ConnectionError, ollama.ResponseError) as error:
            log_error(error)
            stats["errors"] += 1
            print(f"Assistant: {friendly_message(error)}")
        continue

    stats["questions"] += 1
    transcript.append({"role": "user", "content": user_text})

    try:
        answer = ask_agent()
    except (httpx.ConnectError, ConnectionError, ollama.ResponseError) as error:
        # Why: the unanswered question is removed, so the saved chat
        # never has a question without an answer.
        transcript.pop()
        log_error(error)
        stats["errors"] += 1
        print(f"Assistant: {friendly_message(error)}")
        continue

    transcript.append({"role": "assistant", "content": answer})
    save_json(TRANSCRIPT_FILE, transcript)
    stats["answered"] += 1
    print(f"Assistant: {answer}")

print("=" * 60)
print("Session report")
print(f"Questions: {stats['questions']} | Answered: {stats['answered']} | "
      f"Errors: {stats['errors']}")
print(f"WhatsApp imports: {stats['imports']} | Orders placed: "
      f"{stats['orders_placed']} | Orders on file: {len(orders)}")
print("Tool calls:")
for tool_name, count in tool_counts.items():
    print(f"  {tool_name}: {count}")
print("=" * 60)
