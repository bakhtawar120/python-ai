# Design: Sweet Crumbs Front Desk

## Intents

| Intent | Keywords | Reply |
|---|---|---|
| Complaint | refund, complaint, late | Sorry about that. A manager will call you within 1 hour. |
| Human handover | agent, human | Connecting you to a human... |
| Greeting | hi, hello (checked with == / startswith) | Hello! How can I help? |
| Hours | hour, open, timing | We are open 9 am to 10 pm, every day. |
| Location | where, location | We are on Main Boulevard, Lahore. |
| Delivery | deliver | We deliver across the city. Fee 200 PKR, free from 3,000 PKR. |
| Price | price, cost, how much | Type /quote to get an exact price. |

## Business rules

| Rule | Value |
|---|---|
| Item prices | cupcake 250, brownie 300, chocolate cake 1,500 PKR |
| Bulk discount | 10% off for 10 or more items |
| Delivery | 200 PKR, free from 3,000 PKR (checked after the discount) |
| Private words | phone, cnic, my address (routed to the local model, cost 0) |
| Example cloud price | 0.1 PKR per 1K tokens (example, not a real price) |

## Rule Tests

| You type | Expected | Pass? |
|---|---|---|
| `  WHAT are your HOURS  ` | Hours reply (capitals and spaces handled) | Yes |
| `which cake is best?` | Fallback, not a greeting | Yes |
| `my order is late` | Manager reply (complaint first) | Yes |
| `/quote` chocolate cake x1 | Delivery 200 charged, total 1,700 | Yes |
| `/quote` chocolate cake x3 | Delivery free, total 4,500 | Yes |
| `/quote` cupcake x12 | Discount 300, delivery 200, total 2,900 | Yes |
| `/quote` pizza x2 | "Not on our menu", no crash | Yes |
| `can I change my phone number?` | Routed to local model, cost 0 | Yes |
| Enter with no text | Asks again | Yes |
| `/quote` cupcake x `abc` | Polite message, no crash | Yes |
| `BYE` | Goodbye + session report | Yes |

**Note:** In my first run, `/quote` did not work because I typed the item and quantity on the same line as `/quote`. The bot treated it as a normal question. In the second run I typed `/quote`, the item and the quantity on separate lines, and it worked. A final test session gave `Quotes: 3 | Quoted value: 9,100 PKR`, which matches 1,700 + 4,500 + 2,900.