import asyncio
from datetime import datetime
from dataclasses import dataclass
from typing import List

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from telegram import User


@dataclass
class ScheduledTask:
    message: str
    span: int


class AbandonedChatScheduler:

    def __init__(self, tasks: List[ScheduledTask], minute='*', hour='*', day='*', month='*', day_of_week='*'):
        self.application = None
        self.state_machine = None

        self.scheduler = BackgroundScheduler()

        self.tasks = tasks

        self.minute = minute
        self.hour = hour
        self.day = day
        self.month = month
        self.day_of_week = day_of_week

    def start(self, application, state_machine):
        self.application = application
        self.state_machine = state_machine
        cron_trigger = CronTrigger(minute=self.minute, hour=self.hour, day=self.day, month=self.month,
                                   day_of_week=self.day_of_week)

        def step():
            asyncio.run(self.process())

        self.scheduler.add_job(step, trigger=cron_trigger)
        self.scheduler.start()

    async def process(self):

        # List users
        for user_id in self.application.user_data:

            chats = self.application.user_data[user_id]["chats"]

            # List chats
            for chat_id in chats:

                date_modified = chats[chat_id]['date_modified']
                past_time = datetime.now().timestamp() - date_modified

                for task in self.tasks:
                    if past_time > task.span:
                        await self.state_machine.process({
                            "update": {
                                "message": {
                                    "from_user": User(id=user_id, first_name='', is_bot=False)
                                },
                                "effective_chat": {
                                    "id": chat_id
                                }
                            },
                            "context": self.application,
                            "text": task.message
                        })
