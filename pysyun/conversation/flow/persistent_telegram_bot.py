from pysyun.conversation.flow.dialog_state_machine import DialogStateMachineBuilder
from telegram.ext import PicklePersistence, Application
from pysyun.conversation.flow.telegram_bot import TelegramBot


class PersistentTelegramBot(TelegramBot):

    def __init__(self, token, initial_state="/start", persistence_file="persistent_data.pickle", scheduler=None):
        self.application = Application \
            .builder() \
            .token(token) \
            .persistence(PicklePersistence(filepath=persistence_file)) \
            .build()
        self.state_machine = self.build_state_machine(DialogStateMachineBuilder(initial_state=initial_state)).build()

        if scheduler:
            self.scheduler = scheduler
            scheduler.start(self.application, self.state_machine)
