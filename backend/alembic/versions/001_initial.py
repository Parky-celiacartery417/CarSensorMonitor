"""initial schema

Revision ID: 001
Revises:
Create Date: 2025-01-01 00:00:00.000000
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("username", sa.String(100), unique=True, index=True, nullable=False),
        sa.Column("hashed_password", sa.String(255), nullable=False),
        sa.Column("is_active", sa.Boolean(), default=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )

    op.create_table(
        "cars",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("carsensor_id", sa.String(255), unique=True, index=True, nullable=False),
        sa.Column("maker", sa.String(100), nullable=False),
        sa.Column("maker_ja", sa.String(100)),
        sa.Column("model", sa.String(200), nullable=False),
        sa.Column("model_ja", sa.String(200)),
        sa.Column("grade", sa.String(200)),
        sa.Column("body_type", sa.String(100)),
        sa.Column("year", sa.Integer()),
        sa.Column("mileage_km", sa.Integer()),
        sa.Column("total_price_yen", sa.Integer()),
        sa.Column("body_price_yen", sa.Integer()),
        sa.Column("displacement_cc", sa.Integer()),
        sa.Column("transmission", sa.String(50)),
        sa.Column("fuel_type", sa.String(50)),
        sa.Column("drive_type", sa.String(50)),
        sa.Column("color", sa.String(100)),
        sa.Column("color_ja", sa.String(100)),
        sa.Column("inspection_expiry", sa.String(100)),
        sa.Column("repair_history", sa.String(50)),
        sa.Column("dealer_name", sa.String(300)),
        sa.Column("dealer_location", sa.String(300)),
        sa.Column("image_url", sa.Text()),
        sa.Column("detail_url", sa.Text()),
        sa.Column("is_active", sa.Boolean(), default=True, index=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )

    op.create_table(
        "price_history",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column(
            "car_id",
            sa.String(36),
            sa.ForeignKey("cars.id", ondelete="CASCADE"),
            index=True,
            nullable=False,
        ),
        sa.Column("total_price_yen", sa.Integer()),
        sa.Column("body_price_yen", sa.Integer()),
        sa.Column("recorded_at", sa.DateTime(timezone=True), nullable=False),
    )

    op.create_table(
        "scrape_runs",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("started_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("finished_at", sa.DateTime(timezone=True)),
        sa.Column("status", sa.String(20), default="running"),
        sa.Column("cars_found", sa.Integer(), default=0),
        sa.Column("cars_new", sa.Integer(), default=0),
        sa.Column("cars_updated", sa.Integer(), default=0),
        sa.Column("error_message", sa.Text()),
    )


def downgrade() -> None:
    op.drop_table("scrape_runs")
    op.drop_table("price_history")
    op.drop_table("cars")
    op.drop_table("users")
