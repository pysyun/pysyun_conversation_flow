import os

from dotenv import load_dotenv

from pysyun.conversation.flow.drain_telegram_bot import DrainTelegramBot

load_dotenv()


class DrainBot(DrainTelegramBot):

    def build_state_machine(self, builder):
        main_menu_transition = self.build_menu_response_transition(
            "Welcome to Alerts Drain Bot!",
            [["Subscribe", "Unsubscribe"], ["About"]])

        return builder \
            .edge("/start", "/start", "/start", on_transition=main_menu_transition)


DrainBot(os.getenv('TELEGRAM_BOT_TOKEN')).run()
