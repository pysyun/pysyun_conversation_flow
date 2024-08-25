from telegram import Update, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, MessageHandler, filters, ContextTypes, CallbackQueryHandler

from pysyun.conversation.flow.dialog_state_machine import DialogStateMachineBuilder


class TelegramBot:

    def __init__(self, token, initial_state="/start", scheduler=None):
        self.application = Application.builder().token(token).build()
        self.state_machine = self.build_state_machine(DialogStateMachineBuilder(initial_state=initial_state)).build()

        if scheduler:
            self.scheduler = scheduler
            scheduler.start(self.application, self.state_machine)

    def build_state_machine(self, builder):
        return builder

    @staticmethod
    def build_message_response_transition(message):
        async def transition(action):
            await action["context"].bot.send_message(chat_id=action["update"]["effective_chat"]["id"], text=message)

        return transition

    @staticmethod
    def build_menu_response_transition(title, menu_items):
        async def transition(action):
            menu = ReplyKeyboardMarkup(menu_items, resize_keyboard=True, one_time_keyboard=True)
            await action["context"]["bot"].send_message(chat_id=action["update"].effective_chat.id,
                                                        text=title,
                                                        reply_markup=menu)

        return transition

    @staticmethod
    def build_inline_keyboard(keyboard_data):
        keyboard = []
        for row in keyboard_data:
            keyboard_row = []

            for button in row:
                text = button[0]
                callback_data = button[1]

                if callback_data is None:
                    url = button[2]
                    keyboard_row.append(InlineKeyboardButton(text, url=url))
                    continue

                keyboard_row.append(InlineKeyboardButton(text, callback_data=callback_data))

            keyboard.append(keyboard_row)

        return InlineKeyboardMarkup(keyboard)

    def build_graphviz_response_transition(self):
        async def transition(action):
            await action["context"].bot.send_message(chat_id=action["update"].effective_chat.id,
                                                     text=self.state_machine.to_graphviz())

        return transition

    def run(self):
        async def on_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
            await self.state_machine.process({
                "update": update,
                "context": context,
                "text": update.message.text
            })

            # TODO: Do we need to remove this log entry?
            print("Processing message", update.message.text)

            # Update the list of chats to record last activity in the chat
            if "chats" not in context.user_data:
                context.user_data["chats"] = {}
            if update.effective_chat.id not in context.user_data["chats"]:
                context.user_data["chats"][update.effective_chat.id] = {}
            context.user_data["chats"][update.effective_chat.id]["date_modified"] = update.message.date.timestamp()

        async def on_callback_query(update: Update, context: ContextTypes.DEFAULT_TYPE):
            query = update.callback_query
            await self.state_machine.process({
                "update": update,
                "context": context,
                "text": query.data
            })

            print("Processing callback query", query.data)

            # Update the list of chats to record last activity in the chat
            if "chats" not in context.user_data:
                context.user_data["chats"] = {}
            if update.effective_chat.id not in context.user_data["chats"]:
                context.user_data["chats"][update.effective_chat.id] = {}
            context.user_data["chats"][update.effective_chat.id]["date_modified"] = (update.effective_message.date.
                                                                                     timestamp())

            await query.answer()

        self.application.add_handler(
            MessageHandler(filters.TEXT | filters.COMMAND | filters.SenderChat.ALL, on_command))
        self.application.add_handler(CallbackQueryHandler(on_callback_query))

        self.application.run_polling()
