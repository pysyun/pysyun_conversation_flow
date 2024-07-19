import logging
import pickle
from datetime import datetime, timedelta

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from telegram.ext import Application

from logger import logger_instance


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

    def set_application(self, application: Application):
        self.application = application

    def set_persistence_file(self, persistence_file):
        self.persistence_file = persistence_file

    def set_state_machine(self, state_machine):
        self.state_machine = state_machine

    def start(self):
        logger_instance.info('Starting scheduler...')
        if self.persistence_file and self.application:
            if (self.state_transition and self.state_machine) or self.message:
                self.scheduler.add_job(self.task, 'interval', minutes=self.interval)
                self.scheduler.start()
            else:
                raise ValueError("Message text or state_transition and state_machine are required")
        else:
            raise ValueError("persistent_file and application are required")

    async def task(self):
        logger_instance.info('Starting task...')
        with open(self.persistence_file, 'rb') as file:
            data = pickle.load(file)
            users = data['user_data']
            for user_id in users:
                last_message_timestamp = users[user_id][user_id]['last_message_timestamp']
                last_message_datetime = datetime.fromtimestamp(last_message_timestamp)
                past_time = datetime.now() - timedelta(minutes=self.minutes)

                # If user was inactive
                if not last_message_datetime > past_time:
                    print(f"User {user_id} was inactive for more than {self.minutes} minute(s).")
                    await self.application.bot.send_message(user_id, self.message) if self.message else None
                    await self.state_machine.process(
                        {
                            "update":
                                {
                                    "effective_chat":
                                        {
                                            "id": user_id
                                        }
                                },
                            "context": self.application,
                            "text": self.state_transition
                        }
                    ) if self.state_transition else None
