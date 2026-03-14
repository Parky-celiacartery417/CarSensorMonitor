from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime, timezone

from app.models.base import Base, TimestampMixin, generate_uuid


class Car(Base, TimestampMixin):
    __tablename__ = "cars"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=generate_uuid)
    carsensor_id: Mapped[str] = mapped_column(String(255), unique=True, index=True)

    maker: Mapped[str] = mapped_column(String(100))
    maker_ja: Mapped[str | None] = mapped_column(String(100))
    model: Mapped[str] = mapped_column(String(200))
    model_ja: Mapped[str | None] = mapped_column(String(200))
    grade: Mapped[str | None] = mapped_column(String(200))
    body_type: Mapped[str | None] = mapped_column(String(100))

    year: Mapped[int | None] = mapped_column(Integer)
    mileage_km: Mapped[int | None] = mapped_column(Integer)
    total_price_yen: Mapped[int | None] = mapped_column(Integer)
    body_price_yen: Mapped[int | None] = mapped_column(Integer)
    displacement_cc: Mapped[int | None] = mapped_column(Integer)

    transmission: Mapped[str | None] = mapped_column(String(50))
    fuel_type: Mapped[str | None] = mapped_column(String(50))
    drive_type: Mapped[str | None] = mapped_column(String(50))
    color: Mapped[str | None] = mapped_column(String(100))
    color_ja: Mapped[str | None] = mapped_column(String(100))

    inspection_expiry: Mapped[str | None] = mapped_column(String(100))
    repair_history: Mapped[str | None] = mapped_column(String(50))

    dealer_name: Mapped[str | None] = mapped_column(String(300))
    dealer_location: Mapped[str | None] = mapped_column(String(300))

    image_url: Mapped[str | None] = mapped_column(Text)
    detail_url: Mapped[str | None] = mapped_column(Text)

    is_active: Mapped[bool] = mapped_column(Boolean, default=True, index=True)

    price_history: Mapped[list["PriceHistory"]] = relationship(
        back_populates="car", cascade="all, delete-orphan", order_by="PriceHistory.recorded_at.desc()"
    )


class PriceHistory(Base):
    __tablename__ = "price_history"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=generate_uuid)
    car_id: Mapped[str] = mapped_column(String(36), ForeignKey("cars.id", ondelete="CASCADE"), index=True)
    total_price_yen: Mapped[int | None] = mapped_column(Integer)
    body_price_yen: Mapped[int | None] = mapped_column(Integer)
    recorded_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )

    car: Mapped["Car"] = relationship(back_populates="price_history")
