from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user
from app.core.database import get_db
from app.models.user import User
from app.schemas.car import CarDetailResponse, CarListResponse, CarResponse, PriceHistoryResponse
from app.services.car_service import get_car_by_id, get_makers, get_stats, list_cars

router = APIRouter()


@router.get("", response_model=CarListResponse)
async def get_cars(
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    sort_by: str = Query("created_at", pattern="^(created_at|total_price_yen|year|mileage_km)$"),
    sort_order: str = Query("desc", pattern="^(asc|desc)$"),
    maker: str | None = None,
    year_min: int | None = None,
    year_max: int | None = None,
    price_min: int | None = None,
    price_max: int | None = None,
    mileage_max: int | None = None,
    transmission: str | None = None,
    body_type: str | None = None,
    search: str | None = None,
    db: AsyncSession = Depends(get_db),
    _user: User = Depends(get_current_user),
):
    result = await list_cars(
        db,
        page=page,
        per_page=per_page,
        sort_by=sort_by,
        sort_order=sort_order,
        maker=maker,
        year_min=year_min,
        year_max=year_max,
        price_min=price_min,
        price_max=price_max,
        mileage_max=mileage_max,
        transmission=transmission,
        body_type=body_type,
        search=search,
    )
    return CarListResponse(
        items=[CarResponse.model_validate(car, from_attributes=True) for car in result["items"]],
        total=result["total"],
        page=result["page"],
        per_page=result["per_page"],
        pages=result["pages"],
    )


@router.get("/makers", response_model=list[str])
async def get_all_makers(
    db: AsyncSession = Depends(get_db),
    _user: User = Depends(get_current_user),
):
    return await get_makers(db)


@router.get("/stats")
async def get_car_stats(
    db: AsyncSession = Depends(get_db),
    _user: User = Depends(get_current_user),
):
    return await get_stats(db)


@router.get("/{car_id}", response_model=CarDetailResponse)
async def get_car(
    car_id: str,
    db: AsyncSession = Depends(get_db),
    _user: User = Depends(get_current_user),
):
    car = await get_car_by_id(db, car_id)
    if car is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Car not found")

    return CarDetailResponse(
        **CarResponse.model_validate(car, from_attributes=True).model_dump(),
        price_history=[
            PriceHistoryResponse.model_validate(ph, from_attributes=True)
            for ph in car.price_history
        ],
    )
