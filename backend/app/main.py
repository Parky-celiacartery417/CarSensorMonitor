import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text

from app.core.config import settings
from app.core.database import async_session, engine
from app.core.security import hash_password
from app.models import Base, User

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")


async def seed_admin():
    async with async_session() as session:
        result = await session.execute(text("SELECT id FROM users WHERE username = 'admin'"))
        row = result.first()
        if row is None:
            admin = User(
                username="admin",
                hashed_password=hash_password("admin123"),
                is_active=True,
            )
            session.add(admin)
            await session.commit()
            logger.info("Admin user seeded")
        else:
            await session.execute(
                text("UPDATE users SET hashed_password = :pw WHERE username = 'admin'"),
                {"pw": hash_password("admin123")},
            )
            await session.commit()
            logger.info("Admin password updated")


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    await seed_admin()

    from app.scraper.worker import start_scheduler, stop_scheduler

    scheduler = await start_scheduler()
    logger.info("Application started")
    yield
    await stop_scheduler(scheduler)
    await engine.dispose()
    logger.info("Application stopped")


app = FastAPI(title="CarSensor Monitor API", version="1.0.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://frontend:3000", "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from app.api import router  # noqa: E402

app.include_router(router, prefix="/api")
