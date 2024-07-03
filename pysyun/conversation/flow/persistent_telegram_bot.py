from telegram.ext import PicklePersistence, Application

from pysyun.conversation.flow.dialog_state_machine import DialogStateMachineBuilder
from pysyun.conversation.flow.telegram_bot import TelegramBot
from pysyun.conversation.worker.scheduler import scheduler


class PersistentTelegramBot(TelegramBot):

    def __init__(self, token, initial_state="/start", persistence_file="persistent_data.pickle"):
        self.application = Application \
            .builder() \
            .token(token) \
            .persistence(PicklePersistence(filepath=persistence_file)) \
            .build()
        self.state_machine = self.build_state_machine(DialogStateMachineBuilder(initial_state=initial_state)).build()
        self.user_data = {}

        # Scheduler setup in config.py
        # Starts the Scheduled jobs
        scheduler.start()
