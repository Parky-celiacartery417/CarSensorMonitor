from fastapi import APIRouter

from app.api.auth import router as auth_router
from app.api.cars import router as cars_router

router = APIRouter()
router.include_router(auth_router, prefix="/auth", tags=["auth"])
router.include_router(cars_router, prefix="/cars", tags=["cars"])
