# Module 1 Checkpoint 2: Project Design

## Project name
**Sweet Crumbs Front Desk Assistant**

A rule-based bakery assistant that answers common questions, calculates item quotes, and prepares cost-estimated AI prompts for questions the rules cannot answer.

## Table 1: Intents

| Intent | Keywords | Reply |
|---|---|---|
| Complaint | refund, complaint, late | Sorry about that. A manager will call you within 1 hour. |
| Greeting | hi, hello, salam | Welcome to Sweet Crumbs! How can I help you? |
| Hours | hours, open, timing | We are open 9 AM to 10 PM every day. |
| Location | location, where are you | Please contact our staff for the bakery location. |
| Delivery | delivery, deliver, shipping | Delivery costs 200 PKR. It is free for orders of 3,000 PKR or more after discount. |
| Contact | contact | Please contact our staff for assistance. |
| Goodbye | bye | Goodbye, and thank you for contacting Sweet Crumbs. |
| Human handover | agent, human | Connecting you to a human... |

## Table 2: Business rules

| Rule | Value |
|---|---|
| Business | Sweet Crumbs bakery |
| Bot name | Sweet Crumbs Desk |
| Cupcake | 250 PKR each |
| Brownie | 300 PKR each |
| Chocolate cake | 1,500 PKR each |
| Bulk discount | 10% off for 10 or more items |
| Delivery fee | 200 PKR |
| Free delivery limit | 3,000 PKR after discount |
| Private words | phone, CNIC, address |
| Local model | llama3.2 through Ollama |
| Cloud model | Small cloud model (cheap) |
| Example cloud price | 0.10 PKR per 1,000 tokens (illustrative only; replace with your provider's actual price if required) |
| Token estimate | Rounded characters / 4 |
| Question limit | First 150 characters |

## Table 3: Rule test results

Run every test and change Pass? only after checking the actual result.

| You type | Expected | Pass? |
|---|---|---|
| ` WHAT are your hours ` | Hours reply; spaces and capitals handled | Pending run |
| `which cake is best?` | AI fallback, not greeting | Pending run |
| `my order is late` | Complaint / manager reply | Pending run |
| `/quote`, quantity 1 chocolate cake | 200 PKR delivery fee | Pending run |
| `/quote`, quantity 3 chocolate cakes | Free delivery (discounted subtotal is 4,500 PKR) | Pending run |
| `/quote`, quantity 10 cupcakes | 10% discount | Pending run |
| `/quote`, item pizza | Not on our menu; no crash | Pending run |
| `Can I change my phone number?` | Local model; cost 0 | Pending run |
| Press Enter with no text | Asks for a message again | Pending run |
| `BYE` | Goodbye and session report | Pending run |
| Quantity `abc` | Friendly quantity error; no crash | Pending run |
| `human` | Handover message, report, complaint count | Pending run |

## Rule order explanation

1. Complaint rule first so complaints get priority.
2. Human handover and goodbye stop the chat.
3. `/quote` runs the price calculator.
4. Greeting uses exact matches or `.startswith()` to avoid the greeting trap: `hi` should not match inside `which`.
5. Other FAQ rules answer known questions.
6. The fallback handles questions with no matching rule.
7. The report prints after the loop ends.

## Pricing example

12 cupcakes cost 3,000 PKR. A 10% discount is 300 PKR, so the discounted subtotal is 2,700 PKR. This is below the 3,000 PKR free-delivery limit, so delivery is 200 PKR. Final total: **2,900 PKR**.

## AI routing

Questions containing `phone`, `cnic`, or `address` are assigned to the local model at a zero estimated cloud cost. Other unknown questions are assigned to the example cloud model. The price per 1,000 tokens is an illustrative value, not a verified current provider price.

## Testing note

Do not mark a test as passed until you run it and compare the output with the expected result.