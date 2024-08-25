from pysyun.conversation.flow.telegram_bot import TelegramBot


class SimpleInlineButtonBot(TelegramBot):
    def build_state_machine(self, builder):
        return builder \
            .edge("/start", "/start", "/start", on_transition=self.start_transition()) \
            .edge("/start", "/start", "/abandoned", on_transition=self.start_transition())

    def start_transition(self):
        async def transition(action):
            markup = self.build_inline_keyboard(
                [
                    [
                        ["First button", "/start"],
                        ["Second button", "/abandoned"]
                    ],
                    [
                        ["URL", None, "https://example.org"]
                    ]
                ]
            )
            await action["context"].bot.send_message(
                chat_id=action["update"]["effective_chat"]["id"],
                text="You are the best!",
                reply_markup=markup,
            )

        return transition


if __name__ == "__main__":
    bot = SimpleInlineButtonBot("YOUR_TELEGRAM_TOKEN")
    bot.run()
