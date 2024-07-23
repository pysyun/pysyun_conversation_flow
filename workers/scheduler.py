from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger


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

        self.scheduler.add_job(self.process, trigger=cron_trigger)
        self.scheduler.start()

    def process(self):
        print(self.injected_message)
