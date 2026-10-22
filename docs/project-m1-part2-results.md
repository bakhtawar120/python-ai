# AI Test Results — Module 1 Checkpoint 2

**Important:** These are prepared test prompts, not claimed Ollama outputs. Run each prompt with Ollama and replace the answer section with the actual answer your model returns.

## Test 1: General bakery question

**Prompt printed by the bot**

You are the assistant of Sweet Crumbs bakery.
Answer Ali Raza in 2 short lines. Question: Do you make sugar-free cakes?

**Ollama model:** `llama3.2` (or the model you actually used)

**AI's actual answer:**
_Paste the answer from Ollama here._

**Judgement:** Pending actual run. Check whether the model avoids inventing menu items, prices, or promises. If it says sugar-free cakes are available without evidence, mark it as not reliable.

## Test 2: Private order detail

**Prompt printed by the bot**

You are the assistant of Sweet Crumbs bakery.
Answer Ali Raza in 2 short lines. Question: Can i change my phone number on the order?

**Ollama model:** `llama3.2` (local)

**AI's actual answer:**
_Paste the answer from Ollama here._

**Judgement:** Pending actual run. Check whether the answer recommends contacting staff instead of claiming it has changed the customer's order. A model response alone does not actually update an order.

## How to run the tests

1. Run the front desk script and copy the two prompts it prints.
2. Open a terminal and run `ollama run llama3.2`.
3. Paste each prompt and wait for the model's answer.
4. Replace the placeholders above with the actual answers.
5. Write one honest line for each answer explaining whether it is useful and whether it invents facts.