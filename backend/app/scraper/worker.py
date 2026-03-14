"""APScheduler worker — schedules the scraper to run at configured intervals."""

import logging

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger

from app.core.config import settings

logger = logging.getLogger(__name__)


async def scrape_job():
    """Wrapper that imports and runs the scraper."""
    from app.scraper.spider import run_scrape

    try:
        await run_scrape()
    except Exception as e:
        logger.error(f"Scrape job failed: {e}")


async def start_scheduler() -> AsyncIOScheduler:
    scheduler = AsyncIOScheduler()
    scheduler.add_job(
        scrape_job,
        trigger=IntervalTrigger(minutes=settings.SCRAPE_INTERVAL_MINUTES),
        id="carsensor_scraper",
        name="CarSensor Scraper",
        replace_existing=True,
        max_instances=1,
    )
    scheduler.start()
    logger.info(f"Scheduler started, scraping every {settings.SCRAPE_INTERVAL_MINUTES} minutes")

    # Run first scrape on startup (non-blocking)
    import asyncio

    asyncio.create_task(scrape_job())
    return scheduler


async def stop_scheduler(scheduler: AsyncIOScheduler):
    if scheduler.running:
        scheduler.shutdown(wait=False)
        logger.info("Scheduler stopped")
