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
    
    
    
    # response schema for payment link creation
    
class PaymentLinkResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    product_name: str
    description: str | None
    amount: Decimal
    currency: str
    token: str
    payment_url: str
    status: str
    expires_at: datetime
    created_at: datetime
    
    
    # Payment request / respinse schemas   
class PaymentCreate(BaseModel):
    
    
    idempotency_key: str = Field(
    min_length=1,
    max_length=64,
)
    
    
    
    payment_link_token: str = Field(
        min_length=1,
        max_length=32,
    )

    amount: Decimal = Field(
        gt=0,
        max_digits=12,
        decimal_places=2,
    )

    currency: str = Field(
        min_length=3,
        max_length=3,
    )

    @field_validator("currency")
    @classmethod
    def validate_currency(cls, value: str) -> str:
        return value.upper()


class CheckoutPaymentCreate(BaseModel):
    idempotency_key: str = Field(min_length=1, max_length=64)
    payment_link_token: str = Field(min_length=1, max_length=32)


class PaymentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    payment_link_id: str
    amount: Decimal
    currency: str
    status: str
    created_at: datetime