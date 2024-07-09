import pickle
from datetime import datetime, timedelta

from apscheduler.schedulers.asyncio import AsyncIOScheduler


class Scheduler:
    def __init__(self, minutes, hours, days, interval, message, application=None, persistence_file=None):
        self.scheduler = AsyncIOScheduler()
        self.application = application

        self.minutes = minutes + hours * 60 + days * 24 * 3600
        self.interval = interval

        self.message = message
        self.persistence_file = persistence_file

    def start(self):
        print('Starting scheduler...')
        self.scheduler.add_job(self.task, 'interval', minutes=self.interval)
        self.scheduler.start()

    async def task(self):
        print('Starting task...')
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
                    await self.application.bot.send_message(user_id, self.message)
