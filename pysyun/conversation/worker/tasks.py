import os
import pickle
from datetime import datetime, timedelta

from pysyun.config import SchedulerConfig


def get_bot():
    from telegram.ext import Application
    from dotenv import load_dotenv
    load_dotenv()
    token = os.getenv('TELEGRAM_BOT_TOKEN')
    return Application.builder().token(token).build()


async def send_reminder(persistence_file=SchedulerConfig.persistence_file, minutes=SchedulerConfig.minutes,
                        hours=SchedulerConfig.hours, days=SchedulerConfig.days, message=SchedulerConfig.message):
    minutes = minutes + hours * 60 + days * 24 * 3600

    # Deserialize from a file
    with open(persistence_file, 'rb') as file:
        data = pickle.load(file)
        users = data['user_data']

        for user_id in users:
            last_message_timestamp = users[user_id][user_id]['last_message_timestamp']
            last_message_datetime = datetime.fromtimestamp(last_message_timestamp)
            past_time = datetime.now() - timedelta(minutes=minutes)

            # If user was inactive
            if not last_message_datetime > past_time:
                print(f"User {user_id} was inactive for more than {minutes} minute(s).")
                await get_bot().bot.send_message(user_id, message)
