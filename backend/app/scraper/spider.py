"""CarSensor.net spider — orchestrates page-by-page scraping with Playwright.

Navigates listing pages for configured makers, extracts car data via parser,
and upserts results into the database. Includes rate limiting, retries, and error isolation.
"""

import asyncio
import logging
from datetime import datetime, timezone

from playwright.async_api import async_playwright

from app.core.config import settings
from app.core.database import async_session
from app.models.scrape_run import ScrapeRun
from app.scraper.parser import parse_listing_page, parse_total_pages
from app.services.car_service import upsert_car

logger = logging.getLogger(__name__)

MAKER_CODE_MAP = {
    "TO": "トヨタ",
    "HO": "ホンダ",
    "NI": "日産",
    "MZ": "マツダ",
    "SB": "スバル",
    "SZ": "スズキ",
    "DA": "ダイハツ",
    "MI": "三菱",
    "LE": "レクサス",
}

USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/131.0.0.0 Safari/537.36"
)


def build_listing_url(maker_code: str, page: int = 1) -> str:
    """Build CarSensor listing URL for a maker and page number."""
    base = f"{settings.CARSENSOR_BASE_URL}/usedcar/b{maker_code}"
    if page == 1:
        return f"{base}/index.html"
    return f"{base}/index{page}.html"


async def scrape_page(page, url: str, retries: int = 3) -> str | None:
    """Load a page with retries and return HTML content."""
    for attempt in range(1, retries + 1):
        try:
            response = await page.goto(url, wait_until="domcontentloaded", timeout=30000)
            if response and response.status == 200:
                await page.wait_for_timeout(1000)
                return await page.content()
            elif response and response.status == 404:
                logger.warning(f"Page not found: {url}")
                return None
            else:
                status = response.status if response else "no response"
                logger.warning(f"Unexpected status {status} for {url}, attempt {attempt}")
        except Exception as e:
            logger.warning(f"Error loading {url}, attempt {attempt}: {e}")

        if attempt < retries:
            await asyncio.sleep(2 * attempt)

    return None


async def scrape_maker(page, maker_code: str, max_pages: int) -> list[dict]:
    """Scrape all pages for a given maker, up to max_pages."""
    all_cars = []
    url = build_listing_url(maker_code, 1)
    logger.info(f"Scraping maker {maker_code}, page 1: {url}")

    html = await scrape_page(page, url)
    if not html:
        logger.error(f"Failed to load first page for maker {maker_code}")
        return all_cars

    total_pages = parse_total_pages(html)
    pages_to_scrape = min(total_pages, max_pages)
    logger.info(f"Maker {maker_code}: {total_pages} total pages, scraping {pages_to_scrape}")

    cars = parse_listing_page(html)
    all_cars.extend(cars)

    for page_num in range(2, pages_to_scrape + 1):
        await asyncio.sleep(2)
        url = build_listing_url(maker_code, page_num)
        logger.info(f"Scraping maker {maker_code}, page {page_num}: {url}")

        html = await scrape_page(page, url)
        if not html:
            logger.warning(f"Failed to load page {page_num} for maker {maker_code}")
            continue

        cars = parse_listing_page(html)
        all_cars.extend(cars)

    return all_cars


async def run_scrape():
    """Main scraping entry point — scrapes all configured makers and saves to DB."""
    logger.info("Starting scrape run")
    max_pages = settings.SCRAPE_MAX_PAGES_PER_MAKER

    async with async_session() as db:
        run = ScrapeRun(status="running")
        db.add(run)
        await db.commit()
        await db.refresh(run)
        run_id = run.id

    total_found = 0
    total_new = 0
    total_updated = 0
    error_messages = []

    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(
                headless=True,
                args=["--no-sandbox", "--disable-dev-shm-usage"],
            )
            context = await browser.new_context(
                user_agent=USER_AGENT,
                viewport={"width": 1920, "height": 1080},
                locale="ja-JP",
            )
            page = await context.new_page()

            for maker_code in settings.MAKER_CODES:
                try:
                    cars_data = await scrape_maker(page, maker_code, max_pages)
                    total_found += len(cars_data)

                    for car_data in cars_data:
                        try:
                            async with async_session() as db:
                                _, is_new = await upsert_car(db, car_data)
                                if is_new:
                                    total_new += 1
                                else:
                                    total_updated += 1
                        except Exception as e:
                            logger.error(f"Failed to upsert car {car_data.get('carsensor_id')}: {e}")

                    await asyncio.sleep(3)
                except Exception as e:
                    msg = f"Error scraping maker {maker_code}: {e}"
                    logger.error(msg)
                    error_messages.append(msg)

            await browser.close()

        status = "success"
    except Exception as e:
        msg = f"Scrape run failed: {e}"
        logger.error(msg)
        error_messages.append(msg)
        status = "failed"

    async with async_session() as db:
        from sqlalchemy import select

        result = await db.execute(select(ScrapeRun).where(ScrapeRun.id == run_id))
        run = result.scalar_one()
        run.finished_at = datetime.now(timezone.utc)
        run.status = status
        run.cars_found = total_found
        run.cars_new = total_new
        run.cars_updated = total_updated
        run.error_message = "\n".join(error_messages) if error_messages else None
        await db.commit()

    logger.info(
        f"Scrape run finished: status={status}, found={total_found}, "
        f"new={total_new}, updated={total_updated}"
    )
