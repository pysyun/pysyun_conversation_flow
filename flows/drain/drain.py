import os
import asyncio
import threading
import time

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


bot = DrainBot(os.getenv('TELEGRAM_BOT_TOKEN'))


def run_timer_thread():
    while True:
        asyncio.run(bot.process({
            "text": "Hello, Drain!",
            "update": {
                "message": {
                    "from_user": {
                        "id": 0
                    }
                }
            }
        }))
        time.sleep(1)  # Sleep for 1 second to reduce CPU load


if __name__ == "__main__":
    main_thread = threading.Thread(target=run_timer_thread)
    main_thread.start()

    bot.run()
