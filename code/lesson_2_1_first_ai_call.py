"""Task 2.1: AI Tutor.

Asks the user for a topic and a level (beginner or expert), sends them
to an Ollama model, and prints the answer together with the total
tokens used and the time taken in seconds.
"""

from langchain.chat_models import init_chat_model

# Why: users often type extra spaces by mistake, and .strip() removes
# them so the AI receives clean text.
topic = input("Topic:   ").strip()
level = input("Level (beginner or expert): ").strip()

# Why: the system message sets the AI's role and the answer length.
# A short length limit keeps answers focused and uses fewer tokens,
# which means lower cost for the tuition centre.
system_message = (
    "You are a friendly tutor. "
    f"Explain the topic for a {level} student. "
    "Answer in at most 3 short sentences."
)

# Why: temperature 0.2 makes answers more focused and less random,
# which is better for teaching.
llm = init_chat_model(
    "gemma4:31b-cloud",
    model_provider="ollama",
    temperature=0.2,
)

messages = [
    {"role": "system", "content": system_message},
    {"role": "user", "content": topic},
]

response = llm.invoke(messages)

tokens = response.usage_metadata["total_tokens"]
# Why: Ollama gives the duration in nanoseconds, so we divide by
# 1 billion to get seconds.
seconds = response.response_metadata["total_duration"] / 1_000_000_000

print("=" * 40)
print(response.text)
print("=" * 40)
print(f"{tokens} tokens in {seconds:.1f} seconds")
