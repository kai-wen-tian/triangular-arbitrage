import logging

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.schedulers.blocking import BlockingScheduler
from app.providers import logging_provider
from app.services.arbitrage.triangular import execute_tri

def create_scheduler() -> BlockingScheduler:
    logging_provider.register()

    logging.info("BlockingScheduler initializing")

    scheduler: BlockingScheduler = BlockingScheduler()

    register_job(scheduler)

    return scheduler


def register_job(scheduler):
    """
     注册调度任务
    """
    scheduler.add_job(execute_tri, 'interval', seconds=150,misfire_grace_time=None,max_instances=2)
