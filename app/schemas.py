from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field, field_validator


# request and response schemas for payment link creation
class PaymentLinkCreate(BaseModel):
    product_name: str = Field(
        min_length=1,
        max_length=255,
    )

    description: str | None = Field(
        default=None,
        max_length=1000,
    )

    amount: Decimal = Field(
        gt=0,
        max_digits=12,
        decimal_places=2,
    )

    currency: str = Field(
        default="ZAR",
        min_length=3,
        max_length=3,
    )

    expires_in_minutes: int = Field(
        default=15,
        ge=1,
        le=1440,
    )

    @field_validator("currency")
    @classmethod
    def validate_currency(cls, value: str) -> str:
        return value.upper()