import asyncio
from dataclasses import dataclass
from typing import List

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from telegram import User
from telegram.constants import ChatType


@dataclass
class ScheduledTask:
    message: str
    span: int


class StateMachineScheduler:

    def __init__(self, tasks: List[ScheduledTask], minute='*', hour='*', day='*', month='*', day_of_week='*'):
        self.application = None
        self.state_machine = None

        self.scheduler = AsyncIOScheduler()

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
        for task in self.tasks:
            await self.state_machine.process({
                "update": {
                    "message": {
                        "from_user": User(id=0, first_name='', is_bot=False),
                        "chat_id": 0,
                        "chat": {
                            "type": ChatType.PRIVATE
                        }
                    },
                    "effective_chat": {
                        "id": 0
                    },
                    "effective_user": User(id=0, first_name='', is_bot=False)
                },
                "context": self.application,
                "text": task.message
            })
