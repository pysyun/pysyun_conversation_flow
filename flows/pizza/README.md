# Pizza Bot User Manual

## Overview

The Pizza Bot is a conversational Telegram or CLI bot that allows users to place pizza orders and manage their cart. It showcases common patterns like state machines and persistence.

Key features:

- Place new pizza orders
- Build custom pizza orders  
- View and update shopping cart
- Persists user state across sessions
- State machine architecture 

## Getting Started 

### Setup

To run the bot yourself:

1. `git clone https://github.com/pysyun/pysyun_conversation_flow`
2. `pip install -r requirements.txt`  
3. Set `TELEGRAM_BOT_TOKEN` in `.env`
4. `python flows/pizza/pizza.py`

## Ordering Pizzas 

Start new order:

1. Type `/start` or tap **Order Pizza** button
2. Select desired pizza or tap **Custom Pizza** 
3. Review order and tap **Add to Cart**

View current order:
 
1. Tap **View Cart** to see items
2. Tap **Back** when done  

## Custom Orders

Build a custom pizza order:

1. Tap **Custom Pizza** from main menu 
2. Type pizza specifications (size, toppings, etc)
3. Tap **Add to Cart** to save order

Go back and retry:

- Tap **Back** to redo custom order 
  
## Persistence

Cart contents and order state is saved for each user across sessions.

To clear saved state:

- Tap **Cancel Order**  
- Tap **Back to Start**

This resets state so you can start fresh.

## Architecture 

The Pizza Bot uses a state machine architecture for managing order flows. States represent different screens like `/start`, `/order`, `/custom_pizza` etc.

Transitions between states occur based on user button taps or text replies. This maps well to conversational UIs.

For more on state machines, see the [documentation](../../documentation/state-machines.md).

The full state machine is visualized here:

![Pizza Bot State Machine](./pizza.png)

Simplified version:

```
/start 
   |- (Order Pizza) -> /order
       |- (Custom Pizza) -> /custom_pizza
           |- (Add to Cart) -> /add_to_cart 
               |- (Back) -> /order
   |- (View Cart) -> /view_cart
   |- (Cancel Order) -> /cancel_order   
```

That covers the key concepts and usage of the Pizza Bot demo. Checkout the code in [pizza.py](./pizza.py) for implementation details.
