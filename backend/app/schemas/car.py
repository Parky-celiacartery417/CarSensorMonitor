from datetime import datetime

from pydantic import BaseModel


class PriceHistoryResponse(BaseModel):
    total_price_yen: int | None
    body_price_yen: int | None
    recorded_at: datetime


class CarResponse(BaseModel):
    id: str
    carsensor_id: str
    maker: str
    maker_ja: str | None = None
    model: str
    model_ja: str | None = None
    grade: str | None = None
    body_type: str | None = None
    year: int | None = None
    mileage_km: int | None = None
    total_price_yen: int | None = None
    body_price_yen: int | None = None
    displacement_cc: int | None = None
    transmission: str | None = None
    fuel_type: str | None = None
    drive_type: str | None = None
    color: str | None = None
    color_ja: str | None = None
    inspection_expiry: str | None = None
    repair_history: str | None = None
    dealer_name: str | None = None
    dealer_location: str | None = None
    image_url: str | None = None
    detail_url: str | None = None
    is_active: bool
    created_at: datetime
    updated_at: datetime


class CarDetailResponse(CarResponse):
    price_history: list[PriceHistoryResponse] = []


class CarListResponse(BaseModel):
    items: list[CarResponse]
    total: int
    page: int
    per_page: int
    pages: int
