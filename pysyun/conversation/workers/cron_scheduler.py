from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger


class CronScheduler:
    def __init__(self, minute='*', hour='*', day='*', month='*', day_of_week='*'):
        self._scheduler = AsyncIOScheduler()
        self._minute = minute
        self._hour = hour
        self._day = day
        self._month = month
        self._day_of_week = day_of_week
        self._cyber = None

    async def process(self):
        await self._cyber.process()

    def _start(self, cyber):
        self._cyber = cyber

        cron_trigger = CronTrigger(
            minute=self._minute,
            hour=self._hour,
            day=self._day,
            month=self._month,
            day_of_week=self._day_of_week
        )

        self._scheduler.add_job(self.process, trigger=cron_trigger)
        self._scheduler.start()
