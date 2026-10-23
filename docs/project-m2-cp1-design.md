# Design: AI Content Studio (Sweet Crumbs Bakery)

## Facts
| Key | Value |
|---|---|
| name | Sweet Crumbs |
| city | Lahore |
| hours | 9 am to 10 pm, every day |
| phone | 0300-1234567 |
| delivery | 200 PKR, free for orders from 3,000 PKR |
| prices | chocolate cake 1,500 PKR, cupcake 250 PKR, brownie 300 PKR, donut 200 PKR, mango tart 0 (coming soon) |

## Tones
| Tone | Description sent to the AI |
|---|---|
| fun | playful and full of energy, short sentences |
| premium | elegant and calm, focused on quality |
| urgent | exciting, tells customers to order today |

## Which model for which job
| Job | Model and temperature | Why |
|---|---|---|
| Menu descriptions | creative, 0.8 | Marketing text should be varied |
| Social media posts | creative, 0.8 | Posts should feel fresh and different each time |
| Chat with customers | precise, 0.2 | Answers must be accurate and match the facts |
| /price | no AI | The dictionary is exact, free and instant |

## Feature tests
| You type | Expected | Pass? |
|---|---|---|
| /menu | Price-0 item skipped, numbered menu, prices with commas | |
| /post fun, /post premium, /post urgent | Post streams word by word, different style each time | |
| /post pirate | Default tone used, no KeyError | |
| /price CUPCAKE | Correct price | |
| /price mango tart | Coming soon | |
| /price pizza | Not on our menu, no crash | |
| My name is Ali, then What is my name? | Remembers the name | |
| /reset, then What is my name? | Does not know | |
| Press Enter with no text | Asks again | |
| BYE | Goodbye + session report | |