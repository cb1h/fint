from apscheduler.schedulers.asyncio import AsyncIOScheduler
from bot.handlers.report import report_command
from config import REPORT_DAY, REPORT_TIME

async def schedule_weekly_report(dp):
    scheduler = AsyncIOScheduler()
    scheduler.add_job(report_command, 'cron', day_of_week=str(REPORT_DAY), hour=int(REPORT_TIME.split(':')[0]), minute=int(REPORT_TIME.split(':')[1]), args=[dp])
    scheduler.start()