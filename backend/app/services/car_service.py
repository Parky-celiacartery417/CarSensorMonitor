import math
from datetime import datetime, timezone

from sqlalchemy import Select, func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.car import Car, PriceHistory


def apply_filters(
    query: Select,
    maker: str | None = None,
    year_min: int | None = None,
    year_max: int | None = None,
    price_min: int | None = None,
    price_max: int | None = None,
    mileage_max: int | None = None,
    transmission: str | None = None,
    body_type: str | None = None,
    search: str | None = None,
) -> Select:
    query = query.where(Car.is_active == True)  # noqa: E712

    if maker:
        query = query.where(Car.maker.ilike(f"%{maker}%"))
    if year_min:
        query = query.where(Car.year >= year_min)
    if year_max:
        query = query.where(Car.year <= year_max)
    if price_min:
        query = query.where(Car.total_price_yen >= price_min)
    if price_max:
        query = query.where(Car.total_price_yen <= price_max)
    if mileage_max:
        query = query.where(Car.mileage_km <= mileage_max)
    if transmission:
        query = query.where(Car.transmission.ilike(f"%{transmission}%"))
    if body_type:
        query = query.where(Car.body_type.ilike(f"%{body_type}%"))
    if search:
        pattern = f"%{search}%"
        query = query.where(
            Car.maker.ilike(pattern)
            | Car.model.ilike(pattern)
            | Car.grade.ilike(pattern)
        )
    return query


async def list_cars(
    db: AsyncSession,
    page: int = 1,
    per_page: int = 20,
    sort_by: str = "created_at",
    sort_order: str = "desc",
    **filters,
) -> dict:
    base_query = select(Car)
    base_query = apply_filters(base_query, **filters)

    count_query = select(func.count()).select_from(base_query.subquery())
    total_result = await db.execute(count_query)
    total = total_result.scalar() or 0

    sort_column = getattr(Car, sort_by, Car.created_at)
    if sort_order == "asc":
        base_query = base_query.order_by(sort_column.asc())
    else:
        base_query = base_query.order_by(sort_column.desc())

    offset = (page - 1) * per_page
    base_query = base_query.offset(offset).limit(per_page)

    result = await db.execute(base_query)
    items = result.scalars().all()

    return {
        "items": items,
        "total": total,
        "page": page,
        "per_page": per_page,
        "pages": math.ceil(total / per_page) if total > 0 else 0,
    }


async def get_car_by_id(db: AsyncSession, car_id: str) -> Car | None:
    result = await db.execute(
        select(Car).where(Car.id == car_id).options(selectinload(Car.price_history))
    )
    return result.scalar_one_or_none()


async def upsert_car(db: AsyncSession, data: dict) -> tuple[Car, bool]:
    carsensor_id = data["carsensor_id"]
    result = await db.execute(select(Car).where(Car.carsensor_id == carsensor_id))
    existing = result.scalar_one_or_none()

    if existing:
        price_changed = (
            existing.total_price_yen != data.get("total_price_yen")
            or existing.body_price_yen != data.get("body_price_yen")
        )

        for key, value in data.items():
            if key != "carsensor_id":
                setattr(existing, key, value)
        existing.is_active = True
        existing.updated_at = datetime.now(timezone.utc)

        if price_changed:
            history = PriceHistory(
                car_id=existing.id,
                total_price_yen=data.get("total_price_yen"),
                body_price_yen=data.get("body_price_yen"),
            )
            db.add(history)

        await db.commit()
        return existing, False
    else:
        car = Car(**data)
        db.add(car)
        await db.flush()

        history = PriceHistory(
            car_id=car.id,
            total_price_yen=data.get("total_price_yen"),
            body_price_yen=data.get("body_price_yen"),
        )
        db.add(history)
        await db.commit()
        return car, True


async def get_makers(db: AsyncSession) -> list[str]:
    result = await db.execute(
        select(Car.maker)
        .where(Car.is_active == True)  # noqa: E712
        .distinct()
        .order_by(Car.maker)
    )
    return [row[0] for row in result.all()]


async def get_stats(db: AsyncSession) -> dict:
    total = await db.execute(
        select(func.count()).where(Car.is_active == True)  # noqa: E712
    )
    avg_price = await db.execute(
        select(func.avg(Car.total_price_yen)).where(
            Car.is_active == True, Car.total_price_yen.isnot(None)  # noqa: E712
        )
    )
    makers_count = await db.execute(
        select(func.count(func.distinct(Car.maker))).where(Car.is_active == True)  # noqa: E712
    )

    return {
        "total_cars": total.scalar() or 0,
        "average_price_yen": int(avg_price.scalar() or 0),
        "makers_count": makers_count.scalar() or 0,
    }
