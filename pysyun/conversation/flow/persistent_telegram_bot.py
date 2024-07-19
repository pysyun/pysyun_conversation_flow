from telegram.ext import PicklePersistence, Application

from pysyun.conversation.flow.dialog_state_machine import DialogStateMachineBuilder
from pysyun.conversation.flow.telegram_bot import TelegramBot
from pysyun.conversation.workers.scheduler import Scheduler


class PersistentTelegramBot(TelegramBot):

    def __init__(self, token, scheduler: Scheduler = None,
                 initial_state="/start", persistence_file="persistent_data.pickle"):
        self.application = Application \
            .builder() \
            .token(token) \
            .persistence(PicklePersistence(filepath=persistence_file)) \
            .build()
        self.state_machine = self.build_state_machine(DialogStateMachineBuilder(initial_state=initial_state)).build()
        self.user_data = {}

        # Scheduler setup in config.py
        # Starts the Scheduled jobs
        if scheduler:
            scheduler.set_application(self.application)
            scheduler.set_state_machine(self.state_machine)
            scheduler.set_persistence_file(persistence_file)
            scheduler.start()

