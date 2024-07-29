## Using the `AbandonedChatScheduler` in Bot Projects

### Overview

The `AbandonedChatScheduler` class is a utility that allows developers to schedule tasks for handling users who have abandoned their chat sessions. This helps in maintaining user engagement, providing timely prompts, and ensuring that users don't lose track of their conversation flow due to inactivity.

### Why Use the `AbandonedChatScheduler`?

In conversational bots, it’s common for users to leave a session midway and return later. However, if the user doesn’t return for an extended period, they might need a reminder or some form of re-engagement. The `AbandonedChatScheduler` helps by:

1. Sending reminders to users who have been inactive for a specified duration.
2. Maintaining user engagement and improving the user experience.
3. Managing long-duration conversations by providing timely notifications or actions.
4. Automatically triggering state transitions based on inactivity.

### Key Features

- **Task Scheduling:** Schedule tasks to be executed at specific intervals.
- **Flexible Triggers:** Define triggers based on time intervals (e.g., every minute, hour, day).
- **Persistent State:** Works seamlessly with persistent bots to ensure that state is maintained across sessions.
- **Easy Integration:** Can be easily integrated into existing state machine-based bot architectures.

### How to Use the `AbandonedChatScheduler`

1. **Integrate the Scheduler:**

   Import the class and define the scheduled tasks. Each task can define a message to be sent and a time span in seconds after which it should be triggered if the user is inactive.

   ```python
   from pysyun.conversation.workers.abandoned_chat_scheduler import AbandonedChatScheduler, ScheduledTask
   ```

2. **Define Scheduled Tasks:**

   Create a list of `ScheduledTask` instances. Each task specifies a message and the duration (in seconds) of inactivity after which that message should be sent.

   ```python
   tasks = [
       ScheduledTask(message='/start', span=1800),  # Send a start message if the user is inactive for 30 minutes
   ]
   ```

3. **Initialize and Start the Scheduler:**

   Pass the tasks to the `AbandonedChatScheduler` and start it with the bot's application and state machine.

   ```python
   scheduler = AbandonedChatScheduler(tasks, minute='*/1')  # Run the check every minute
   bot = PersistentTelegramBot(token='YOUR_TELEGRAM_BOT_TOKEN', scheduler=scheduler)
   bot.run()
   ```

### Example

The following example demonstrates how to set up the `AbandonedChatScheduler` in a pizza ordering bot to re-engage users who have been inactive for 30 minutes.

```python
import os
from dotenv import load_dotenv
from pysyun.conversation.flow.persistent_telegram_bot import PersistentTelegramBot
from pysyun.conversation.workers.abandoned_chat_scheduler import AbandonedChatScheduler, ScheduledTask

load_dotenv()


class PizzaBot(PersistentTelegramBot):

    def build_state_machine(self, builder):
        main_menu_transition = self.build_menu_response_transition(
            "Welcome to PizzaBot! How can I help you today?",
            [["Order Pizza", "View Cart"], ["Cancel Order"]])

        order_pizza_transition = self.build_menu_response_transition(
            "What kind of pizza would you like?",
            [["Pepperoni", "Cheese"], ["Veggie", "Meat Lovers"], ["Custom Pizza"]])

        custom_pizza_transition = self.build_message_response_transition(
            "Please type out your custom pizza order.")

        add_to_cart_transition = self.build_message_response_transition(
            "Got it! Adding that pizza to your cart.")

        view_cart_transition = self.build_message_response_transition(
            "Here's what's in your cart so far: ...")

        cancel_order_transition = self.build_message_response_transition(
            "Your order has been cancelled. Have a nice day!")

        return builder
            .edge("/start", "/start", "/start", on_transition=main_menu_transition)
            .edge(
            "/start",
            "/start",
            "/graph",
            on_transition=self.build_graphviz_response_transition())
            .edge("/start", "/order", "Order Pizza", on_transition=order_pizza_transition)
            .edge("/order", "/custom_pizza", "Custom Pizza", on_transition=custom_pizza_transition)
            .edge("/custom_pizza", "/add_to_cart", "Add to Cart", on_transition=add_to_cart_transition)
            .edge("/order", "/add_to_cart", ".*", on_transition=add_to_cart_transition)
            .edge("/start", "/view_cart", "View Cart", on_transition=view_cart_transition)
            .edge("/start", "/cancel_order", "Cancel Order", on_transition=cancel_order_transition)
            .edge("/custom_pizza", "/order", "Back", on_transition=order_pizza_transition)
            .edge("/add_to_cart", "/order", "Back", on_transition=order_pizza_transition)
            .edge("/view_cart", "/start", "Back", on_transition=main_menu_transition)
            .edge("/cancel_order", "/start", "Back to Start", on_transition=main_menu_transition)

    def build_menu_response_transition(self, title, menu_items):
        menu = self.build_menu(menu_items)

        async def transition(action):
            await action["context"].bot.send_message(chat_id=action["update"]["effective_chat"]["id"],
                                                     text=title,
                                                     reply_markup=menu)

        return transition

    @staticmethod
    def build_message_response_transition(message):
        async def transition(action):
            await action["context"].bot.send_message(chat_id=action["update"]["effective_chat"]["id"],
                                                     text=message)

        return transition

    def build_menu(self, menu_items):
        buttons = [[self.build_button(item) for item in row] for row in menu_items]
        return {"keyboard": buttons, "resize_keyboard": True}

    @staticmethod
    def build_button(label):
        return {"text": label}


tasks = [
    ScheduledTask('/start', 1800)  # Send /start if user is inactive for 30 minutes
]
scheduler = AbandonedChatScheduler(tasks, minute='*/1')  # Check every minute
PizzaBot(os.getenv('TELEGRAM_BOT_TOKEN'), scheduler=scheduler).run()
```

### Conclusion

By incorporating the `AbandonedChatScheduler` into your bot projects, you can improve user engagement and ensure that conversations don't get lost due to inactivity. This powerful utility provides a structured way to manage and re-engage users in a conversational bot environment.

