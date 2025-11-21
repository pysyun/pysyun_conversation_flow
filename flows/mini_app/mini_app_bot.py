from pysyun.conversation.flow.telegram_bot import TelegramBot
from telegram import MenuButtonWebApp, WebAppInfo


class MiniAppBot(TelegramBot):
    def build_state_machine(self, builder):
        return builder \
            .edge("/start", "/start", "/start", on_transition=self.start_transition()) \
            .edge("/start", "/start", "/mini", on_transition=self.mini_transition())

    def start_transition(self):
        async def transition(action):
            # На старт показуємо кнопку
            markup = self.build_inline_keyboard(
                [
                    [
                        ["Open Mini App", None, None, "https://github.com/pysyun/pysyun_conversation_flow"]
                    ]
                ]
            )
            await action["context"].bot.send_message(
                chat_id=action["update"]["effective_chat"]["id"],
                text="Welcome! Click the button or use /mini command",
                reply_markup=markup,
            )
        return transition

    def mini_transition(self):
        async def transition(action):
            # Для команди створюємо MenuButton з веб-застосунком
            web_app = WebAppInfo(url="https://github.com/pysyun/pysyun_conversation_flow")
            await action["context"].bot.set_chat_menu_button(
                chat_id=action["update"]["effective_chat"]["id"],
                menu_button=MenuButtonWebApp(text="Mini App", web_app=web_app)
            )
            # Відправляємо повідомлення про успішну установку
            await action["context"].bot.send_message(
                chat_id=action["update"]["effective_chat"]["id"],
                text="Mini app menu button has been set!"
            )
        return transition


if __name__ == "__main__":
    bot = MiniAppBot("YOUR_TELEGRAM_TOKEN")
    bot.run()
