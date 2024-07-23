import asyncio

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from telegram import User


class Scheduler:

    def __init__(self, injected_message, minute='*', hour='*', day='*', month='*', day_of_week='*'):
        self.state_machine = None

        self.scheduler = BackgroundScheduler()

        self.injected_message = injected_message

        self.minute = minute
        self.hour = hour
        self.day = day
        self.month = month
        self.day_of_week = day_of_week

    def start(self, state_machine):
        self.state_machine = state_machine
        cron_trigger = CronTrigger(minute=self.minute, hour=self.hour, day=self.day, month=self.month,
                                   day_of_week=self.day_of_week)

        def step():
            asyncio.run(self.process())

        self.scheduler.add_job(step, trigger=cron_trigger)
        self.scheduler.start()

    async def process(self):
        await self.state_machine.process({
            "update": {
                "message": {
                    "from_user": User(id=0, first_name='', is_bot=False)
                },
                "effective_chat": {
                    "id": 0
                }
            },
            # TODO: Pass the context
            "context": None,
            "text": self.injected_message
        })
