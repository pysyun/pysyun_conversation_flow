from apscheduler.schedulers.asyncio import AsyncIOScheduler

from pysyun.config import SchedulerConfig
from pysyun.conversation.worker.tasks import send_reminder

# APScheduler setup

scheduler = AsyncIOScheduler()

scheduler.add_job(send_reminder, trigger='interval', minutes=SchedulerConfig.interval)
