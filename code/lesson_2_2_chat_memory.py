"""Task 2.2: Personal Tutor with Memory.

A chat loop where the tutor remembers the conversation. The memory is
a list of messages. Commands: /reset clears memory, /count shows the
number of messages, bye exits. Only the system message plus the last
8 messages are kept so the cost does not grow forever.
Stretch: a separate questions list is summarised when the user says bye.
"""

from langchain.chat_models import init_chat_model

# Why: the model is created once, outside the loop, because creating
# it again for every message would be slow and wasteful.
llm = init_chat_model(
    "gemma4:31b-cloud",
    model_provider="ollama",
    temperature=0.2,
)

# Why: the system message sets the tutor's role and answer length. It
# is stored in its own variable so /reset can bring it back easily.
system_message = {
    "role": "system",
    "content": (
        "You are a friendly tutor. "
        "Answer in at most 3 short sentences."
    ),
}

# Why: messages[0] is always the system message, so the AI never loses
# its role, even after /reset or trimming.
messages = [system_message]

# NEW (stretch)
# Why: a separate list keeps only the user's questions, so we can
# summarise the session at the end. Commands are not counted.
questions = []

print("Tutor: Ask me anything. Commands: /reset, /count, bye")

while True:
    user_text = input("You: ").strip()

    # Why: skip empty input so we do not waste an AI call on nothing.
    if user_text == "":
        continue

    # NEW (stretch): print the summary before leaving
    if user_text.lower() == "bye":
        # Why: we check the list is not empty, otherwise questions[0]
        # would crash when nothing was asked.
        if len(questions) > 0:
            print(f"Tutor: You asked {len(questions)} questions.")
            print(f"       First: {questions[0]}")
            print(f"       Last: {questions[-1]}")
        print("Tutor: Goodbye!")
        break

    if user_text.lower() == "/reset":
        # Why: we keep the system message and delete everything else,
        # so the tutor forgets the chat but keeps its role.
        messages = [system_message]
        print("Tutor: Memory cleared.")
        continue

    if user_text.lower() == "/count":
        print(f"Tutor: {len(messages)} messages in memory.")
        continue

    # NEW (stretch): save the question before asking the AI
    questions.append(user_text)

    # Normal message: add the user message, ask the AI, add the reply.
    messages.append({"role": "user", "content": user_text})
    response = llm.invoke(messages)
    messages.append({"role": "assistant", "content": response.text})

    # Why: trimming keeps the system message plus only the last 8
    # messages, so the tokens (and cost) stop growing.
    messages = [messages[0]] + messages[1:][-8:]

    print(f"Tutor: {response.text}")
    print(f"       (tokens sent: {response.usage_metadata['input_tokens']})")