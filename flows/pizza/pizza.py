import os
import re

from dotenv import load_dotenv

from pysyun.conversation.flow.persistent_telegram_bot import PersistentTelegramBot

load_dotenv()


class PizzaBot(PersistentTelegramBot):

    def build_state_machine(self, builder):
        main_menu_transition = self.build_menu_response_transition(
            "Welcome to PizzaBot! How can I help you today?",
            [["Order Pizza", "View Cart"], ["Cancel Order"]])

        order_pizza_transition = self.build_menu_response_transition(
            "What kind of pizza would you like?",
            [["Pepperoni", "Cheese"], ["Veggie", "Meat Lovers"], ["Custom Pizza", "Back"]])

        custom_pizza_transition = self.build_message_response_transition(
            "Please type out your custom pizza order.")

        add_to_cart_transition = self.build_menu_response_transition(
            "Got it! Adding that pizza to your cart.",
            [["Back"]])

        view_cart_transition = self.build_menu_response_transition(
            "Here's what's in your cart so far: ...",
            [["Back"]])

        cancel_order_transition = self.build_menu_response_transition(
            "Your order has been cancelled. Have a nice day!",
            [["Back"]])

        return builder \
            .edge("/start", "/start", "/start", on_transition=main_menu_transition) \
            .edge(
                "/start",
                "/start",
                "/graph",
                on_transition=self.build_graphviz_response_transition()) \
            .edge("/start", "/order", "Order Pizza", on_transition=order_pizza_transition) \
            .edge("/start", "/view_cart", "View Cart", on_transition=view_cart_transition) \
            .edge("/start", "/cancel_order", "Cancel Order", on_transition=cancel_order_transition) \
 \
            .edge("/order", "/custom_pizza", "Custom Pizza", on_transition=custom_pizza_transition) \
            .edge("/order", "/start", "Back", on_transition=main_menu_transition) \
            .edge("/order", "/add_to_cart", None, matcher=re.compile(".*"), on_transition=add_to_cart_transition) \
 \
            .edge("/custom_pizza", "/add_to_cart", None, matcher=re.compile(".*"),
                  on_transition=add_to_cart_transition) \
            .edge("/custom_pizza", "/order", "Back", on_transition=order_pizza_transition) \
 \
            .edge("/add_to_cart", "/order", "Back", on_transition=order_pizza_transition) \
 \
            .edge("/view_cart", "/start", "Back", on_transition=main_menu_transition) \
 \
            .edge("/cancel_order", "/start", "Back", on_transition=main_menu_transition)

    def build_menu_response_transition(self, title, menu_items):
        menu = self.build_menu(menu_items)

        async def transition(action):
            chat_id = action["update"]["effective_chat"]["id"]
            await action["context"].bot.send_message(chat_id=chat_id,
                                                     text=title,
                                                     reply_markup=menu)

        return transition

    @staticmethod
    def build_message_response_transition(message):
        async def transition(action):
            chat_id = action["update"]["effective_chat"]["id"]
            await action["context"].bot.send_message(chat_id=chat_id,
                                                     text=message)

        return transition

    def build_menu(self, menu_items):
        buttons = [[self.build_button(item) for item in row] for row in menu_items]
        return {"keyboard": buttons, "resize_keyboard": True}

    @staticmethod
    def build_button(label):
        return {"text": label}


PizzaBot(os.getenv('TELEGRAM_BOT_TOKEN')).run()
