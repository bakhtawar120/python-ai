"""Task 2.5: AI Skills Toolkit for Sweet Crumbs Bakery.

A toolkit of reusable AI skills (summarize, translate, reply to a
review) built on one ask_ai() function. A menu loop runs the skills
and a usage dictionary counts how often each one is used.
"""

from langchain.chat_models import init_chat_model

# Why: both models are created once, at the top. Creating a model
# inside a function would repeat the slow setup on every call.
# Precise (low temperature) is for facts, creative is for writing.
precise = init_chat_model(
    "gemma4:31b-cloud", model_provider="ollama", temperature=0.2
)
creative = init_chat_model(
    "gemma4:31b-cloud", model_provider="ollama", temperature=0.8
)


def ask_ai(prompt: str, system: str = "You are a helpful assistant.",
           creative_mode: bool = False) -> str:
    """Send a prompt to the AI and return the answer text."""
    # Why: one function picks the model, so every skill uses the same
    # tested code and we never copy-paste the AI call.
    model = creative if creative_mode else precise
    response = model.invoke([
        {"role": "system", "content": system},
        {"role": "user", "content": prompt},
    ])
    return response.text


def summarize(text: str) -> str:
    """Summarize a text in 2 short sentences."""
    return ask_ai(
        text,
        system="You summarize text in exactly 2 short sentences.",
    )


def translate(text: str, language: str = "Urdu") -> str:
    """Translate a text into the given language (default: Urdu)."""
    return ask_ai(
        text,
        system=f"Translate the text into {language}. Reply with the translation only.",
    )


def reply_to_review(review: str) -> str:
    """Write a polite reply to a customer review."""
    # Why: creative_mode=True because a reply should sound warm and
    # human, not robotic.
    return ask_ai(
        review,
        system=(
            "You are the owner of Sweet Crumbs Bakery in Lahore. "
            "Write a polite reply to this customer review in 2 short sentences."
        ),
        creative_mode=True,
    )


def estimate_tokens(text: str) -> int:
    """Estimate tokens: about 1 token for every 4 characters."""
    return len(text) // 4


# Why: assert tests check a function that needs no AI. If a test
# fails, Python stops and tells us the function is broken.
assert estimate_tokens("") == 0
assert estimate_tokens("abcd") == 1
assert estimate_tokens("a" * 40) == 10

# Why: the dictionary starts with every skill at 0, so we can add 1
# each time a skill is used and print the report at the end.
usage = {"summarize": 0, "translate": 0, "reply": 0}

print("Sweet Crumbs AI Toolkit. Commands: /summarize, /translate, /reply, /batch, bye")

while True:
    command = input("Command: ").strip().lower()

    if command == "bye":
        break

    elif command == "/summarize":
        text = input("Text to summarize: ").strip()
        print(f"AI: {summarize(text)}")
        usage["summarize"] += 1

    elif command == "/translate":
        text = input("Text to translate: ").strip()
        language = input("Language (Enter for Urdu): ").strip()
        if language == "":
            # Enter pressed: call without language so the default is used
            print(f"AI: {translate(text)}")
        else:
            print(f"AI: {translate(text, language)}")
        usage["translate"] += 1

    elif command == "/reply":
        review = input("Customer review: ").strip()
        print(f"AI: {reply_to_review(review)}")
        print(f"    (review was about {estimate_tokens(review)} tokens)")
        usage["reply"] += 1

    elif command == "/batch":
        # Stretch: one skill over a list of 3 reviews
        reviews = [
            "Cake was great but delivery was late.",
            "Best brownies in Lahore, will order again!",
            "The cupcake was dry and the price is too high.",
        ]
        for number, review in enumerate(reviews, start=1):
            print(f"{number}. Review: {review}")
            print(f"   Reply: {reply_to_review(review)}")
            usage["reply"] += 1

    else:
        print("Unknown command. Try /summarize, /translate, /reply, /batch or bye.")

print("Skills used today:")
for skill, count in usage.items():
    print(f"  {skill}: {count}")