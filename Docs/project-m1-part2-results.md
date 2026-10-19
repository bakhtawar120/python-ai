# AI Test Results (Ollama, llama3.2)

## Test 1: Cloud-routed question

**Prompt:** You are the assistant of Sweet Crumbs bakery. Answer Bakhtawar Khan in 2 short lines. Question: Do you make sugar-free cakes?

*Answer : Yes, we do! We offer a variety of sugar-free options and can also customize a cake to meet your specific dietary needs. 🍰✨*

**Useful?** No. The tone is friendly, but the AI promised "a variety of sugar-free options" and custom cakes. The bot never gave it the real menu, so this is a hallucination. A customer could trust a promise the bakery cannot keep.


## Test 2: Local-routed question (private)
**Prompt:** You are the assistant of Sweet Crumbs bakery. Answer Bakhtawar khan in 2 short lines. Question: Can i change my phone number on the order?
*Answer Yes, you certainly can!*
Please provide your **order number** and the **new phone number** here, or give us a quick call, and we'll update it for you 
right away🍰
**Useful?** Partly. The reply is polite and the next step (order number and new number) makes sense. But the AI said "yes, you can" without knowing the bakery's policy, and it asked for personal data in chat. It needs the real policy in the prompt before using it with customers.


## Lesson learned
The AI sounds confident even when it does not know the bakery's facts. In Module 2, I will add real menu, hours and policies to the prompt so the AI does not invent promises.