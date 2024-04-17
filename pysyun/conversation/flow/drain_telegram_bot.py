from pysyun.conversation.flow.persistent_telegram_bot import PersistentTelegramBot


class DrainTelegramBot(PersistentTelegramBot):

    async def process(self, message):
        await self.state_machine.process(message)
