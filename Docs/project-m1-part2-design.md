# Design: Sweet Crumbs Front Desk

## Intents
| Intent | Keywords | Reply |
|---|---|---|
| Complaint | refund, complaint, late | Sorry about that. A manager will call you within 1 hour. |
| Greeting | hi, hello (exact / startswith) | Hello! How can I help? |
| Hours | hour, open, timing | We are open 9 am to 10 pm, every day. |
| Location | where, location | We are on Main Boulevard, Lahore. |
| Delivery | deliver | We deliver across the city. Fee 200 PKR, free from 3,000 PKR. |
| Price | price, cost, how much | Type /quote to get an exact price. |

## Business rules
| Rule | Value |
|---|---|
| Item prices | cupcake 250, brownie 300, chocolate cake 1,500 PKR |
| Bulk discount | 10% off for 10 or more |
| Delivery | 200 PKR, free from 3,000 PKR (checked after discount) |
| Private words | phone, cnic, my address |
