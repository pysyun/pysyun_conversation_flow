import pickle
from datetime import datetime, timedelta
from venv import logger

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from telegram import User
from telegram.ext import Application


class Scheduler:
    def __init__(self, minutes, hours, days, interval, message=None, state_transition=None):
        self.state_machine = None
        self.persistence_file = None
        self.application = None
        self.scheduler = AsyncIOScheduler()

        self.minutes = minutes + hours * 60 + days * 24 * 3600
        self.interval = interval

        self.message = message
        self.state_transition = state_transition

        if not self.message or not self.state_transition:
            raise ValueError("Message text or state_transition not specified")

    def set_application(self, application: Application):
        self.application = application

    def set_persistence_file(self, persistence_file):
        self.persistence_file = persistence_file

    def set_state_machine(self, state_machine):
        self.state_machine = state_machine

    def start(self):
        if self.persistence_file and self.application:
            self.scheduler.add_job(self.task, 'interval', minutes=self.interval)
            self.scheduler.start()
        else:
            raise ValueError("persistent_file and application are required")

    async def task(self):
        logger.info("Starting task...")
        with open(self.persistence_file, 'rb') as file:
            data = pickle.load(file)
            users = data['user_data']
            for user_id in users:
                last_message_timestamp = users[user_id][user_id]['last_message_timestamp']
                last_message_datetime = datetime.fromtimestamp(last_message_timestamp)
                past_time = datetime.now() - timedelta(minutes=self.minutes)

                # If user was inactive
                if not last_message_datetime > past_time:
                    await self.application.bot.send_message(user_id, self.message) if self.message else None
                    await self.state_machine.process(
                        {
                            "update":
                                {
                                    "message":
                                    {
                                        "from_user": User(id=user_id, first_name='', is_bot=False)
                                    },
                                    "effective_chat":
                                        {
                                            "id": user_id
                                        }
                                },
                            "context": self.application,
                            "text": self.state_transition
                        }
                    ) if self.state_transition else None
